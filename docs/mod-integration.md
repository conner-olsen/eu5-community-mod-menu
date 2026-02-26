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
    display_name_key = YOUR_MOD_NAME_KEY
    description_key = YOUR_MOD_DESC_KEY
}
```

Arguments:

- `mod_id`: stable machine id for ownership.
- `display_name_key`: localized mod display name.
- `description_key`: localized one-line description shown in the right header.

### 2) Register boolean settings

```txt
cmm_register_bool_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    display_name_key = YOUR_SETTING_NAME_KEY
    description_key = YOUR_SETTING_DESC_KEY
    default_value = 0 # 0 (off) or 1 (on)
}
```

Arguments:

- `mod_id`: owner mod id.
- `setting_id`: stable id within your mod.
- `display_name_key`: localized label.
- `description_key`: localized description.
- `default_value`: initial value for brand-new saves (`0` off, `1` on).

## Immediate Setting Callback Contract

When a player toggles a setting in CMM, CMM immediately calls:

```txt
<mod_id>__<setting_id>_on_changed = {
    # CMM provides the setting key in $setting$
    # Example: cmm_example__feature_enabled
}
```

Example callback names:

- `cmm_example__feature_enabled_on_changed`
- `cmm_example2__ai_helper_on_changed`

Callbacks run in player country scope.

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
- `cmm_registered_setting_keys` (variable list of `<mod_id>__<setting_id>`)
- `cmm_mod_display_name_key_<mod_id>` (flag value)
- `cmm_mod_description_key_<mod_id>` (flag value)
- `cmm_setting_owner_mod_id_<mod_id>__<setting_id>` (flag value)
- `<mod_id>__<setting_id>_label` (flag value)
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
        display_name_key = YOUR_MOD_NAME
        description_key = YOUR_MOD_DESC
    }

    cmm_register_bool_setting = {
        mod_id = your_mod
        setting_id = allow_feature
        display_name_key = YOUR_MOD_SETTING_ALLOW_FEATURE
        description_key = YOUR_MOD_SETTING_ALLOW_FEATURE_DESC
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
    if = {
        limit = {
            var:$setting$ = 1
        }
        set_variable = { name = your_mod_feature_enabled value = 1 }
    }
    else = {
        set_variable = { name = your_mod_feature_enabled value = 0 }
    }
}
```

## Localization

Define your keys in your own localization file:

```txt
YOUR_MOD_NAME: "Your Mod Name"
YOUR_MOD_DESC: "One-line description"
YOUR_MOD_SETTING_ALLOW_FEATURE: "Allow Feature"
YOUR_MOD_SETTING_ALLOW_FEATURE_DESC: "Enables the feature when checked."
```

## Notes

- CMM v1 settings controls are bool-only.
- Keep ids stable (`mod_id`, `setting_id`) across updates.
- Keep integration/API docs in repository docs, not runtime UI localization.
