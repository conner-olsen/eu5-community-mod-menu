# CMM Mod Integration

This document is for mod authors integrating with **EU5 Community Mod Menu (CMM)**.

## Scope

- CMM is a shared dependency mod.
- Your mod registers itself; CMM owns the pause-menu entry and shared window shell.
- Do not edit CMM core files to add your mod.

## Public API

Country scope effect:

```txt
cmm_register_mod = {
    mod_id = your_mod_id
    display_name_key = YOUR_MOD_NAME_KEY
    description_key = YOUR_MOD_DESC_KEY
}
```

## Arguments

- `mod_id` (required): stable machine id for your mod entry.
- `display_name_key` (required): localization key for your mod name.
- `description_key` (optional intent): localization key reserved for future right-panel metadata consistency.

## Minimal integration example

```txt
# in_game/common/scripted_effects/your_mod_cmm_effects.txt
your_mod_register_country = {
    cmm_register_mod = {
        mod_id = your_mod_id
        display_name_key = YOUR_MOD_NAME_KEY
        description_key = YOUR_MOD_DESC_KEY
    }
}
```

```txt
# in_game/common/on_action/your_mod_on_action.txt
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
        }
    }
}

your_mod_ensure_registered = {
    trigger = { is_ai = no }
    effect = {
        your_mod_register_country = yes
    }
}
```

## Localization

Define your keys in your own localization file:

```txt
YOUR_MOD_NAME_KEY: "Your Mod Name"
YOUR_MOD_DESC_KEY: "One-line description"
```

## Current limitations

- Runtime left-list labels are still on fallback entry text in current CMM build.
- True case-insensitive substring search and A-Z sorting are blocked by exposed GUI APIs.

See `docs/cmm-search-blocker.md` for tested probes and evidence.
