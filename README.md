# runandbun-box-randomizer
A modular Lua and Python-based randomizer for Pokémon Emerald (Run &amp; Bun). It automatically generates balanced, ready-to-play PC boxes based on configurable presets, with full support for encounter manipulation, regional variants, and custom difficulty settings.

### by Baat01

---

## How to Use

### Running the Launcher

Open `launcher.py`.

### Main Menu (Launcher)

- **Language:** changes interface language (not functional yet).
- **Regional Variant Dupes Clause:** selects how regional variant duplicates are handled.
- **Difficulty:** defines the difficulty (not yet implemented; affects the number of deaths at script start).
- **Preset:** choose the preset configuration.
- **Launch:** saves the selected parameters for the randomizer script.

### Preset Editor Menu

- **Subzone:** choose the subzones to include in the preset (Land, Surf, etc.).
    
    When a subzone becomes available later in the game (e.g., Rustboro City Other – Fossil during the Norman split), a “Delay” option can be toggled to skip it.
    
- **Encounter Manipulation:** enables Magnet Pull or Static if a Pokémon with the ability is available.
- **Repel Manip:** enables repel-based encounter control to get only max-level Pokémon.
- **Zone Number:** defines the encounter roll order (currently not functional).

### Script Execution

After configuring and saving through the launcher:

1. Load the script in your emulator.
2. A “Randomizer” console tab will appear, displaying the selected settings.
3. Run `randomizeBox()` to generate the encounters according to your preset.

(Note: currently, all affected PC slots must contain valid Pokémon for the function to execute properly.)

---

## Fonctionnement

Lancez `launcher.py`.

## Menu principal du launcher

- “Langue” : permet de changer la langue (non fonctionnel pour l’instant)
- ”Regional Variant Dupes Clause” : permet de choisir le paramètre de dupe clause pour les variant régionals
- ”Difficulté” : permet de choisir la difficulté (non implémenté pour l’instant)(nombre de mort au lancement du script)
”Preset” :
- “Lancer” : Sauvegardes les paramètres choisi pour l’execution du script

## Menu principal du launcher

- “Subzone” : Permet de choisir les parties des zones qu’on va faire sur le préset (Land/Surf…). Si une zone possède une subzone disponible plus tard dans le jeu (exemple : Rustboro City Other (Fossile) au moment du Norman Split), une option “Delay” deviens disponible et permet de ne pas roll l’encounter
- ”Encounter Manipulation” : Permet de choisir si on veut lead magnet pull ou static si on a obtenu un pokémon le permettant avant
- ”Repel Manip” : Permet de choisir si on veut repel manip la zone pour avoir uniquement les pokémon niveaux max
- ”Zone Numéro” : Permet de choisir l’ordre des zone qui vont être roll (non fonctionnel pour le moment)

## Fonctionnement du script

1. Une fois avoir lancé le launcher et sauvegarder les paramètres avec le bouton “Lancer”, charger le script dans l’émulateur
2. Un onglet “Randomizer” devrait apparaître, avec les différentes info des settings dans la console
3. Lancez la fonction `randomizeBox()` pour randomizer selon les settings (pour l’instant, des pokémons doivent être présent sur tous les slots modifiés pour que la fonction s’exécute bien)

---

## 1. Overview

The **Run & Bun Randomizer** is a complete tool designed to automatically generate a **ready-to-play Pokémon PC box**, based on a **configurable preset selected through a graphical interface**.

Originally built for the **Pokémon Emerald (Run & Bun)** ROM, it automates the creation of balanced teams for specific segments (Norman & Weather Institute), while remaining **adaptable to other GBA ROMs** with minimal modification.

The goal of this tool is to allow players to:

- test and practice the game outside of the *Truck Hell* split (the actual gameplay portion);
- play with fun and exotic PC boxes;
- have a reliable and flexible tool for playtesting hackroms more easily;

while adjusting the difficulty and encounter conditions according to their preferences.

