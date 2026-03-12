# CMM Mod Integration

This document is for mod authors integrating with **EU5 Community Mod Menu (CMM)**.

## Scope

- CMM is a shared dependency mod.
- Your mod registers metadata and settings; CMM renders the UI.
- Do not edit CMM core GUI files to add your settings.

## Public API

All calls below are country-scope.

For normal integrations, you only need to register settings. CMM implicitly registers the owning mod, tab, and group from those calls.

### 1) Optional: register an empty mod

```txt
cmm_register_mod = {
    mod_id = your_mod_id
}
```

Arguments:

- `mod_id`: stable machine id for ownership.

Notes:

- Use explicit `cmm_register_mod` only when you want the mod row to exist before any tabs or settings have been registered.

### 2) Optional: register tabs

```txt
cmm_register_tab = {
    mod_id = your_mod_id
    tab_id = your_tab_id
}
```

Arguments:

- `mod_id`: owner mod id.
- `tab_id`: tab id unique within your mod.

Notes:

- `cmm_register_tab` implicitly registers the owner mod.
- `cmm_register_bool_setting`, `cmm_register_button_setting`, `cmm_register_numeric_setting`, `cmm_register_slider_setting`, `cmm_register_dropdown_setting`, `cmm_register_text_setting`, and their supported `cmm_register_global_*` variants auto-register their tab.
- Use explicit `cmm_register_tab` only when you need an empty tab with no settings yet.

### 3) Optional: register groups

```txt
cmm_register_group = {
    mod_id = your_mod_id
    tab_id = your_tab_id
    group_id = your_group_id
}
```

Arguments:

- `mod_id`: owner mod id.
- `tab_id`: owner tab id within your mod.
- `group_id`: group id unique within your mod.

Notes:

- `cmm_register_group` implicitly registers the owner tab and mod.
- All setting registration APIs auto-register their group. Standard settings use `group_id`; list settings use `setting_id` as their dedicated group key.
- Use explicit `cmm_register_group` only when you need an empty group with no settings yet.
- Groups provide visual structure within a tab: each group renders a header bar and a shared background container for its settings.

### 4) Register bool settings

```txt
cmm_register_bool_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
    default_value = 0 # 0 (off) or 1 (on)
}
```

Arguments:

- `mod_id`: owner mod id.
- `setting_id`: stable id within your mod.
- `tab_id`: owner tab id within your mod.
- `group_id`: owner group id within your mod.
- `default_value`: initial value for brand-new saves (`0` off, `1` on).

Global-storage variant:

```txt
cmm_register_global_bool_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
    default_value = 0
}
```

### 5) Register numeric settings

```txt
cmm_register_numeric_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
    default_value = 10
    min_value = 0
    max_value = 100
    step_value = 5
}
```

Arguments:

- `mod_id`: owner mod id.
- `setting_id`: stable id within your mod.
- `tab_id`: owner tab id within your mod.
- `group_id`: owner group id within your mod.
- `default_value`: initial value for brand-new saves.
- `min_value`: minimum allowed value.
- `max_value`: maximum allowed value.
- `step_value`: amount added/removed per button press.
  - CMM numeric controls support modifiers:
    - Click: `1x` step.
    - `Ctrl+click`: `5x` step.
    - `Shift+click`: jump to min/max.

Global-storage variant:

```txt
cmm_register_global_numeric_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
    default_value = 10
    min_value = 0
    max_value = 100
    step_value = 5
}
```

### 6) Register slider settings

```txt
cmm_register_slider_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
    default_value = 50
    min_value = 0
    max_value = 100
    step_value = 10
}
```

Arguments:

- `mod_id`: owner mod id.
- `setting_id`: stable id within your mod.
- `tab_id`: owner tab id within your mod.
- `group_id`: owner group id within your mod.
- `default_value`: initial value for brand-new saves. CMM quantizes slider values to the nearest configured step.
- `min_value`: minimum allowed value.
- `max_value`: maximum allowed value.
- `step_value`: logical slider interval.
  - Track clicks select the nearest slider position.
  - Click on `-` / `+`: `1x` step.
  - `Ctrl+click` on `-` / `+`: `5x` step.
  - `Shift+click` on `-` / `+`: jump to min/max.
  - Slider tracks render up to 25 visual slots. Above that, track clicks snap to the nearest visual slot while `-` / `+` still use exact step math.

