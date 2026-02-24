# EU5 Community Mod Menu (CMM)

A dependency mod for **Europa Universalis 5** that provides one shared in-game mod settings window.

## What it provides

- Pause menu button (`Mod Menu`) via intentional `ingame_menu.gui` override.
- Central settings window shell for registered mods.
- Mod-id-based registration API with no fixed slot cap.

## Current status

- Registration works for multiple independent mods without editing core CMM files.
- Left list currently renders registered entries in registration order.
- Advanced search targets (case-insensitive substring) and A-Z sorting are currently blocked by exposed GUI string APIs.

See blocker details: `docs/cmm-search-blocker.md`.

## Install

1. Place this folder in `Documents\Paradox Interactive\Europa Universalis V\mod`.
2. Enable `community.mod.menu.dev` (and any integrating mod) in the launcher.

## Mod integration

API (country scope):

```txt
cmm_register_mod = {
    mod_id = your_mod_id
    display_name_key = YOUR_MOD_NAME_KEY
    description_key = YOUR_MOD_DESC_KEY # optional in intent, reserved for future right-panel metadata
}
```

Recommended registration flow:

- Register on `on_game_start` with a short delay (for player country availability).
- Re-assert registration on a periodic country pulse for human countries.

Full docs: `docs/mod-integration.md`.

## License

GPL-3.0. See `LICENSE`.