---

## 2. Project Structure

```
/RandomizerLauncher/
│
├── launcher.py                # Main GUI (preset selection & editing)
│
├── config/
│   ├── zones.csv              # Generic list of all in-game zones
│   ├── contexts.json          # Defines splits associated with each context (Norman, Winstitute, etc.)
│   ├── presets/               # Folder containing zone configurations
│   │   ├── tryhard.json
│   │   ├── full_random.json
│   │   ├── full_delay.json
│   │   ├── tryhard_winstitute.json
│   │   └── custom1.json
│   └── settings.json          # Stores last used preset, difficulty, language, and dupe clause
│
├── data/
│   ├── dupes_family.json              # Evolution family groups
│   ├── dupes_regionnal_variant.json   # Regional variant relationships
│   ├── movesets.json                  # Full movesets per Pokémon
│   ├── static.json                    # List of static Pokémon
│   ├── magnet_pull.json               # Pokémon with the Magnet Pull ability
│   ├── zones.json                     # Encounter data per zone
│   ├── types.json                     # Pokémon types
│
└── scripts/
    ├── randomizer.lua        # Main randomizer script
    └── runner.lua            # Loads JSON/CSV files and initializes the system

```

---

## 3. How It Works

### Step 1 – Selection via the Launcher

The `launcher.py` interface allows the user to:

- choose a **preset** (tryhard, full_random, etc.);
- set the **difficulty** and **dupe clause mode**;
- and create or modify custom presets.

The `full_random` preset is a special case:

- it cannot be manually edited;
- only the **context** can be selected;
- **subzones** are randomly chosen;
- all **encounter manipulations** (repel, magnet pull, static) are disabled.

---

### Step 2 – Loading via the Runner

The `runner.lua` file:

- loads the selected preset;
- reads the data files (`movesets`, `types`, `dupes`, `zones`, etc.);
- and builds the structures required by the randomizer.

---

### Step 3 – Running the Randomizer

The `randomizer.lua` script contains the core logic for Pokémon generation and creation.

All the randomization is handled by a single function:

### `randomizeBox()`

This function:

1. Reads the zones defined in the selected preset;
2. Randomly selects Pokémon according to encounter rates and dupe rules;
3. Applies appropriate movesets based on context (if available);
4. Creates the generated Pokémon directly in the PC boxes (`setPCBoxMon()`).

---

## 4. Example of Use

In your emulator’s Lua console:

```lua
-- Load the randomizer
dofile("H:\\Downloads\\Run&Bun\\Randomiser\\scripts\\THIEFSCRIPT.lua")

-- Launch full randomization
randomizeBox()

```

Typical output:

```
===============================================
Randomizer Initialization
Preset loaded : tryhard_winstitute
Context : Winstitute
Dupe Mode : dupe both
Difficulty : normal
===============================================
Slot 1 → Swampert lv.36 | Nature: Adamant | IVs: 27/22/18/6/25/31
Slot 2 → Altaria lv.34 | Nature: Jolly | IVs: 21/30/17/8/22/25
...
6 Pokémon successfully created in PC

```

---

## 5. Main Features

- **Modular Presets**
    
    The system relies on fully customizable presets, allowing users to define encounter structures and logic for specific contexts (Norman, Winstitute, etc.).
    
    Available modes include:
    
    - *Tryhard*: balanced and competitive;
    - *Full Random*: fully randomized with random subzones;
    - *Full Delay*: prioritizes late-game and water encounters;
    - *Custom*: user-defined configuration via the launcher.
- **Advanced Dupe Management**
    
    The randomizer prevents duplicate Pokémon from appearing across the same evolutionary family or regional variant group.
    
    This behavior is controlled by the **Regional Variant Dupe Clause**, offering three modes:
    
    - *dupe both*: standard and regional forms share the same family;
    - *dupe same name*: only identical names are treated as duplicates;
    - *dupe neither*: all forms are treated independently.
