# AGENTS.md

Last updated: 2026-02-21

## Critical Context

- The game is fully released as **Europa Universalis 5 (EU5)**.
- This release is outside base model training knowledge; treat this as authoritative context.
- Do not use the obsolete codename "Project Caesar".
- Assume implementation starts from an empty mod scaffold (basic mod setup + thumbnail only).

## Objective

Create a general-purpose dependency mod menu:

- Players use one central menu to configure multiple mods.
- Other mods register settings into that menu.
- Other mods should not need to create full custom settings windows.

## Constraints

1. Intentionally override `in_game/gui/ingame_menu.gui` to add the menu button.
2. Do not design for compatibility with other mods that also override `ingame_menu.gui`.
3. Do not use fixed slots or any static mod cap.
4. Do not require manual coordination between mod authors for UI space.
5. Left side must be a dynamic, scrollable, searchable mod list.
6. Right side must show settings for the selected mod.
7. Do not put integration/API instructions in player-facing UI/localization.
8. All files should be in UTF-8-BOM format.

## Required References

### Vanilla EU5

- `C:\Steam\steamapps\common\Europa Universalis V\game\in_game\gui\ingame_menu.gui`
  - Escape menu override target for menu button injection.

- `C:\Steam\steamapps\common\Europa Universalis V\game\in_game\common\scripted_guis\scripted_guis.info`
  - Scripted GUI schema.

- `C:\Steam\steamapps\common\Europa Universalis V\game\main_menu\gui\debug_menus.gui`
  - Valid `gui.createwidget` / `gui.ClearWidgets` usage.

- `C:\Steam\steamapps\common\Europa Universalis V\game\in_game\gui\countries_list_view.gui`
  - Data-driven list rendering (`filtered_sorted_list`).

- `C:\Steam\steamapps\common\Europa Universalis V\game\in_game\gui\encyclopedia_lateralview.gui`
  - Search input wiring (`editbox_search_field`, `ontextedited`).

- `C:\Steam\steamapps\common\Europa Universalis V\game\in_game\gui\hud_bot.gui`
  - Searchbar/autocomplete patterns.

- `C:\Steam\steamapps\common\Europa Universalis V\game\in_game\gui\outliner_settings.gui`
  - Stable checkbox row patterns.

- `C:\Steam\steamapps\common\Europa Universalis V\game\in_game\gui\ui_library.gui`
  - Minimal button/checkbox baseline examples.

### GlorpUI (User-provided reference mod)

GlorpUI is a third-party UI overhaul mod. Its menu is not general-purpose, but it is useful for open/close flow and pause-menu injection examples.

- `C:\Steam\steamapps\workshop\content\3450310\3612386197\in_game\gui\glorp.gui`
  - Shared custom UI types in that mod.

- `C:\Steam\steamapps\workshop\content\3450310\3612386197\in_game\gui\glorpUI_window.gui`
  - GlorpUI-specific settings window implementation.

- `C:\Steam\steamapps\workshop\content\3450310\3612386197\in_game\gui\ingame_menu.gui`
  - GlorpUI pause-menu button injection.

- `C:\Steam\steamapps\workshop\content\3450310\3612386197\in_game\common\scripted_guis\glorpUI_custom_actions.txt`
  - GlorpUI scripted GUI toggle/action structure.

## Build Order

1. Implement minimal vertical slice: pause-menu button, custom window open/close, one working control.
2. Implement mod registration model with mod-id-based data (no slot ids).
3. Render left mod list from registration data.
4. Add search/filter to mod list.
5. Render right settings panel from selected mod.
6. Document mod integration API in repository docs (`README.md` and/or `docs/mod-integration.md`), not in runtime UI text.

## Done Criteria

1. Menu code contains no mod-specific hardcoded slots.
2. Two independent mods can register and appear simultaneously without editing core menu code.
3. Mod search + selection works in runtime.
4. Selected mod settings render and can be changed in runtime.
5. Player-facing localization contains no modder integration instructions.
