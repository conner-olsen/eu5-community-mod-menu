# Community Mod Menu Example Mod 3

Minimal test/integration mod for `community.mod.menu.dev`.

## What it does

- Registers mod id `cmm_example3` into CMM.
- Uses derived localization keys (`<mod_id>_name` / `<mod_id>_desc`).
- Appends into CMM shared registration hook `cmm_on_register_country`.
- Applies setting changes immediately via scripted GUI callbacks (`cmm_example3__<setting_id>_on_changed`, plus numeric `_on_decrease` / `_on_increase`).
