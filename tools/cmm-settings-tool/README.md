# CMM Settings Tool

Visual editor for creating and managing EU5 Community Mod Menu (CMM) settings integrations.

## Features

- Create and edit all CMM setting types: bool, button, numeric, slider, dropdown, text, and list settings
- Support for both local and global settings
- Live preview styled to match the in-game CMM window
- Real-time generated code view for all output files
- Localization key overview with missing-value highlights
- Import existing mod files for editing
- Export as ZIP or write directly to a mod directory

## Quick Start

### From GitHub (single command)

```bash
pipx run --spec "git+https://github.com/<org>/eu5-community-mod-menu#subdirectory=tools/cmm-settings-tool" cmm-settings-tool
```

### From a cloned repo

```bash
cd tools/cmm-settings-tool
pip install -e .
cmm-settings-tool
```

### Development

```bash
cd tools/cmm-settings-tool
python -m cmm_settings_tool
```

### Options

```
--port PORT    Port to run on (default: 5005)
--host HOST    Host to bind to (default: 127.0.0.1)
--no-open      Don't auto-open browser
```

## Usage

1. **Configure your mod** - Set the Mod ID, name, and description
2. **Add tabs and groups** - Organize your settings into tabs and groups
3. **Add settings** - Create settings of any type with full configuration
4. **Preview** - See how your settings will look in the CMM window
5. **Review code** - Check the generated Paradox script in the Code tab
6. **Download** - Export as a ZIP file or write directly to your mod directory

## Import Existing Mod

Click **Import** and provide the path to your existing mod directory. The tool will parse your registration effects, scripted GUIs, and localization files to reconstruct your settings configuration for editing.

## Generated Files

The tool generates 5 files per mod integration:

| File | Path | Purpose |
|------|------|---------|
| On Action | `in_game/common/on_action/<prefix>_on_action.txt` | CMM registration hook |
| Effects | `in_game/common/scripted_effects/<prefix>_effects.txt` | Setting registrations + text callbacks |
| Scripted GUIs | `in_game/common/scripted_guis/<prefix>_scripted_gui.txt` | Setting change callbacks |
| Localization | `main_menu/localization/english/<prefix>_l_english.yml` | All display strings |
| Metadata | `.metadata/metadata.json` | Mod metadata with CMM dependency |

All `.txt` and `.yml` files are encoded as UTF-8-BOM with CRLF line endings, matching the EU5 modding conventions.

## Requirements

- Python 3.9+
- No external dependencies (uses only Python standard library)
