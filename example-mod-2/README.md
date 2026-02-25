# Community Mod Menu Example Mod 2

Minimal test/integration mod for `community.mod.menu.dev`.

## What it does

- Registers mod id `cmm_example2` into CMM.
- Uses explicit `display_name_key` and `description_key`.
- Appends into CMM shared registration hook `cmm_on_register_country`.
- Applies setting changes immediately via `cmm_example2__<setting_id>_on_changed`.
