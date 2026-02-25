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

- `mod_id` (required): stable machine id for ownership.
- `display_name_key` (required): localized mod display name.
- `description_key` (required): localized one-line description shown in the right header.

### 2) Register boolean settings

```txt
cmm_register_bool_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    display_name_key = YOUR_SETTING_NAME_KEY
    description_key = YOUR_SETTING_DESC_KEY
    default_value = 0 # optional, 0 or 1
}
```

Arguments:

- `mod_id` (required): owner mod id.
- `setting_id` (required): stable id within your mod.
- `display_name_key` (required): localized label.
- `description_key` (required): localized description.
- `default_value` (optional): initial value for brand-new saves (`0` off, `1` on).

### 3) Pending-setting helper

When users click a CMM checkbox, CMM sets a pending marker:

- `cmm_pending_setting_<mod_id>__<setting_id>`

After your mod handles the change, clear it:

```txt
cmm_clear_pending_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
}
```

### 4) Read helper trigger

```txt
cmm_is_bool_setting_enabled = {
    mod_id = your_mod_id
    setting_id = your_setting_id
}
```

Use this in your own pulse/on_action logic when processing pending markers.

## Data Contract (Runtime Variables)

CMM writes these country-scope variables/lists:

- `cmm_registered_mod_ids` (variable list; registration order)
- `cmm_registered_mod_display_name_keys` (variable list; registration order)
- `cmm_registered_setting_keys` (variable list of `<mod_id>__<setting_id>`)
- `cmm_first_registered_mod_id` (flag value; fallback selection)
- `cmm_first_registered_display_name_key` (flag value; fallback header title)
- `cmm_mod_display_name_key_<mod_id>` (flag value)
- `cmm_mod_description_key_<mod_id>` (flag value)
- `cmm_mod_description_key_by_display_name_key_<display_name_key>` (flag value)
- `cmm_setting_owner_mod_id_<mod_id>__<setting_id>` (flag value)
- `cmm_setting_label_key_<mod_id>__<setting_id>` (flag value)
- `cmm_setting_desc_key_<mod_id>__<setting_id>` (flag value)
- `cmm_setting_bool_value_<mod_id>__<setting_id>` (`1` means enabled)
- `cmm_pending_setting_<mod_id>__<setting_id>` (`1` means changed from UI)

## Recommended Registration Flow

```txt
on_game_start = {
    on_actions = {
        delay = { days = 1 }
        your_mod_register_all_humans
    }
}

yearly_country_pulse = {
    on_actions = { your_mod_ensure_registered }
}

your_mod_register_all_humans = {
    effect = {
        every_country = {
            limit = { is_ai = no }
            your_mod_register_country = yes
            your_mod_process_pending_settings = yes
        }
    }
}

your_mod_ensure_registered = {
    trigger = { is_ai = no }
    effect = {
        your_mod_register_country = yes
        your_mod_process_pending_settings = yes
    }
}
```

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

your_mod_process_pending_settings = {
    if = {
        limit = { has_variable = cmm_pending_setting_your_mod__allow_feature }

        if = {
            limit = {
                cmm_is_bool_setting_enabled = {
                    mod_id = your_mod
                    setting_id = allow_feature
                }
            }
            set_variable = { name = your_mod_feature_enabled value = 1 }
        }
        else = {
            remove_variable = your_mod_feature_enabled
        }

        cmm_clear_pending_setting = {
            mod_id = your_mod
            setting_id = allow_feature
        }
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


