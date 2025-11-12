import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, csv, os, random

CONFIG_DIR = "config"
PRESETS_DIR = os.path.join(CONFIG_DIR, "presets")
ZONES_FILE = os.path.join(CONFIG_DIR, "zones.csv")
CONTEXTS_FILE = os.path.join(CONFIG_DIR, "contexts.json")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")

# ============================================================
# UTILITAIRES
# ============================================================
def load_json(path, default=None):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default or {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_zones(file_path):
    zones = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["split"] = int(row.get("split", 0))
            zones.append(row)
    return zones

def load_presets():
    presets = []
    if os.path.exists(PRESETS_DIR):
        for file in os.listdir(PRESETS_DIR):
            if file.endswith(".json"):
                presets.append(file.replace(".json", ""))
    return presets

def read_preset(name):
    path = os.path.join(PRESETS_DIR, name + ".json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def save_preset(name, data):
    path = os.path.join(PRESETS_DIR, name + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ============================================================
# CHARGEMENT INITIAL
# ============================================================
zones = load_zones(ZONES_FILE)
contexts = load_json(CONTEXTS_FILE)
presets = load_presets()
settings = load_json(SETTINGS_FILE, {
    "last_preset": presets[0] if presets else "",
    "difficulty": "normal",
    "language": "fr",
    "dupe_mode": "dupe both"
})

# ============================================================
# FENÊTRE PRINCIPALE
# ============================================================
root = tk.Tk()
root.title("Pokémon Randomizer Launcher")
root.geometry("700x500")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

main_tab = ttk.Frame(notebook)
notebook.add(main_tab, text="Principal")

# Langue
ttk.Label(main_tab, text="Langue :").grid(row=0, column=0, padx=10, pady=10, sticky="w")
language_var = tk.StringVar(value=settings.get("language", "fr"))
ttk.Combobox(main_tab, textvariable=language_var, values=["fr", "en"], width=10).grid(row=0, column=1, sticky="w")

# Regional Variant Dupe Clause
ttk.Label(main_tab, text="Regional Variant Dupe Clause :").grid(row=1, column=0, padx=10, pady=10, sticky="w")
dupe_mode_var = tk.StringVar(value=settings.get("dupe_mode", "dupe both"))
ttk.Combobox(main_tab, textvariable=dupe_mode_var,
             values=["dupe both", "dupe same name", "dupe neither"],
             width=20, state="readonly").grid(row=1, column=1, sticky="w")

# Difficulté
ttk.Label(main_tab, text="Difficulté :").grid(row=2, column=0, padx=10, pady=10, sticky="w")
difficulty_var = tk.StringVar(value=settings.get("difficulty", "normal"))
ttk.Combobox(main_tab, textvariable=difficulty_var,
             values=["casu", "normal", "hardcore"]).grid(row=2, column=1, sticky="w")

# Preset
ttk.Label(main_tab, text="Preset :").grid(row=3, column=0, padx=10, pady=10, sticky="w")
preset_var = tk.StringVar(value=settings.get("last_preset", presets[0] if presets else ""))
preset_combo = ttk.Combobox(main_tab, textvariable=preset_var, values=presets, width=25)
preset_combo.grid(row=3, column=1, sticky="w")

# ============================================================
# LOGIQUE DU LANCEUR
# ============================================================
def open_preset_editor():
    name = preset_var.get().strip()
    if not name:
        messagebox.showerror("Erreur", "Veuillez sélectionner un preset.")
        return

    if name == "full_random":
        # ⚠️ Fenêtre spéciale pour le preset full_random
        messagebox.showinfo("Preset verrouillé",
                            "Le preset 'full_random' ne peut pas être modifié.\n"
                            "Vous pouvez uniquement choisir un contexte.")
        FullRandomContextEditor(root, name)
    else:
        data = read_preset(name)
        PresetEditor(root, name, data)

ttk.Button(main_tab, text="Modifier le preset", command=open_preset_editor).grid(row=3, column=2, padx=10)
ttk.Button(main_tab, text="Lancer", command=lambda: messagebox.showinfo("Lancement", "Script lancé ✅")).grid(row=4, column=1, pady=20)

# Sauvegarde à la fermeture
def on_close():
    settings["last_preset"] = preset_var.get()
    settings["difficulty"] = difficulty_var.get()
    settings["language"] = language_var.get()
    settings["dupe_mode"] = dupe_mode_var.get()
    save_json(SETTINGS_FILE, settings)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# ============================================================
# FENÊTRE SPÉCIALE POUR LE PRESET FULL_RANDOM
# ============================================================
class FullRandomContextEditor(tk.Toplevel):
    def __init__(self, master, preset_name):
        super().__init__(master)
        self.title("Preset full_random - Choix du contexte")
        self.geometry("400x200")
        self.preset_name = preset_name

        ttk.Label(self, text="Contexte :").pack(pady=10)
        self.context_var = tk.StringVar(value=list(contexts.keys())[0])
        ttk.Combobox(self, textvariable=self.context_var,
                     values=list(contexts.keys()), width=25, justify="center").pack(pady=5)

        ttk.Button(self, text="💾 Sauvegarder", command=self.save_randomized_preset).pack(pady=15)

    def save_randomized_preset(self):
        ctx_name = self.context_var.get()
        ctx = contexts.get(ctx_name, {})
        start = ctx.get("splits", {}).get("start", 1)
        end = ctx.get("splits", {}).get("end", 9999)
        filtered = [z for z in zones if start <= z["split"] <= end]

        unique = {}
        for z in filtered:
            unique.setdefault(z["zone"], []).append(z["subzone"])

        # Construction automatique du preset
        zones_data = {}
        for zone_name, subzones in unique.items():
            sub_choices = [s for s in subzones if s != "Delay"]
            subzone = random.choice(sub_choices) if sub_choices else subzones[0]
            zones_data[zone_name] = {
                "subzone": subzone,
                "repel": False,
                "magnet_pull_or_static": "none",
                "zone_number": None
            }

        preset = {
            "name": self.preset_name,
            "difficulty": "normal",
            "context": ctx_name,
            "zones": zones_data
        }

        save_preset(self.preset_name, preset)
        messagebox.showinfo("Preset full_random", "Preset généré et sauvegardé avec succès !")
        self.destroy()

# ============================================================
# TOOLTIP
# ============================================================
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)
    def show(self, event=None):
        if self.tip:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        label = ttk.Label(tw, text=self.text, background="lightyellow",
                          relief="solid", borderwidth=1, wraplength=280)
        label.pack(ipadx=4, ipady=2)
    def hide(self, event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


# ============================================================
# FENÊTRE D'ÉDITION DE PRÉSET
# ============================================================
class PresetEditor(tk.Toplevel):
    def __init__(self, master, preset_name, data):
        super().__init__(master)
        self.title(f"Édition du preset : {preset_name}")
        self.geometry("850x720")
        self.preset_name = preset_name
        self.data = data or {}
        self.zone_widgets = {}

        # Sélecteur de contexte
        header_frame = ttk.Frame(self)
        header_frame.pack(anchor="center", pady=10)
        ttk.Label(header_frame, text="Contexte :").pack(side="left", padx=5)
        self.context_var = tk.StringVar(value=self.data.get("context", list(contexts.keys())[0]))
        context_menu = ttk.Combobox(header_frame, textvariable=self.context_var,
                                    values=list(contexts.keys()), width=25, justify="center")
        context_menu.pack(side="left")
        context_menu.bind("<<ComboboxSelected>>", lambda e: self.refresh_zones(force_clear=True))

        # Scroll global
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=10)
        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.inner_frame = ttk.Frame(self.scrollable_frame)
        self.inner_frame.pack(anchor="center", pady=10)
        for i in range(5):
            self.inner_frame.grid_columnconfigure(i, weight=1, uniform="col")

        # Boutons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Enregistrer", command=self.save_preset).pack(side="left", padx=15)
        ttk.Button(btn_frame, text="Enregistrer sous...", command=self.save_as_new).pack(side="left", padx=15)

        self.refresh_zones(force_clear=True)

    def build_headers(self, parent, row_index):
        """Construit les entêtes dans la même frame que les zones"""
        for i in range(5):
            parent.grid_columnconfigure(i, weight=1, uniform="col")
        ttk.Label(parent, text="Zone", anchor="center", width=25).grid(row=row_index, column=0, padx=5)
        ttk.Label(parent, text="Subzone", anchor="center", width=20).grid(row=row_index, column=1, padx=5)
        ttk.Label(parent, text="Encounter Manipulation", anchor="center", width=25).grid(row=row_index, column=2, padx=5)
        ttk.Label(parent, text="Repel Manip", anchor="center", width=15).grid(row=row_index, column=3, padx=5)
        zone_num_label = ttk.Label(parent, text="Zone numéro", anchor="center", width=15)
        zone_num_label.grid(row=row_index, column=4, padx=5)
        Tooltip(zone_num_label,
                "Définit l'ordre dans lequel cette zone sera randomisée.\n"
                "Exemple : '3' signifie que deux autres zones seront faites avant celle-ci.")
        ttk.Separator(parent, orient="horizontal").grid(
            row=row_index + 1, column=0, columnspan=5, sticky="ew", pady=(0, 5)
        )

    def get_filtered_zones(self):
        ctx = contexts.get(self.context_var.get(), {})
        start = ctx.get("splits", {}).get("start", 1)
        end = ctx.get("splits", {}).get("end", 9999)
        filtered = [z for z in zones if start <= z["split"] <= end]
        unique = {}
        for z in filtered:
            unique.setdefault(z["zone"], []).append(z["subzone"])
        return unique, start, end

    def refresh_zones(self, force_clear=False):
        for w in self.inner_frame.winfo_children():
            w.destroy()

        filtered, start, end = self.get_filtered_zones()
        all_zones_by_name = {}
        for z in zones:
            all_zones_by_name.setdefault(z["zone"], []).append(z["subzone"])

        row_index = 0
        self.build_headers(self.inner_frame, row_index)
        row_index += 2  # pour espacer sous la ligne de séparation

        zone_total = len(filtered)

        for zone_name, subzones in filtered.items():
            frame = ttk.Frame(self.inner_frame)
            frame.grid(row=row_index, column=0, columnspan=5, sticky="ew", pady=2)
            for c in range(5):
                frame.grid_columnconfigure(c, weight=1, uniform="col")

            vars = {}
            ttk.Label(frame, text=zone_name, anchor="center", width=25).grid(row=0, column=0, padx=5)

            # Sous-zones externes ?
            all_subzones = all_zones_by_name.get(zone_name, [])
            has_external_subzone = any(
                not (start <= z["split"] <= end)
                for z in zones if z["zone"] == zone_name
            )
            default_sub = self.data.get("zones", {}).get(zone_name, {}).get("subzone", subzones[0])
            sub_choices = list(subzones)
            if len(all_subzones) > len(subzones) and has_external_subzone:
                sub_choices.append("Delay")

            if len(sub_choices) > 1:
                sub_var = tk.StringVar(value=default_sub if default_sub in sub_choices else "Delay")
                ttk.Combobox(frame, textvariable=sub_var, values=sub_choices,
                             width=20, justify="center").grid(row=0, column=1, padx=5)
            else:
                ttk.Label(frame, text=subzones[0], anchor="center", width=20).grid(row=0, column=1, padx=5)
                sub_var = tk.StringVar(value=subzones[0])

            # Encounter Manip
            ability_var = tk.StringVar(value=self.data.get("zones", {}).get(zone_name, {}).get("magnet_pull_or_static", "none"))
            manip_frame = ttk.Frame(frame)
            manip_frame.grid(row=0, column=2, padx=10)
            rb1 = ttk.Radiobutton(manip_frame, variable=ability_var, value="mpull")
            rb2 = ttk.Radiobutton(manip_frame, variable=ability_var, value="static")
            rb3 = ttk.Radiobutton(manip_frame, variable=ability_var, value="none")
            rb1.pack(side="left", padx=5)
            rb2.pack(side="left", padx=5)
            rb3.pack(side="left", padx=5)
            Tooltip(rb1, "Magnet Pull : attire les pokémons acier.")
            Tooltip(rb2, "Static : attire les pokémons électriques.")
            Tooltip(rb3, "Aucun effet de manipulation de rencontre.")

            # Repel Manip
            repel_var = tk.BooleanVar(value=self.data.get("zones", {}).get(zone_name, {}).get("repel", False))
            repel_btn = ttk.Checkbutton(frame, variable=repel_var)
            repel_btn.grid(row=0, column=3, padx=10)
            Tooltip(repel_btn, "Repel Manip : force les pokémons à être au niveau maximum possible.")

            # Zone numéro
            zone_order_values = list(range(1, zone_total + 1))
            zone_num_default = self.data.get("zones", {}).get(zone_name, {}).get("zone_number", "")
            zone_num_var = tk.StringVar(value=str(zone_num_default) if zone_num_default else "")
            zone_menu = ttk.Combobox(frame, textvariable=zone_num_var, values=zone_order_values, width=10, justify="center")
            zone_menu.grid(row=0, column=4, padx=5)
            Tooltip(zone_menu, "Choisis la position d'apparition de cette zone (1 = première zone, etc.).")

            vars.update({
                "sub_var": sub_var,
                "repel_var": repel_var,
                "ability_var": ability_var,
                "zone_number": zone_num_var
            })
            self.zone_widgets[zone_name] = vars
            row_index += 1

    def save_preset(self):
        zones_data = {}
        used_orders = set()

        # Première passe : enregistrer les numéros déjà définis
        for zone_name, vars in self.zone_widgets.items():
            num_str = vars["zone_number"].get().strip()
            try:
                num = int(num_str)
            except ValueError:
                num = None
            if num and num not in used_orders:
                used_orders.add(num)
            zones_data[zone_name] = {
                "subzone": vars["sub_var"].get(),
                "repel": vars["repel_var"].get(),
                "magnet_pull_or_static": vars["ability_var"].get(),
                "zone_number": num  # sera corrigé si None
            }

        # Seconde passe : assigner automatiquement les numéros manquants
        next_num = 1
        for zone_name, info in zones_data.items():
            if info["zone_number"] is None:
                # Trouve le prochain numéro libre
                while next_num in used_orders:
                    next_num += 1
                info["zone_number"] = next_num
                used_orders.add(next_num)
                next_num += 1

        preset = {
            "name": self.preset_name,
            "difficulty": "normal",
            "context": self.context_var.get(),
            "zones": zones_data
        }

        save_preset(self.preset_name, preset)
        messagebox.showinfo("Sauvegardé", f"Preset '{self.preset_name}' enregistré.")


    def save_as_new(self):
        new_name = simpledialog.askstring("Nouveau nom", "Nom du nouveau preset :")
        if not new_name:
            return
        self.preset_name = new_name
        self.save_preset()
        messagebox.showinfo("Nouveau preset", f"Preset '{new_name}' créé.")
        self.destroy()


root.mainloop()
