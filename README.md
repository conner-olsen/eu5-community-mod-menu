# EU5 Community Mod Menu (CMM)

A dependency mod for **Europa Universalis 5** that provides one shared in-game mod settings window.

## What it provides

- Pause menu button (`Mod Menu`) via intentional `ingame_menu.gui` override.
- Dynamic left mod list (search + compact rendering).
- Dynamic right settings panel for registered bool and numeric settings.
- Dynamic per-mod tabs in the right panel.
- Mod-id-based registration API with no fixed slot cap.
- GUI function macro layer for shared CMM data-binding expressions (`loading_screen/data_binding/cmm_macros.txt`).

## Current settings scope (v1)

- Bool settings (`0`/`1`) with checkbox controls.
- Numeric settings with stepper controls (`-` / `+`).
- Registration order is preserved.
- Value changes are persisted as country variables.
- UI invokes per-setting scripted GUI callbacks immediately on interaction.

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

cmm_register_numeric_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    tab_id = your_tab_id
    default_value = 10 # required
    min_value = 0      # required
    max_value = 100    # required
    step_value = 5     # required
}
```

Localization key format is enforced by ids:

- Mod: `<mod_id>_name`, `<mod_id>_desc`
- Tab: `<mod_id>_<tab_id>_name`
- Setting: `<mod_id>_<setting_id>_name`, `<mod_id>_<setting_id>_desc`

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
```

CMM handles numeric increase/decrease through generic marker scripted GUIs and then executes the setting-specific `_on_changed`.

Registration hook contract:

```txt
cmm_on_register_country = {
    on_actions = { your_mod_on_register_country }
}
```

Full integration docs: `docs/mod-integration.md`.

## License

GPL-3.0. See `LICENSE`.