- **Encounter Manipulations**
    
    The system supports several encounter mechanics affecting spawn probabilities:
    
    - *Static*: increases Electric-type encounters;
    - *Magnet Pull*: attracts Steel-type Pokémon;
    - *Repel Manip*: forces encounters at maximum level.
        
        These features can be toggled on or off depending on the preset configuration.
        
- **Python Launcher (V1)**
    
    A simple and functional GUI developed in Python (Tkinter) enables users to:
    
    - select and edit existing presets;
    - create new presets from a given context;
    - manage difficulty, dupe mode, and language;
    - edit zones and subzones without manually modifying JSON or CSV files.

---

## 6. Compatibility

- Compatible ROM: **Run & Bun (Pokémon Emerald-based)**
- Supported emulators: **any emulator supporting Lua scripting**
- Required languages: **Python 3.11+** and **Lua 5.4**

---

## 7. Adaptability to Other Projects

The **Run & Bun Randomizer** was designed to be **highly modular** and **easily portable** to other ROMs or randomizer projects.

### To adapt it to another ROM:

1. **Change the PC memory address**
    
    In `THIEFSCRIPT.lua`, modify the following constant:
    
    ```lua
    PC_BASE = 0x2028848
    
    ```
    
    This address points to the first PC slot in Emerald.
    
    Replace it with the corresponding address for your target ROM (e.g., FireRed, Ruby, etc.).
    
2. **Adapt the Lua functions**
    
    Update the `readBoxMon` and `setBoxMon` functions, along with any relevant offsets, to match the memory structure of your ROM.
    
    These functions define how Pokémon data is read and written to memory.
    
3. **Update the data files**
    
    Modify the following to match the new ROM’s Pokémon and encounter data:
    
    - Files in the `data/` directory (`movesets.json`, `types.json`, `dupes_family.json`, etc.);
    - The `config/zones.csv` file (keeping the same `zone,subzone,split` format).

Following these three steps, the randomizer will function correctly on a new ROM without requiring any change to the main logic in `runner.lua` or `randomizer.lua`.

---

## 8. Current Project Status

- Main randomizer script
    - Functional
- Runner (data loader)
    - Functional
- Graphical launcher
    - Prototype
- Moveset data
    - Functional
    - In progress (120/340 complete)
- Encounter manipulation
    - Functional
- Death mechanic
    - Concept phase
- Documentation
    - In progress
- Launcher design (responsive and polished)
    - Planned
- English localization
    - Planned

---

## 9. Final Goal

To create a **simple and plug-and-play tool** capable of:

- generating balanced, ready-to-play saves;
- freely adjusting difficulty and dupe rules;
- sharing consistent configurations across multiple players;
- easily adapting the system to other ROMs or custom contexts.

---

## 10. Author

**Developed by:** Baat01

**Original idea by:** Kaz

Contact: **Baat01#1245** on Discord

---

## 1. Présentation générale

Le **Run & Bun Randomizer** est un outil complet permettant de générer automatiquement une **box Pokémon prête à jouer**, basée sur un **preset configurable via une interface graphique**.

Conçu pour la ROM **Pokémon Emerald (Run & Bun)**, il automatise la création d’équipes équilibrées pour la pratique de segments spécifiques (Norman & Weather Institute), tout en restant (probablement) **adaptable à d’autres ROMs GBA** avec très peu de modifications.

L’objectif est de permettre aux joueurs de :

- tester le jeu en dehors du truck hell split (aka le vrai jeu)
- jouer avec des box fun et exotiques
- avoir un outil disponible pour playtest plus facilement les hackrom

Tout en ajuster la difficulté et les conditions selon leurs préférences.

---

## 2. Structure du projet

