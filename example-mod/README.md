# Community Mod Menu Example Mod

This is a minimal integration mod for `community.mod.menu.dev`.

## What it demonstrates

- Declaring dependency on Community Mod Menu in `.metadata/metadata.json`.
- Registering a mod id (`cmm_example`) with derived localization keys.
- Appending into CMM shared registration hook `cmm_on_register_country`.
- Defining immediate per-setting scripted GUI callbacks via `_on_changed` (bool and numeric).

## Files

- `in_game/common/on_action/cmm_example_on_action.txt`
- `in_game/common/scripted_effects/cmm_example_effects.txt`
- `in_game/common/scripted_guis/cmm_example_scripted_gui.txt`
- `main_menu/localization/english/cmm_example_mod_l_english.yml`

## Test flow

1. Enable both `community.mod.menu.dev` and `community.mod.menu.example`.
2. Start a new game as any country.
3. Open pause menu and click `Mod Menu`.
4. Confirm the `Registered mods:` counter is at least `2` (core + example).

## Integration snippet for other modders

```txt
# in_game/common/scripted_effects/<your_mod>_cmm.txt
your_mod_register_in_cmm = {
    cmm_register_mod = {
        mod_id = your_mod_id
    }
}
```