Global-storage variant:

```txt
cmm_register_global_slider_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
    default_value = 50
    min_value = 0
    max_value = 100
    step_value = 10
}
```

### 7) Register dropdown settings

```txt
cmm_register_dropdown_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
    default_index = 1
    option_count = 3
}
```

Arguments:

- `mod_id`: owner mod id.
- `setting_id`: stable id within your mod.
- `tab_id`: owner tab id within your mod.
- `group_id`: owner group id within your mod.
- `default_index`: initial selected option index for brand-new saves.
- `option_count`: number of options (`>= 1`). Options are indexed `0..option_count-1`.
  - CMM dropdown controls support modifiers:
    - Click on `<` / `>`: previous/next option.
    - `Shift+click` on `<` / `>`: jump to first/last option.

Global-storage variant:

```txt
cmm_register_global_dropdown_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
    default_index = 1
    option_count = 3
}
```

### 8) Register button settings

```txt
cmm_register_button_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
}
```

Arguments:

- `mod_id`: owner mod id.
- `setting_id`: stable id within your mod.
- `tab_id`: owner tab id within your mod.
- `group_id`: owner group id within your mod.

Global edit-permission variant:

```txt
cmm_register_global_button_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
}
```

Notes:

- Button settings are stateless. CMM does not create or mutate `<mod_id>__<setting_id>` for them.
- Button rows use `<mod_id>__<setting_id>_name` for the setting label and `<mod_id>__<setting_id>_button` for the clickable button caption.
- `cmm_register_global_button_setting` only marks the button as host-editable in multiplayer. It does not create stored value state.

### 9) Register text settings

```txt
cmm_register_text_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    group_id = your_group_id
    character_limit = 42
    quote_text = 1
}
```

Arguments:

- `mod_id`: owner mod id.
- `setting_id`: stable id within your mod.
- `tab_id`: owner tab id within your mod.
- `group_id`: owner group id within your mod.
- `character_limit`: maximum number of characters allowed in the editbox. Values below `1` are clamped to `1`.
- `quote_text`: `1` wraps submitted text in double quotes before CMM passes it to your effect; `0` forwards the raw editbox text unchanged.

Notes:

- Text settings are singleplayer-only. CMM disables them in multiplayer because `ExecuteConsoleCommand` cannot apply effect-backed text submissions there.
- CMM does not persist text values. The editbox content lives only in the live GUI widget.
- CMM does not validate or escape submitted text for you.
- When `quote_text = 0`, your effect must expect an unquoted token. CMM will not sanitize spaces or script syntax for you.
- There is no `cmm_register_global_text_setting`.

### 10) Register list settings

```txt
cmm_register_settings_list = {
    mod_id = your_mod_id
    setting_id = build_priority
    tab_id = general
    item_count = 5
    is_ordered = 1
}

cmm_register_list_bool_field = {
    mod_id = your_mod_id
    setting_id = build_priority
    field_id = enabled
    default_value = 1
}

cmm_register_list_dropdown_field = {
    mod_id = your_mod_id
    setting_id = build_priority
    field_id = mode
    default_index = 1
    option_count = 3
}

cmm_register_list_numeric_field = {
    mod_id = your_mod_id
    setting_id = build_priority
    field_id = weight
    default_value = 5
    min_value = 0
    max_value = 10
    step_value = 1
}
```

Arguments:

