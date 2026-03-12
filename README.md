# EU5 Community Mod Menu (CMM)

A dependency mod for **Europa Universalis 5** that provides one shared in-game mod settings window.

## What it provides

- Pause menu button (`Mod Menu`) via intentional `ingame_menu.gui` override.
- Dynamic left mod list (search + compact rendering).
- Dynamic right settings panel for registered bool, button, numeric, slider, dropdown, text, and list settings.
- Dynamic per-mod tabs in the right panel.
- Mod-id-based registration API with no fixed slot cap.
- GUI function macro layer for shared CMM data-binding expressions (`loading_screen/data_binding/cmm_macros.txt` plus split descriptive companion files such as `cmm_macros_view.txt`, `cmm_macros_settings.txt`, and `cmm_macros_list.txt`).

## Current settings scope (v1)

- Bool settings (`0`/`1`) with checkbox controls.
- Button settings with action buttons.
  - Click button: execute the setting-specific `_on_changed` effect immediately.
- Numeric settings with stepper controls (`-` / `+`).
  - Click: `1x` step.
  - `Ctrl+click`: `5x` step.
  - `Shift+click`: jump to min/max.
- Slider settings with pseudo-slider controls.
  - Click track: jump to the selected slider position.
  - Click `-` / `+`: `1x` step.
  - `Ctrl+click` on `-` / `+`: `5x` step.
  - `Shift+click` on `-` / `+`: jump to min/max.
- Dropdown settings with selector controls (`<` / `>`).
  - Click: previous/next option.
  - `Shift+click`: jump to first/last option.
- List settings with configurable field columns.
  - Ordered lists expose per-item move controls (`click` up/down = move one row, `Shift+click` = move to top/bottom).
  - Unordered lists reuse the same fields without row move controls.
  - Bool fields: checkbox toggle.
  - Dropdown fields: click next, `Shift+click` previous.
- Text settings with single-line editboxes and an `Apply` action.
  - Click `Apply` or press `Enter`: submit the current text through a console-backed effect call.
  - `quote_text = 1` wraps the submitted text in double quotes before CMM passes it to the callback.
- `quote_text = 0` forwards the raw text unchanged; use it only when your effect expects an unquoted token.
- Text settings are singleplayer-only and are not persisted by CMM.
- Registration order is preserved.
- Local bool, numeric, slider, and dropdown value changes are persisted as country variables.
- Global bool, numeric, slider, and dropdown value changes are persisted as global variables and read directly from global scope in UI.
- UI invokes per-setting callbacks immediately on interaction.

## Install

1. Place this folder in `Documents\Paradox Interactive\Europa Universalis V\mod`.
2. Enable `community.mod.menu.dev` (and any integrating mod) in the launcher.

## Integration API summary

Country scope:

```txt
cmm_register_mod = {
    mod_id = your_mod_id
}

cmm_register_bool_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    default_value = 0 # required; 0 (off) or 1 (on)
}

cmm_register_button_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
}

cmm_register_numeric_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    default_value = 10 # required
    min_value = 0      # required
    max_value = 100    # required
    step_value = 5     # required
}

cmm_register_slider_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    default_value = 50 # required
    min_value = 0      # required
    max_value = 100    # required
    step_value = 10    # required
}

cmm_register_dropdown_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    default_index = 1 # required
    option_count = 3  # required; >= 1 (options are 0..option_count-1)
}

cmm_register_text_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    character_limit = 42 # required; >= 1
    quote_text = 1       # required; 1 = wrap in double quotes, 0 = pass raw text
}

cmm_register_settings_list = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    item_count = 5 # required; 1..20
    is_ordered = 1 # required; 1 = ordered, 0 = unordered
}

cmm_register_list_bool_field = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    field_id = enabled
    default_value = 1 # required
}

cmm_register_list_dropdown_field = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    field_id = mode
    default_index = 1 # required
    option_count = 3  # required; >= 1
}
```

Global variants also exist for bool, button, numeric, slider, and dropdown settings. `cmm_register_global_button_setting` only affects host-only multiplayer edit permission and does not create stored value state. Core CMM can additionally lock all global settings behind its `Enable Host-Only Tools` toggle.

CMM also ships a country-scope scripted trigger named `is_host`. It only becomes true when CMM's core `Enable Host-Only Tools` toggle is on, and then resolves to the current human country whenever `has_multiple_players = no`, or to the country last auto-marked by the actual multiplayer host when they opened Mod Menu.

Localization key format is enforced by ids:

- Mod: `<mod_id>_name`, `<mod_id>_desc`
- Tab: `<mod_id>__<tab_id>_name`
- Setting: `<mod_id>__<setting_id>_name`, `<mod_id>__<setting_id>_desc`
- Button setting text: `<mod_id>__<setting_id>_button`
- Dropdown option: `<mod_id>__<setting_id>_option_<index>_name`
- List item: `<mod_id>__<setting_id>_item_<index>_name`
- List field: `<mod_id>__<setting_id>__<field_id>_name`
- List field dropdown option: `<mod_id>__<setting_id>__<field_id>_option_<index>_name`

Callback contract:

```txt
# Bool setting callback (required):
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        cmm_toggle_bool_setting = {
            setting = <mod_id>__<setting_id>
        }
    }
}

# Button setting callback (required):
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        # custom action logic
    }
    # optional is_shown = { ... }
}

# Numeric shared callback (required; executed after + / -):
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        cmm_apply_numeric_change = {
            setting = <mod_id>__<setting_id>
        }
        # optional custom logic after numeric value changes
    }
    # optional is_shown = { ... }
}

# Slider shared callback (required; executed after track click or +/-):
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        cmm_apply_slider_change = {
            setting = <mod_id>__<setting_id>
        }
        # optional custom logic after slider value changes
    }
    # optional is_shown = { ... }
}

# Dropdown shared callback (required; executed after < / >):
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        cmm_apply_dropdown_change = {
            setting = <mod_id>__<setting_id>
        }
    }
}

# List shared callback (required; executed after field interaction and ordered-list row moves):
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        cmm_apply_list_change = {
            setting = <mod_id>__<setting_id>
        }
    }
}

# Text callback (required; define in scripted_effects, not scripted_guis):
<mod_id>__<setting_id>_on_changed = {
    # country scope via `effect c:<player_tag> = { ... }`
    # `text` is the submitted editbox content.
    # If `quote_text = 1`, CMM wraps it in double quotes before calling this effect.
    change_country_name = $text$
}
```

CMM handles numeric, slider, dropdown, and list change modes through generic marker scripted GUIs and then executes the setting-specific `_on_changed`. Ordered lists additionally expose row move actions through that same list callback. Button settings execute `_on_changed` directly on click. Text settings submit through `ExecuteConsoleCommand`, so they are disabled in multiplayer and currently do not use scripted GUI `is_shown` gating.

Registration hook contract:

```txt
cmm_on_mod_registration = {
    on_actions = { your_mod_on_register_mod }
}
```

Full integration docs: `docs/mod-integration.md`.

## License

GPL-3.0. See `LICENSE`.