```
/RandomizerLauncher/
│
├── launcher.py                # Interface graphique principale (sélection & édition de preset)
│
├── config/
│   ├── zones.csv              # Liste générique de toutes les zones du jeu
│   ├── contexts.json          # Définit les splits associés à chaque contexte (Norman, Winstitute, etc.)
│   ├── presets/               # Dossiers des configurations de zones
│   │   ├── tryhard.json
│   │   ├── full_random.json
│   │   ├── full_delay.json
│   │   ├── tryhard_winstitute.json
│   │   └── custom1.json
│   └── settings.json          # Contient le dernier preset, la difficulté, la langue et le mode de dupes
│
├── data/
│   ├── dupes_family.json              # Groupes de familles évolutives
│   ├── dupes_regionnal_variant.json   # Gestion des variantes régionales
│   ├── movesets.json                  # Movesets complets par Pokémon
│   ├── static.json                    # Liste des Pokémon statiques
│   ├── magnet_pull.json               # Pokémon avec la capacité Magnet Pull
│   ├── zones.json                     # Données des encounters par zone
│   ├── types.json                     # Types de chaque Pokémon
│
└── scripts/
    ├── randomizer.lua        # Script principal du randomizer
    └── runner.lua            # Chargement des JSON, CSV et initialisation du système

```

---

## 3. Fonctionnement

### Étape 1 – Sélection via le launcher

Le programme `launcher.py` permet :

- de choisir un **preset** (tryhard, full_random, etc.) ;
- de définir la **difficulté** et le **mode de dupes** ;
- et de créer ou modifier de nouveaux presets.

Le preset `full_random` est un cas particulier :

- il ne peut pas être modifié manuellement ;
- seul le **contexte** peut être choisi ;
- les **subzones** sont tirées aléatoirement ;
- toutes les **manipulations** (repel, magnet pull, static) sont désactivées.

---

### Étape 2 – Chargement avec le runner

Le fichier `runner.lua` lit :

- le preset sélectionné ;
- les fichiers de données (`movesets`, `types`, `dupes`, `zones`, etc.) ;
- et construit les structures utilisées par le randomizer.

---

### Étape 3 – Exécution du randomizer

Le fichier `randomizer.lua` contient la logique principale du tirage et de la création des Pokémon.

Toute la génération est centralisée dans une seule fonction :

### `randomizeBox()`

Cette fonction :

1. Lit les zones définies dans le preset ;
2. Tire les Pokémon selon les taux et les règles de dupes ;
3. Applique les movesets correspondants au contexte si il les trouves;
4. Crée automatiquement les Pokémon dans la boîte PC (`setPCBoxMon()`).

---

## 4. Exemple d’utilisation

Dans la console Lua de ton émulateur :

```lua
-- Charger le randomizer
dofile("H:\\Downloads\\Run&Bun\\Randomiser\\scripts\\THIEFSCRIPT.lua")

-- Lancer la randomisation complète
randomizeBox()

```

Sortie typique :

```
===============================================
Initialisation du Randomizer
Preset chargé : tryhard_winstitute
Contexte : Winstitute
Mode de dupes : dupe both
Difficulté : normal
===============================================
Slot 1 → Swampert lv.36 | Nature: Adamant | IVs: 27/22/18/6/25/31
Slot 2 → Altaria lv.34 | Nature: Jolly | IVs: 21/30/17/8/22/25
...
6 Pokémon créés dans le PC

```

---

## 5. Fonctionnalités principales

- **Presets modulaires**
    
    Le système repose sur des presets entièrement configurables, permettant d’adapter la structure des zones et la logique de tirage à différents contextes (Norman, Winstitute, etc.).
    
    Plusieurs modes sont disponibles :
    
    - *Tryhard* : équilibré et compétitif ;
    - *Full Random* : totalement aléatoire, avec subzones tirées au hasard ;
    - *Full Delay* : met l’accent sur les rencontres tardives et les Pokémon surf ;
    - *Custom* : permet de créer ses propres configurations via le launcher.
