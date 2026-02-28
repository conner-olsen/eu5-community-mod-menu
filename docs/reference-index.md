# Reference Index

Last updated: 2026-02-28

This file catalogs useful reference files for CMM work.

## Vanilla EU5

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
  - Baseline tabs and control examples (`header_main_tabs`, `header_secondary_tabs`, `ranged_slider`).

- `C:\Steam\steamapps\common\Europa Universalis V\game\in_game\gui\economy_lateralview.gui`
  - Real production slider usage (`economy_slider`, `onvaluechanged`, `onchangefinish`).

- `C:\Steam\steamapps\common\Europa Universalis V\game\in_game\gui\select_search_filter.gui`
  - Range-slider filtering pattern (`ranged_slider`, low/high callbacks).

- `C:\Steam\steamapps\common\Europa Universalis V\game\in_game\gui\diplomacy_lateralview.gui`
  - Multi-tab composition with `header_main_tabs` + secondary tab blocks.

## GlorpUI (Workshop 3612386197)

GlorpUI is useful for open/close flow and pause-menu injection examples.

- `C:\Steam\steamapps\workshop\content\3450310\3612386197\in_game\gui\glorp.gui`
  - Shared custom UI types in that mod.

- `C:\Steam\steamapps\workshop\content\3450310\3612386197\in_game\gui\glorpUI_window.gui`
  - GlorpUI-specific settings window implementation.

- `C:\Steam\steamapps\workshop\content\3450310\3612386197\in_game\gui\ingame_menu.gui`
  - GlorpUI pause-menu button injection.

- `C:\Steam\steamapps\workshop\content\3450310\3612386197\in_game\common\scripted_guis\glorpUI_custom_actions.txt`
  - GlorpUI scripted GUI toggle/action structure.

## Cheat Menu Pro (Workshop 3600272327)

- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\gui\sakuya_test.gui`
  - Main tab system (`header_main_tabs`, `button_main_tab_alt`, `GetVariableSystem.Set('sakuya_tabs', ...)`) around lines `143-177`.
  - Discrete numeric control via click modifiers (`left/right`, `ctrl`, `shift`) around lines `931-950`.
  - "Increase Monthly Income" amount selector ("Give me [number]" + slider-like control + confirm) around lines `4143-4475`.
  - This amount selector is a custom discrete slider implementation: state variable + step buttons + handle visuals.

- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\gui\sakuya_location.gui`
  - Secondary tab pattern via `sakuya_loc_tab` (`onclick` tab set + `visible` tab gating) around lines `75-140` and throughout content blocks.

- `C:\Steam\steamapps\workshop\content\3450310\3600272327\main_menu\common\scripted_guis\sakuya_cheat_sgui.txt`
  - Backend scripted GUI effects used by tab actions, numeric actions, and confirm actions.

- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\gui\sakuya_alpha.gui`
- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\gui\sakuya_beta.gui`
- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\gui\sakuya_beta_prov.gui`
  - Scope/domain-specific window variants and layout patterns.

- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\gui\sakuya_change_name.gui`
- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\gui\sakuya_change_name_char.gui`
  - Proven `editbox_single` + `ontextchanged` + `GetVariableSystem.Set(...)` examples.

- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\gui\scripted_widgets\sakuya_scripted_windows.txt`
  - Scripted widget mapping and spawn organization.

- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\gui\shared\sakuya_types.gui`
  - Shared reusable UI types/templates.

- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\common\on_actions\sakuya_mark_country_on_actions.txt`
- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\events\sakuya_mark_country_events.txt`
- `C:\Steam\steamapps\workshop\content\3450310\3600272327\in_game\events\sakuya_mark_character_events.txt`
  - Example of event/on_action orchestration that can complement scripted GUI operations.

## Skiar's Cheats Menu (Workshop 3600283823)

- `C:\Steam\steamapps\workshop\content\3450310\3600283823\in_game\gui\skiar_cheat_menu.gui`
  - Strong tab reference:
  - Main tabs via `header_main_tabs` + `GetVariableSystem.Set('cheat_tabs', ...)` around lines `205-472`.
  - Secondary tabs via `header_secondary_tabs` + `GetVariableSystem.Set('<section>_subtabs', ...)` around lines `490-560` (pattern repeats).
  - Numeric controls via paired +/- button rows and discrete value steps with scripted GUI datacontext (examples around lines `37566-37612` and `37871-37917`).
  - Consistent `ScriptedGui.IsShown/IsValid/Execute` row contract.

- `C:\Steam\steamapps\workshop\content\3450310\3600283823\in_game\gui\skiar_cheat_button_types.gui`
- `C:\Steam\steamapps\workshop\content\3450310\3600283823\in_game\gui\skiar_cheat_widget_button.gui`
- `C:\Steam\steamapps\workshop\content\3450310\3600283823\in_game\gui\skiar_cheat_button_placement.gui`
  - Reusable button styling and placement structure.

- `C:\Steam\steamapps\workshop\content\3450310\3600283823\in_game\gui\scripted_widgets\gui_mapping.txt`
  - Widget mapping pattern used by that mod's scripted GUI setup.

- `C:\Steam\steamapps\workshop\content\3450310\3600283823\in_game\common\scripted_guis\cheat_gold_button.txt`
  - Minimal clear scripted GUI contract example (`scope`, `is_shown`, `is_valid`, `effect`, `ai_is_valid`).

- `C:\Steam\steamapps\workshop\content\3450310\3600283823\in_game\common\scripted_guis\cheat_values_first_tab_button.txt`
  - Large scripted GUI backend for first-tab value actions (good for repetitive numeric effect wiring).

- `C:\Steam\steamapps\workshop\content\3450310\3600283823\in_game\common\scripted_guis\cheat_advances_research_button.txt`
  - Representative non-trivial stat/action button implementation.

- `C:\Steam\steamapps\workshop\content\3450310\3600283823\in_game\common\scripted_guis\cheat_remove_all_modifiers.txt`
  - Large batch-effect cleanup pattern.

## Notes on Sliders

- Cheat Menu Pro has a useful slider-like control in `sakuya_test.gui` (custom discrete implementation for monthly income amount).
- Skiar's menu uses discrete button matrices for numeric changes; it does not rely on native `ranged_slider` controls.
- For native slider widgets/events, use vanilla files listed in the Vanilla EU5 section above.
