# EU5 Community Mod Menu (CMM)

A dependency mod for **Europa Universalis 5** that provides one shared in-game mod settings window.

## What it provides

- Pause menu button (`Mod Menu`) via intentional `ingame_menu.gui` override.
- Dynamic left mod list (search + compact rendering).
- Dynamic right settings panel for registered boolean settings.
- Mod-id-based registration API with no fixed slot cap.

## Current settings scope (v1)

- Boolean settings only.
- Registration order is preserved.
- Value changes are persisted as country variables.
- UI invokes immediate per-setting callback effects after each toggle.

## Install

1. Place this folder in `Documents\Paradox Interactive\Europa Universalis V\mod`.
2. Enable `community.mod.menu.dev` (and any integrating mod) in the launcher.

## Integration API summary

Country scope:

```txt
cmm_register_mod = {
    mod_id = your_mod_id
    display_name_key = YOUR_MOD_NAME_KEY
    description_key = YOUR_MOD_DESC_KEY
}

cmm_register_bool_setting = {
    mod_id = your_mod_id
    setting_id = your_setting_id
    display_name_key = YOUR_SETTING_NAME_KEY
    description_key = YOUR_SETTING_DESC_KEY
    default_value = 0 # optional; 0 or 1
}
```

Callback contract:

```txt
# CMM calls this on each UI toggle and passes $setting$:
<mod_id>__<setting_id>_on_changed = {
    if = { limit = { var:$setting$ = yes } ... }
}
```

Registration hook contract:

```txt
cmm_on_register_country = {
    on_actions = { your_mod_on_register_country }
}
```

Full integration docs: `docs/mod-integration.md`.

## License

GPL-3.0. See `LICENSE`.

