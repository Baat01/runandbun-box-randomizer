-- =====================================================
-- Runner.lua : charge les fichiers JSON/CSV et prépare le randomizer
-- =====================================================

-- ===== Fonctions utilitaires =====
local function join(...)
  return table.concat({...}, "/")
end

-- ===== JSON support (dkjson) =====
local ok, json = pcall(require, "lib.dkjson-master.dkjson")
if not ok then
  error("Impossible de charger dkjson : " .. tostring(json))
end

-- =====================================================
-- Fonctions génériques de chargement de fichiers
-- =====================================================

local function loadJSON(path)
  local file = io.open(path, "r")
  if not file then error("Fichier introuvable : " .. path) end
  local content = file:read("*a")
  file:close()
  return json.decode(content)
end

local function loadCSV(path)
  local file = io.open(path, "r")
  if not file then error("Fichier introuvable : " .. path) end
  local data = {}
  for line in file:lines() do
    local row = {}
    for value in string.gmatch(line, '([^,]+)') do
      table.insert(row, value)
    end
    table.insert(data, row)
  end
  file:close()
  return data
end

-- =====================================================
-- Chargement des fichiers principaux
-- =====================================================


local root = "H:/Downloads/Run&Bun/Randomiser/"
local configDir = join(root,"config")
local dataDir   = join(root,"data")

print("Chargement des fichiers JSON...")

local settings           = loadJSON(join(configDir, "settings.json"))
local dupesFamily        = loadJSON(join(dataDir, "dupes_family.json"))
local dupesRegional      = loadJSON(join(dataDir, "dupes_regionnal_variant.json"))
local movesetsData       = loadJSON(join(dataDir, "movesets.json"))
local staticUsers        = loadJSON(join(dataDir, "static.json"))
local magnetPullUsers    = loadJSON(join(dataDir, "magnet_pull.json"))
local zonesData          = loadJSON(join(dataDir, "zones.json"))
local typesData          = loadJSON(join(dataDir, "types.json"))

print("Tous les fichiers JSON ont été chargés avec succès.")

-- =====================================================
-- Gestion du preset & des paramètres
-- =====================================================

-- Charger le preset défini dans settings.json
local function loadPreset(presetName)
  local path = join(configDir, "presets", presetName .. ".json")
  local file = io.open(path, "r")
  if not file then
    error("Impossible de charger le preset : " .. path)
  end
  local content = file:read("*a")
  file:close()
  local preset = json.decode(content)
  print("Preset chargé :", preset.name or presetName)
  return preset
end

-- Construire la liste ordonnée des zones à partir du preset
local function buildZoneOrderFromPreset(preset, allZones)
  local orderedZones = {}
  for zoneName, data in pairs(preset.zones) do
    local fullZoneName = zoneName .. " " .. data.subzone
    local zoneData = allZones[fullZoneName]

    if zoneData then
      table.insert(orderedZones, {
        name = fullZoneName,
        repel = data.repel,
        magnet_pull_or_static = data.magnet_pull_or_static,
        zone_number = data.zone_number,
        encounters = zoneData
      })
    else
      print("Zone introuvable dans zones.json :", fullZoneName)
    end
  end
  print(tostring(#orderedZones) .. " zones chargées depuis le preset.")
  return orderedZones
end

-- =====================================================
-- Initialisation du randomizer
-- =====================================================

-- Charger les paramètres utilisateur
local selectedPresetName = settings.last_preset or "tryhard"
local selectedDupesMode  = settings.dupe_mode or "dupe both"
local selectedDifficulty = settings.difficulty or "normal"

print("Paramètres de session :")
print("   Preset :", selectedPresetName)
print("   Mode dupes :", selectedDupesMode)
print("   Difficulté :", selectedDifficulty)

-- Charger le preset et construire les zones
local presetLoaded = loadPreset(selectedPresetName)
local zonesToRoll  = buildZoneOrderFromPreset(presetLoaded, zonesData)

-- =====================================================
-- Exposer les données globales au randomizer
-- =====================================================

GLOBAL_SETTINGS = {
  dupes_mode   = selectedDupesMode,
  difficulty   = selectedDifficulty,
  context      = presetLoaded.context,
  preset_name  = selectedPresetName
}

GLOBAL_DATA = {
  dupes_family        = dupesFamily,
  dupes_regional      = dupesRegional,
  movesets            = movesetsData,
  static_users        = staticUsers,
  magnet_pull_users   = magnetPullUsers,
  zones               = zonesToRoll,
  types               = typesData
}

print("Initialisation complète du runner terminée.")

return {
  settings = GLOBAL_SETTINGS,
  data = GLOBAL_DATA
}
