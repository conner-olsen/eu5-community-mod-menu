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

### 2) Register boolean settings

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

Optional explicit tab registration (only needed if you want an empty tab with no settings yet):

```txt
cmm_register_tab = {
    mod_id = your_mod_id
    tab_id = your_tab_id
}
```

Localization keys are derived automatically from ids:

- Mod title: `<mod_id>_name`
- Mod description: `<mod_id>_desc`
- Tab label: `<mod_id>_<tab_id>_name`
- Setting label: `<mod_id>_<setting_id>_name`
- Setting description: `<mod_id>_<setting_id>_desc`

## Immediate Setting Callback Contract

When a player toggles a setting in CMM, CMM executes scripted GUI:

```txt
<mod_id>__<setting_id>_on_changed = {
    scope = country
    effect = {
        cmm_toggle_bool_setting = {
            setting = <mod_id>__<setting_id>
        }
        # optional enabled/disabled logic
    }
}
```

Example callback scripted GUI names:

- `cmm_example__feature_enabled_on_changed`
- `cmm_example2__ai_helper_on_changed`

For each registered bool setting, the matching scripted GUI callback is required.
Define these in `in_game/common/scripted_guis/*.txt`.
`is_shown` is optional. If omitted, the row is visible.
When defined, `is_shown` controls row visibility (the setting box), not checked state.
Checked state is read from `var:<mod_id>__<setting_id>` by CMM UI.

## Registration Hook Contract

CMM defines and fires a shared custom on_action named `cmm_on_register_country`.

- CMM fires it on game start (after a 1-day delay), on yearly pulse for human countries, and when opening Mod Menu.
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
- `<mod_id>_name` (flag value)
- `<mod_id>_desc` (flag value)
- `cmm_tab_owner_mod_id_<mod_id>__<tab_id>` (flag value)
- `<mod_id>__<tab_id>_name` (flag value)
- `cmm_setting_owner_mod_id_<mod_id>__<setting_id>` (flag value)
- `cmm_setting_owner_tab_key_<mod_id>__<setting_id>` (flag value)
- `<mod_id>__<setting_id>_name` (flag value)
- `<mod_id>__<setting_id>_desc` (flag value)
- `<mod_id>__<setting_id>` (boolean value: `0`/`1`)

## Recommended Registration Flow

Use the shared `cmm_on_register_country` hook shown above.  
Do not create separate `on_game_start` or pulse loops per integrating mod.

## Minimal Example

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
}

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

your_mod__allow_feature_on_changed = {
    scope = country
    effect = {
        cmm_toggle_bool_setting = {
            setting = your_mod__allow_feature
        }
        if = {
            limit = {
                var:your_mod__allow_feature = 1
            }
            # enabled effect
        }
        else = {
            # disabled effect
        }
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
```

## Notes

- CMM v1 settings controls are bool-only.
- Keep ids stable (`mod_id`, `setting_id`) across updates.
- `tab_id` is required for bool-setting registration.
- Keep integration/API docs in repository docs, not runtime UI localization.
