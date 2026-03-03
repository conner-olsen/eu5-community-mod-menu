# CMM Mod Integration

This document is for mod authors integrating with **EU5 Community Mod Menu (CMM)**.

## Scope

- CMM is a shared dependency mod.
- Your mod registers metadata and settings; CMM renders the UI.
- Do not edit CMM core GUI files to add your settings.

## Public API

All calls below are country-scope.

### 1) Register your mod

```txt
cmm_register_mod = {
    mod_id = your_mod_id
}
```

Arguments:

- `mod_id`: stable machine id for ownership.

### 2) Register tabs

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

- `cmm_register_bool_setting` and `cmm_register_numeric_setting` auto-register their tab.
- Use explicit `cmm_register_tab` only when you need an empty tab with no settings yet.

### 3) Register bool settings

```txt
cmm_register_bool_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    default_value = 0 # 0 (off) or 1 (on)
}
```

Arguments:

- `mod_id`: owner mod id.
- `setting_id`: stable id within your mod.
- `tab_id`: owner tab id within your mod.
- `default_value`: initial value for brand-new saves (`0` off, `1` on).

### 4) Register numeric settings

```txt
cmm_register_numeric_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
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
- `default_value`: initial value for brand-new saves.
- `min_value`: minimum allowed value.
- `max_value`: maximum allowed value.
- `step_value`: amount added/removed per button press.

Localization keys are derived automatically from ids:

- Mod title: `<mod_id>_name`
- Mod description: `<mod_id>_desc`
- Tab label: `<mod_id>_<tab_id>_name`
- Setting label: `<mod_id>_<setting_id>_name`
- Setting description: `<mod_id>_<setting_id>_desc`

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

Notes:

- `_on_changed` is also used for row visibility (`is_shown`) checks.
- CMM handles numeric +/- via generic marker scripted GUIs, then executes `_on_changed`.
- If `is_shown` is omitted, the row is visible.
- Checked/value state is read directly from `var:<mod_id>__<setting_id>` by CMM UI.

## Registration Hook Contract

CMM defines and fires a shared custom on_action named `cmm_on_register_country`.

- CMM fires it on game start (after a 1-day delay) and when opening Mod Menu.
- Integrating mods should append their own registration leaf on_actions to this hook.

Pattern:

```txt
cmm_on_register_country = {
    on_actions = {
        your_mod_on_register_country
    }
}

your_mod_on_register_country = {
    effect = {
        your_mod_register_country = yes
    }
}
```

## Data Contract (Runtime Variables)

CMM writes these country-scope variables/lists:

- `cmm_registered_mod_ids` (variable list; registration order)
- `cmm_registered_tab_keys` (variable list of `<mod_id>__<tab_id>`)
- `cmm_registered_setting_keys` (variable list of `<mod_id>__<setting_id>`)
- `cmm_tab_setting_count_<mod_id>__<tab_id>` (count of settings in that tab)
- `<mod_id>_name` (flag value)
- `<mod_id>_desc` (flag value)
- `cmm_tab_owner_mod_id_<mod_id>__<tab_id>` (flag value)
- `<mod_id>__<tab_id>_name` (flag value)
- `cmm_setting_owner_mod_id_<mod_id>__<setting_id>` (flag value)
- `cmm_setting_owner_tab_key_<mod_id>__<setting_id>` (flag value)
- `cmm_setting_min_<mod_id>__<setting_id>` (numeric only)
- `cmm_setting_max_<mod_id>__<setting_id>` (numeric only)
- `cmm_setting_step_<mod_id>__<setting_id>` (numeric only)
- `<mod_id>__<setting_id>_name` (flag value)
- `<mod_id>__<setting_id>_desc` (flag value)
- `<mod_id>__<setting_id>` (setting value)

## Minimal Example (Bool + Numeric)

```txt
your_mod_register_country = {
    cmm_register_mod = {
        mod_id = your_mod
    }

    cmm_register_bool_setting = {
        mod_id = your_mod
        setting_id = allow_feature
        tab_id = general
        default_value = 1
    }

    cmm_register_numeric_setting = {
        mod_id = your_mod
        setting_id = amount
        tab_id = general
        default_value = 10
        min_value = 0
        max_value = 100
        step_value = 5
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

your_mod__amount_on_changed = {
    scope = country
    effect = {
        cmm_apply_numeric_change = {
            setting = your_mod__amount
        }
        # optional custom logic
    }
}
```

## Localization

Define your keys in your own localization file:

```txt
your_mod_name: "Your Mod Name"
your_mod_desc: "One-line description"
your_mod_general_name: "General"
your_mod_allow_feature_name: "Allow Feature"
your_mod_allow_feature_desc: "Enables the feature when checked."
your_mod_amount_name: "Amount"
your_mod_amount_desc: "Numeric amount controlled in CMM."
```

## Notes

- CMM v1 controls currently include bool and numeric only.
- Keep ids stable (`mod_id`, `tab_id`, `setting_id`) across updates.
- Keep integration/API docs in repository docs, not runtime UI localization.