- **Gestion avancée des doublons**
    
    Le randomizer empêche l’apparition de Pokémon appartenant à la même famille évolutive ou à une variante régionale déjà obtenue.
    
    Le comportement peut être ajusté à l’aide de la **“Regional Variant Dupe Clause”**, offrant trois options :
    
    - *dupe both* : les formes standard et régionales sont liées ;
    - *dupe same name* : seules les formes portant le même nom sont exclues ;
    - *dupe neither* : toutes les formes sont considérées indépendantes.
- **Manipulations de rencontre**
    
    Le système prend en charge plusieurs mécaniques influençant la probabilité d’apparition des Pokémon :
    
    - *Static* : augmente les chances de rencontrer des Pokémon de type Électrik ;
    - *Magnet Pull* : attire les Pokémon de type Acier ;
    - *Repel Manip* : force l’apparition de Pokémon au niveau maximal possible.
        
        Ces effets peuvent être activés ou désactivés selon les paramètres du preset.
        
- **Launcher V1 en Python**
    
    Une interface graphique simple et fonctionnelle, développée en Python avec Tkinter, permet :
    
    - de sélectionner et modifier les presets existants ;
    - de créer de nouveaux presets à partir d’un contexte ;
    - de gérer la difficulté, le mode de dupes et la langue ;
    - d’éditer les zones et sous-zones sans manipuler directement les fichiers JSON ou CSV.

---

## 6. Compatibilité

- ROMs compatibles : **Run&Bun**
- Émulateurs supportés : **Émulateurs supportant les script LUA**
- Langages requis : **Python 3.11+** et **Lua 5.4**

---

## 7. Adaptabilité à d’autres projets

Le **Run & Bun Randomizer** a été conçu pour être **hautement modulaire** et **transposable** vers d’autres ROMs ou projets de randomisation.

### Pour adapter le projet à une autre ROM :

1. **Changer l’adresse mémoire du PC**
    
    Dans `THIEFSCRIPT.lua`, modifie la constante suivante :
    
    ```lua
    PC_BASE = 0x2028848
    
    ```
    
    Cette adresse correspond au premier slot de la boîte PC dans la ROM Emerald.
    
    Remplace-la par l’adresse équivalente dans ta ROM cible (FireRed, Ruby, etc.).
    
2. **Adapter les fonctions Lua**
    
    Ajuste les fonctions `readBoxMon`, `setBoxMon`, et les offsets associés à la structure mémoire de ta ROM 3G.
    
    Ces fonctions définissent comment lire et écrire les données Pokémon stockées.
    
3. **Modifier les fichiers de données**
    
    Mets à jour :
    
    - les fichiers du dossier `data/` (`movesets.json`, `types.json`, `dupes_family.json`, etc.) pour l’adapter à la rom en question;
    - le fichier `config/zones.csv`, en gardant la même structure (`zone,subzone,split`).

En suivant ces trois étapes, le randomizer fonctionnera sur une autre ROM sans nécessiter de changement dans le cœur du programme (`runner.lua` ou `randomizer.lua`).

---

## 8. État actuel du projet

- Script principal de randomizer
    - Fonctionnel
- Runner (data loader)
    - Fonctionnel
- Launcher Graphique
    - Prototype
- Moveset data
    - Fonctionnel
    - En cours de complétion (120/340)
- Encounter manipulation
    - Fonctionnel
- Mécanique de mort
    - Concept
- Documentation
    - En cours
- Launcher responsive, ergonomique et beau
    - Prévu
- Traduction en anglas
    - Prévu

---

## 9. Objectif final

Créer un outil **simple et plug-and-play** permettant de :

- générer une save équilibrée prête à jouer ;
- ajuster librement la difficulté et les règles de dupes ;
- partager des configurations entre plusieurs joueurs ;
- et adapter facilement le moteur à d’autres ROMs et contextes.

---

## 10. Auteur

**Développé par :** Baat01

**Idée originale :** Kaz

Contact : **Baat01#1245** sur Discord

---