- `mod_id`: owner mod id.
- `setting_id`: stable id within your mod.
- `tab_id`: owner tab id within your mod.
- `item_count`: number of list items. CMM clamps values into `1..20`.
- `is_ordered`: `1` shows row move controls, `0` hides them.
- `field_id`: stable per-list field id unique within the list setting.
- `default_value`: initial bool-field value for brand-new saves (`0` or `1`).
- `default_index`: initial dropdown-field option index for brand-new saves.
- `option_count`: number of dropdown options (`>= 1`).
- `default_value` (numeric field): initial numeric-field value for brand-new saves.
- `min_value`: numeric-field minimum allowed value.
- `max_value`: numeric-field maximum allowed value.
- `step_value`: numeric-field increase/decrease step size.

Notes:

- List settings are local country-scope only in CMM v1. There is no global list-setting API.
- Register the list first, then register its fields.
- `cmm_register_settings_list` supports both ordered and unordered lists through `is_ordered`.
- `cmm_register_list_bool_field`, `cmm_register_list_dropdown_field`, and `cmm_register_list_numeric_field` work the same for both list variants.
- Each list setting creates and owns a dedicated group keyed by `setting_id`. You do not pass `group_id` and you do not need a separate `cmm_register_group` call for that list.
- The dedicated group header uses `<mod_id>__<setting_id>_name`, so the list widget itself does not render a second title line inside that group.
- Each list may register up to 5 fields total.
- Field columns render left-to-right in registration order.
- Bool fields render as checkboxes.
- Dropdown fields render as compact dropdowns.
- Numeric fields render as compact steppers.
- Numeric list-field controls match standard numeric setting behavior:
  - Click `-` / `+`: `1x` step.
  - `Ctrl+click` `-` / `+`: `5x` step.
  - `Shift+click` `-` / `+`: jump to min/max.
- `Shift+click` the numeric value box to apply that row's current numeric value to all rows in the same field.
- `Shift+click` the closed dropdown control to apply that row's current dropdown value to all rows in the same field.
- Ordered list rows additionally support:
  - Click up/down: move one row.
  - `Shift+click` up/down: move to top/bottom.
- Unordered lists keep the same runtime item sequence but do not expose row move controls in CMM UI.

Runtime data shape:

- Row sequence is stored in `cmm_list_items_<mod_id>__<setting_id>`.
- Stable item identity keys are `flag:<mod_id>__<setting_id>_item_<index>`.
- Per-item field values are stored on the stable item identity, not on the visible row position:
  - `<mod_id>__<setting_id>_item_<index>_field_0`
  - `<mod_id>__<setting_id>_item_<index>_field_1`
  - ...
- When iterating your list in script, compare the current list entry against `flag:<mod_id>__<setting_id>_item_<index>` to identify which item you are handling.

Localization keys are derived automatically from ids:

- Mod title: `<mod_id>_name`
- Mod description: `<mod_id>_desc`
- Tab label: `<mod_id>__<tab_id>_name`
- Group label: `<mod_id>__<group_id>_name`
- Setting label: `<mod_id>__<setting_id>_name`
- Setting description: `<mod_id>__<setting_id>_desc`
- Button setting text: `<mod_id>__<setting_id>_button`
- Dropdown options: `<mod_id>__<setting_id>_option_<index>_name`
- List item column label: `<mod_id>__<setting_id>_item_column_name`
- List item labels: `<mod_id>__<setting_id>_item_<index>_name`
- List field labels: `<mod_id>__<setting_id>__<field_id>_name`
- List dropdown options: `<mod_id>__<setting_id>__<field_id>_option_<index>_name`

## Callback Contract

CMM resolves callbacks by naming convention from `<mod_id>__<setting_id>`.

### Bool setting callbacks

Required scripted GUI callback:

```txt
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        cmm_toggle_bool_setting = {
            setting = <mod_id>__<setting_id>
        }
        # optional custom logic
    }
    # optional is_shown = { ... }
}
```

### Button setting callbacks

Required scripted GUI callback:

```txt
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        # custom action logic
    }
    # optional is_shown = { ... }
}
```

### Numeric setting callbacks

Required scripted GUI callback:

```txt
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
```

### Slider setting callbacks

Required scripted GUI callback:

```txt
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
```

### Dropdown setting callbacks

Required scripted GUI callback:

```txt
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        cmm_apply_dropdown_change = {
            setting = <mod_id>__<setting_id>
        }
        # optional custom logic after dropdown value changes
    }
    # optional is_shown = { ... }
}
```

### List setting callbacks

Required scripted GUI callback:

```txt
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        cmm_apply_list_change = {
            setting = <mod_id>__<setting_id>
        }
        # optional custom logic after order or field values change
    }
    # optional is_shown = { ... }
}
```

### Text setting callbacks

Required scripted effect:

```txt
<mod_id>__<setting_id>_on_changed = {
    # country scope via `effect c:<player_tag> = { ... }`
    # `text` is the submitted editbox content.
    # If `quote_text = 1`, CMM wraps it in double quotes before calling this effect.
    change_country_name = $text$
}
```

Notes:

- Non-text `_on_changed` callbacks are also used for row visibility (`is_shown`) checks.
- Button settings execute `_on_changed` directly on click.
- CMM handles numeric modes (`1x`, `5x`, `min/max`) via generic marker scripted GUIs, then executes `_on_changed`.
- CMM handles slider track clicks and `-` / `+` modifiers via generic marker scripted GUIs, then executes `_on_changed`.
- CMM captures dropdown selection index via a generic marker scripted GUI, then executes `_on_changed`.
- CMM captures list row position and field action via generic marker scripted GUIs, then executes `_on_changed`.
- Ordered lists additionally capture row move actions through that same list callback.
- If `is_shown` is omitted, the row is visible.
- Local bool, numeric, slider, and dropdown checked/value state is read from `var:<mod_id>__<setting_id>` by CMM UI.
- Global bool, numeric, slider, and dropdown checked/value state is read from `GetGlobalVariable(<mod_id>__<setting_id>)` by CMM UI.
- Global settings (`cmm_register_global_*`) are writable by host only in multiplayer (`IsHost`); all players can view them.
- Core CMM can additionally lock global settings behind its `Enable Host-Only Tools` toggle. The built-in toggle itself remains editable so the gate can be turned back on.
- Callback contract is unchanged for local vs global settings; `cmm_toggle_bool_setting`, `cmm_apply_numeric_change`, `cmm_apply_slider_change`, and `cmm_apply_dropdown_change` branch automatically.
- If your callback also reads the current setting value for custom logic, use `var:<mod_id>__<setting_id>` for local settings and `global_var:<mod_id>__<setting_id>` for global settings.
- Global button settings are writable by host only in multiplayer, but they do not create stored value state.
- Text settings do not currently use scripted GUI `_on_changed` callbacks or `is_shown` gating. Their submit path calls the scripted effect directly through `ExecuteConsoleCommand`.
- Text setting effects must actually reference `$text$`. If they do not, the engine treats the scripted effect as argument-free and rejects the CMM call.

## Registration Hook Contract

CMM defines and fires a shared custom on_action named `cmm_on_mod_registration`.

- CMM fires it on game start (after a 1-day delay) and when opening Mod Menu.
- Integrating mods should append their own registration leaf on_actions to this hook.

Pattern:

```txt
cmm_on_mod_registration = {
    on_actions = {
        your_mod_on_register_mod
    }
}

your_mod_on_register_mod = {
    effect = {
        your_mod_register_mod = yes
    }
}
```

## Built-in Host Marker

CMM also provides a country-scope scripted trigger named `is_host`.

```txt
is_host = {
    # scope = country
}
```

Notes:

- `is_host` is gated by CMM's core `Enable Host-Only Tools` toggle. If that toggle is off, `is_host` is false in both singleplayer and multiplayer.
- When the toggle is on and `has_multiple_players = no`, `is_host` is true for the current human country.
- When the toggle is on and `has_multiple_players = yes`, `is_host` reflects CMM's stored host-country marker in multiplayer, not a native engine host query.
- CMM updates that multiplayer host-country marker automatically when the actual multiplayer host opens Mod Menu.

## Data Contract (Runtime Variables)

CMM writes these country-scope variables/lists:

