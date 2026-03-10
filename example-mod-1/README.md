# Community Mod Menu Example Mod 1

This is a reference integration mod for `community.mod.menu.dev`.

## What it demonstrates

- Declaring dependency on Community Mod Menu in `.metadata/metadata.json`.
- Registering a mod id (`cmm_example1`) with derived localization keys.
- Appending into CMM shared registration hook `cmm_on_mod_registration`.
- Defining immediate per-setting callbacks for bool, global bool, button, numeric, slider, dropdown, and text examples.
- Grouping the first tab into `toggles` and `values` sections.
- Keeping a global bool example on the first tab for multiplayer host-only edit testing.

## Files

- `in_game/common/on_action/cmm_example1_on_action.txt`
- `in_game/common/scripted_effects/cmm_example1_effects.txt`
- `in_game/common/scripted_guis/cmm_example1_scripted_gui.txt`
- `main_menu/localization/english/cmm_example1_mod_l_english.yml`

## Test flow

1. Enable both `community.mod.menu.dev` and `community.mod.menu.example1`.
2. Start a new game as any country.
3. Open pause menu and click `Mod Menu`.
4. Confirm the `Registered mods:` counter is at least `2` (core + example).
5. Select `CMM Example Mod 1` and confirm the `General` tab shows the full sample set across `Toggles` and `Values`.

## Integration snippet for other modders

```txt
# in_game/common/scripted_effects/<your_mod>_cmm.txt
your_mod_register_in_cmm = {
    cmm_register_mod = {
        mod_id = your_mod_id
    }
}
```
