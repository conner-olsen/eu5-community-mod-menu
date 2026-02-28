# AGENTS.md

Last updated: 2026-02-28

## Critical Context

- The game is fully released as **Europa Universalis 5 (EU5)**.
- Do not use the obsolete codename "Project Caesar".
- Treat this file as the operating brief for current CMM work.
- CMM is not released yet; breaking changes are allowed.
- Do not add backward-compatibility or migration shims unless explicitly requested.

## Objective

Maintain CMM as a general-purpose dependency mod menu:

- Players use one shared settings menu for multiple mods.
- Mod authors register settings into CMM dynamically.
- Mod authors should not need to build a full custom settings window for basic controls.

## Current Implementation State (Authoritative)

Implemented:

1. Pause-menu button injection and open/close flow are working (`ingame_menu.gui` + `cmm_window.gui`).
2. Dynamic mod registration is working via `cmm_register_mod`.
3. Dynamic bool setting registration is working via `cmm_register_bool_setting`.
4. Left panel is dynamic, scrollable, searchable, and physically compacts filtered results.
5. Right panel renders selected-mod metadata and dynamic setting rows.
6. Checkbox toggles are wired through scripted GUI callbacks (`<mod_id>__<setting_id>_on_changed`) and `cmm_toggle_bool_setting`.
7. Shared registration hook `cmm_on_register_country` is in place and used by example mods.
8. Runtime localization keys are derived from ids (no extra registration args for names/descriptions).
9. Dynamic per-mod tabs are implemented in the right panel.
10. Bool settings are filtered by both selected mod and selected tab.

Remaining:

1. Add non-bool controls (numeric/slider/dropdown/text) and define stable API.
2. Finalize list ordering policy (registration-first vs optional alpha mode).
3. Expand docs/examples after non-bool controls exist.

## Constraints

1. Intentionally override `in_game/gui/ingame_menu.gui` to add the menu button.
2. Do not design for compatibility with other mods that also override `ingame_menu.gui`.
3. Do not use fixed slots or any static mod cap.
4. Do not require manual coordination between mod authors for UI space.
5. Left side must remain dynamic and searchable.
6. Right side must remain dynamic and selected-mod scoped.
7. Keep integration/API instructions in repository docs, not player-facing runtime UI/localization.
8. All touched `.gui`, `.txt`, and `.yml` files must be UTF-8-BOM.
9. Use `CMM` naming prefix for core menu systems.
10. Right panel must support dynamic per-mod tabs (no fixed tab count).

## Script Doc Comment Style

Use this comment format for core CMM script files (`in_game/common/*` in this repository), excluding example mods unless explicitly requested.

Standard form:

```txt
# Short Description
# Scope: [scope]
# Args: [arg1] ([arg1type]), [arg2] ([arg2type]), ...
```

Expanded args form (when args are not self-explanatory):

```txt
# Short Description
# Scope: [scope]
# Args:
# - [arg1] ([arg1type]): [arg1shortdesc]
# - [arg2] ([arg2type]): [arg2shortdesc]
```

Additional rules:

- Use `# Args: none` when there are no arguments.
- Place the doc comment immediately above the target scripted object.
- Keep comments concise and implementation-accurate.

## Core File Map

- `in_game/gui/ingame_menu.gui`
- `in_game/gui/cmm_window.gui`
- `in_game/common/scripted_effects/cmm_effects.txt`
- `in_game/common/scripted_guis/cmm_scripted_gui.txt`
- `in_game/common/on_action/cmm_on_action.txt`
- `in_game/common/scripted_triggers/cmm_triggers.txt`
- `docs/mod-integration.md`
- `README.md`

## Integration Contract (Current v1)

Country-scope API:

```txt
cmm_register_mod = {
    mod_id = <required>
}

cmm_register_tab = {
    mod_id = <required>
    tab_id = <required>
}

cmm_register_bool_setting = {
    mod_id = <required>
    setting_id = <required>
    tab_id = <required>
    default_value = <required, 0|1>
}
```

Derived localization keys:

- Mod name: `<mod_id>_name`
- Mod description: `<mod_id>_desc`
- Tab label: `<mod_id>_<tab_id>_name`
- Setting name: `<mod_id>_<setting_id>_name`
- Setting description: `<mod_id>_<setting_id>_desc`

Required scripted GUI callback per bool setting:

```txt
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        cmm_toggle_bool_setting = {
            setting = <mod_id>__<setting_id>
        }
        # optional custom logic
    }
    # optional is_shown = { ... } for row visibility
}
```

## Registration Lifecycle

- CMM fires shared custom on_action `cmm_on_register_country`.
- Integrating mods append their own leaf on_actions under that hook.
- CMM invokes registration on:
  - startup synchronization,
  - periodic human-country sync,
  - menu-open path.

## Tabs (Implemented)

Behavior:

1. Tabs are registered dynamically via `cmm_register_tab` and/or implicitly via `cmm_register_bool_setting`.
2. Right panel renders tabs from `cmm_registered_tab_keys`, filtered to selected mod.
3. Clicking a mod row sets selected mod and selected tab default (`cmm_mod_default_tab_<mod_id>`).
4. Clicking a tab sets `cmm_selected_tab`.
5. Settings rows are visible only when:
   - owner mod matches selected mod,
   - owner tab matches selected tab,
   - optional per-setting scripted GUI `is_shown` evaluates true.
6. Empty-state text for settings is tab-scoped (no settings in selected tab).

Verification:

1. A mod can register multiple tabs and settings appear only in selected tab.
2. Switching selected mod sets selected tab to that mod's default tab.
3. No hardcoded tab slots/caps in GUI/effects.
4. No parser/log errors from tab metadata resolution.

Reference focus for this milestone:

- `docs/reference-index.md` -> Cheat Menu Pro section (`sakuya_test.gui`, `sakuya_location.gui`) for tab and slider-like control patterns.
- `docs/reference-index.md` -> Skiar's Cheats Menu section (`skiar_cheat_menu.gui`) for main+secondary tab composition and large numeric row patterns.

## Acceptance Criteria (Release-Level)

1. No mod-specific hardcoded UI slots/caps in CMM.
2. Independent mods can register concurrently without editing CMM core code.
3. Mod search + selection works in runtime.
4. Selected mod settings render and apply in runtime.
5. Player-facing localization contains no integration instructions.

## Helpful References

- Reference catalog: `docs/reference-index.md`