- `cmm_registered_mod_ids` (variable list; registration order)
- `cmm_registered_tab_keys` (variable list of `<mod_id>__<tab_id>`)
- `cmm_registered_group_keys` (variable list of `<mod_id>__<group_id>`)
- `cmm_registered_setting_keys` (variable list of `<mod_id>__<setting_id>`)
- `cmm_tab_setting_count_<mod_id>__<tab_id>` (count of settings in that tab)
- `cmm_group_setting_keys_<mod_id>__<group_id>` (variable list of setting keys in that group)
- `<mod_id>_name` (flag value)
- `<mod_id>_desc` (flag value)
- `cmm_tab_owner_mod_id_<mod_id>__<tab_id>` (flag value)
- `<mod_id>__<tab_id>_name` (flag value)
- `cmm_group_owner_mod_id_<mod_id>__<group_id>` (flag value)
- `cmm_group_owner_tab_key_<mod_id>__<group_id>` (flag value)
- `<mod_id>__<group_id>_name` (flag value)
- `cmm_setting_owner_mod_id_<mod_id>__<setting_id>` (flag value)
- `cmm_setting_owner_tab_key_<mod_id>__<setting_id>` (flag value)
- `cmm_setting_owner_group_key_<mod_id>__<setting_id>` (flag value)
- `cmm_setting_is_global_<mod_id>__<setting_id>` (`0` local country setting, `1` global setting)
- `cmm_setting_is_slider_<mod_id>__<setting_id>` (`0` non-slider, `1` slider)
- `cmm_setting_is_button_<mod_id>__<setting_id>` (`0` non-button, `1` button)
- `cmm_setting_min_<mod_id>__<setting_id>` (numeric and slider)
- `cmm_setting_max_<mod_id>__<setting_id>` (numeric and slider)
- `cmm_setting_step_<mod_id>__<setting_id>` (numeric and slider)
- `cmm_setting_slider_actual_step_count_<mod_id>__<setting_id>` (slider only)
- `cmm_setting_slider_actual_last_index_<mod_id>__<setting_id>` (slider only)
- `cmm_setting_slider_visual_step_count_<mod_id>__<setting_id>` (slider only)
- `cmm_setting_slider_visual_last_index_<mod_id>__<setting_id>` (slider only)
- `cmm_setting_dropdown_count_<mod_id>__<setting_id>` (dropdown only)
- `cmm_setting_dropdown_last_index_<mod_id>__<setting_id>` (dropdown only)
- `cmm_setting_list_count_<mod_id>__<setting_id>` (list only)
- `cmm_setting_list_is_ordered_<mod_id>__<setting_id>` (list only; `1` ordered, `0` unordered)
- `cmm_setting_list_last_index_<mod_id>__<setting_id>` (list only)
- `cmm_list_items_<mod_id>__<setting_id>` (list-only variable list of stable item keys)
- `cmm_list_field_count_<mod_id>__<setting_id>` (list only)
- `cmm_list_field_<slot>_type_<mod_id>__<setting_id>` (list only; `1` bool, `2` dropdown)
- `cmm_list_field_<slot>_name_<mod_id>__<setting_id>` (list only; flag value)
- `cmm_list_field_<slot>_option_root_<mod_id>__<setting_id>` (list only; flag value for list dropdown localization)
- `cmm_list_field_<slot>_dropdown_count_<mod_id>__<setting_id>` (list dropdown fields only)
- `cmm_list_field_<slot>_dropdown_last_index_<mod_id>__<setting_id>` (list dropdown fields only)
- `cmm_list_item_owner_setting_<mod_id>__<setting_id>_item_<index>` (list only; flag value)
- `<mod_id>__<setting_id>_item_<index>_name` (list only; flag value)
- `<mod_id>__<setting_id>_item_<index>_field_<slot>` (list only; per-item field value)
- `cmm_setting_text_character_limit_<mod_id>__<setting_id>` (text only)
- `cmm_setting_text_quote_<mod_id>__<setting_id>` (text only)
- `<mod_id>__<setting_id>_name` (flag value)
- `<mod_id>__<setting_id>_desc` (flag value)
- `<mod_id>__<setting_id>_button` (flag value; button only)
- local `<mod_id>__<setting_id>` (country-scope value for local bool, numeric, slider, and dropdown settings)
- global `<mod_id>__<setting_id>` (global-scope value for global bool, numeric, slider, and dropdown settings; read directly by CMM UI)
- global `cmm_core__enable_host_only_tools` (bool gate controlling whether host-only settings and `is_host`-gated tools are enabled)
- global `cmm_core_host_country` (country reference used by CMM's multiplayer host marker and multiplayer `is_host` checks)

## Minimal Example (Bool + Button + Numeric + Slider + Dropdown + Text)

```txt
your_mod_register_mod = {
    cmm_register_bool_setting = {
        mod_id = your_mod
        setting_id = allow_feature
        tab_id = general
        group_id = general
        default_value = 1
    }

    cmm_register_button_setting = {
        mod_id = your_mod
        setting_id = run_feature
        tab_id = general
        group_id = general
    }

    cmm_register_numeric_setting = {
        mod_id = your_mod
        setting_id = amount
        tab_id = general
        group_id = general
        default_value = 10
        min_value = 0
        max_value = 100
        step_value = 5
    }

    cmm_register_slider_setting = {
        mod_id = your_mod
        setting_id = intensity
        tab_id = general
        group_id = general
        default_value = 50
        min_value = 0
        max_value = 100
        step_value = 10
    }

    cmm_register_dropdown_setting = {
        mod_id = your_mod
        setting_id = mode
        tab_id = general
        group_id = general
        default_index = 1
        option_count = 3
    }

    cmm_register_text_setting = {
        mod_id = your_mod
        setting_id = country_name
        tab_id = general
        group_id = general
        character_limit = 42
        quote_text = 1
    }
}

your_mod__allow_feature_on_changed = {
    scope = country
    effect = {
        cmm_toggle_bool_setting = {
            setting = your_mod__allow_feature
        }
    }
}

your_mod__run_feature_on_changed = {
    scope = country
    effect = {
        # custom action logic
    }
}

your_mod__amount_on_changed = {
    scope = country
    effect = {
        cmm_apply_numeric_change = {
            setting = your_mod__amount
        }
        # optional custom logic
    }
}

your_mod__intensity_on_changed = {
    scope = country
    effect = {
        cmm_apply_slider_change = {
            setting = your_mod__intensity
        }
        # optional custom logic
    }
}

your_mod__mode_on_changed = {
    scope = country
    effect = {
        cmm_apply_dropdown_change = {
            setting = your_mod__mode
        }
        # optional custom logic
    }
}

your_mod__country_name_on_changed = {
    change_country_name = $text$
}
```

## Localization

Define your keys in your own localization file:

```txt
your_mod_name: "Your Mod Name"
your_mod__general_name: "General" # used for both tab and group label
your_mod__allow_feature_name: "Allow Feature"
your_mod__allow_feature_desc: "Enables the feature when checked."
your_mod__run_feature_name: "Run Feature"
your_mod__run_feature_button: "Run"
your_mod__run_feature_desc: "Runs the feature when pressed."
your_mod__amount_name: "Amount"
your_mod__amount_desc: "Numeric amount controlled in CMM."
your_mod__intensity_name: "Intensity"
your_mod__intensity_desc: "Slider amount controlled in CMM."
your_mod__mode_name: "Mode"
your_mod__mode_desc: "Dropdown mode controlled in CMM."
your_mod__mode_option_0_name: "Off"
your_mod__mode_option_1_name: "Standard"
your_mod__mode_option_2_name: "Aggressive"
your_mod__country_name_name: "Country Name"
your_mod__country_name_desc: "Singleplayer-only text setting. Applies the entered name on submit."
```

## Notes

- CMM v1 controls currently include bool, button, numeric, slider, dropdown, text, and list settings (`ordered` or `unordered`).
- Keep ids stable (`mod_id`, `tab_id`, `group_id`, `setting_id`) across updates.
- Keep integration/API docs in repository docs, not runtime UI localization.
