"""Code generator: ModModel -> Paradox script files."""

import json
from .models import ModModel, Setting, ListField


def generate_all(model: ModModel) -> dict:
    """Generate all output files from a ModModel. Returns {filepath: content}."""
    prefix = model.file_prefix or model.mod_id
    mod_id = model.mod_id

    files = {}
    if mod_id:
        files[f"in_game/common/on_action/{prefix}_on_action.txt"] = _gen_on_action(prefix)
        files[f"in_game/common/scripted_effects/{prefix}_effects.txt"] = _gen_effects(model)
        files[f"in_game/common/scripted_guis/{prefix}_scripted_gui.txt"] = _gen_scripted_guis(model)
        files[f"main_menu/localization/english/{prefix}_l_english.yml"] = _gen_localization(model)
        files[".metadata/metadata.json"] = _gen_metadata(model)

    return files


def _gen_on_action(prefix: str) -> str:
    return (
        f"# Hook this mod into CMM shared registration on_action.\n"
        f"cmm_on_mod_registration = {{\n"
        f"\ton_actions = {{\n"
        f"\t\t{prefix}_on_register_mod\n"
        f"\t}}\n"
        f"}}\n"
        f"\n"
        f"{prefix}_on_register_mod = {{\n"
        f"\teffect = {{\n"
        f"\t\t{prefix}_register_mod = yes\n"
        f"\t}}\n"
        f"}}\n"
    )


def _gen_effects(model: ModModel) -> str:
    prefix = model.file_prefix or model.mod_id
    mod_id = model.mod_id
    lines = []
    lines.append(f"# Root scope: country.")
    lines.append(f"{prefix}_register_mod = {{")

    first = True
    for tab in model.tabs:
        for group in tab.groups:
            for setting in group.settings:
                if not first:
                    lines.append("")
                first = False
                _emit_registration(lines, mod_id, tab.tab_id, group.group_id, setting)

    lines.append("}")

    # Text setting effects (text callbacks are scripted effects, not scripted GUIs)
    for tab in model.tabs:
        for group in tab.groups:
            for setting in group.settings:
                if setting.setting_type == "text":
                    qid = f"{mod_id}__{setting.setting_id}"
                    lines.append("")
                    lines.append(f"{qid}_on_changed = {{")
                    lines.append(f"\t# Custom text handling effect. Uses $text$ parameter.")
                    lines.append(f"\t# Replace this placeholder with your actual effect logic.")
                    lines.append(f"\tlog = \"Text submitted: $text$\"")
                    lines.append("}")

    return "\n".join(lines) + "\n"


def _emit_registration(lines: list, mod_id: str, tab_id: str, group_id: str, setting: Setting):
    st = setting.setting_type
    is_global = setting.is_global

    if st == "list":
        # List registration: no group_id
        lines.append(f"\tcmm_register_settings_list = {{")
        lines.append(f"\t\tmod_id = {mod_id}")
        lines.append(f"\t\tsetting_id = {setting.setting_id}")
        lines.append(f"\t\ttab_id = {tab_id}")
        lines.append(f"\t\titem_count = {_int(setting.item_count, 1)}")
        lines.append(f"\t\tis_ordered = {_int(setting.is_ordered, 0)}")
        lines.append(f"\t}}")

        # List fields
        for field in (setting.fields or []):
            lines.append("")
            _emit_list_field(lines, mod_id, setting.setting_id, field)
        return

    # Determine registration function name
    prefix_map = {
        "bool": "bool_setting",
        "button": "button_setting",
        "numeric": "numeric_setting",
        "slider": "slider_setting",
        "dropdown": "dropdown_setting",
        "text": "text_setting",
    }
    func_name = prefix_map.get(st, st)
    if is_global and st not in ("text", "list"):
        reg_func = f"cmm_register_global_{func_name}"
    else:
        reg_func = f"cmm_register_{func_name}"

    lines.append(f"\t{reg_func} = {{")
    lines.append(f"\t\tmod_id = {mod_id}")
    lines.append(f"\t\tsetting_id = {setting.setting_id}")
    lines.append(f"\t\ttab_id = {tab_id}")
    lines.append(f"\t\tgroup_id = {group_id}")

    if st == "bool":
        lines.append(f"\t\tdefault_value = {_int(setting.default_value, 0)}")
    elif st == "button":
        pass  # no extra params
    elif st in ("numeric", "slider"):
        lines.append(f"\t\tdefault_value = {_num(setting.default_value, 0)}")
        lines.append(f"\t\tmin_value = {_num(setting.min_value, 0)}")
        lines.append(f"\t\tmax_value = {_num(setting.max_value, 100)}")
        lines.append(f"\t\tstep_value = {_num(setting.step_value, 1)}")
    elif st == "dropdown":
        lines.append(f"\t\tdefault_index = {_int(setting.default_index, 1)}")
        lines.append(f"\t\toption_count = {_int(setting.option_count, 1)}")
    elif st == "text":
        lines.append(f"\t\tcharacter_limit = {_int(setting.character_limit, 42)}")
        lines.append(f"\t\tquote_text = {_int(setting.quote_text, 0)}")

    lines.append(f"\t}}")


def _emit_list_field(lines: list, mod_id: str, setting_id: str, field: ListField):
    ft = field.field_type
    if ft == "bool":
        lines.append(f"\tcmm_register_list_bool_field = {{")
        lines.append(f"\t\tmod_id = {mod_id}")
        lines.append(f"\t\tsetting_id = {setting_id}")
        lines.append(f"\t\tfield_id = {field.field_id}")
        lines.append(f"\t\tdefault_value = {_int(field.default_value, 0)}")
        lines.append(f"\t}}")
    elif ft == "dropdown":
        lines.append(f"\tcmm_register_list_dropdown_field = {{")
        lines.append(f"\t\tmod_id = {mod_id}")
        lines.append(f"\t\tsetting_id = {setting_id}")
        lines.append(f"\t\tfield_id = {field.field_id}")
        lines.append(f"\t\tdefault_index = {_int(field.default_index, 1)}")
        lines.append(f"\t\toption_count = {_int(field.option_count, 1)}")
        lines.append(f"\t}}")
    elif ft == "numeric":
        lines.append(f"\tcmm_register_list_numeric_field = {{")
        lines.append(f"\t\tmod_id = {mod_id}")
        lines.append(f"\t\tsetting_id = {setting_id}")
        lines.append(f"\t\tfield_id = {field.field_id}")
        lines.append(f"\t\tdefault_value = {_num(field.default_value, 0)}")
        lines.append(f"\t\tmin_value = {_num(field.min_value, 0)}")
        lines.append(f"\t\tmax_value = {_num(field.max_value, 10)}")
        lines.append(f"\t\tstep_value = {_num(field.step_value, 1)}")
        lines.append(f"\t}}")


def _gen_scripted_guis(model: ModModel) -> str:
    mod_id = model.mod_id
    blocks = []

    for tab in model.tabs:
        for group in tab.groups:
            for setting in group.settings:
                if setting.setting_type == "text":
                    continue  # text uses scripted effects
                qid = f"{mod_id}__{setting.setting_id}"
                blocks.append(_gen_callback_block(setting, qid))

    return "\n\n".join(blocks) + "\n"


def _gen_callback_block(setting: Setting, qid: str) -> str:
    st = setting.setting_type
    is_global = setting.is_global
    var_prefix = "global_var" if is_global else "var"

    lines = []
    lines.append(f"{qid}_on_changed = {{")
    lines.append(f"\tscope = country")
    lines.append(f"")
    lines.append(f"\teffect = {{")

    if st == "bool":
        lines.append(f"\t\tcmm_toggle_bool_setting = {{")
        lines.append(f"\t\t\tsetting = {qid}")
        lines.append(f"\t\t}}")
        lines.append(f"")
        lines.append(f"\t\tif = {{")
        lines.append(f"\t\t\tlimit = {{ {var_prefix}:{qid} = 1 }}")
        lines.append(f"\t\t\t# enabled effect")
        lines.append(f"\t\t}}")
        lines.append(f"\t\telse = {{")
        lines.append(f"\t\t\t# disabled effect")
        lines.append(f"\t\t}}")
    elif st == "button":
        lines.append(f"\t\t# Button effect")
    elif st == "numeric":
        lines.append(f"\t\tcmm_apply_numeric_change = {{")
        lines.append(f"\t\t\tsetting = {qid}")
        lines.append(f"\t\t}}")
        lines.append(f"\t\t# optional custom logic")
    elif st == "slider":
        lines.append(f"\t\tcmm_apply_slider_change = {{")
        lines.append(f"\t\t\tsetting = {qid}")
        lines.append(f"\t\t}}")
        lines.append(f"\t\t# optional custom logic")
    elif st == "dropdown":
        lines.append(f"\t\tcmm_apply_dropdown_change = {{")
        lines.append(f"\t\t\tsetting = {qid}")
        lines.append(f"\t\t}}")
        lines.append(f"\t\t# optional custom logic")
    elif st == "list":
        lines.append(f"\t\tcmm_apply_list_change = {{")
        lines.append(f"\t\t\tsetting = {qid}")
        lines.append(f"\t\t}}")
        lines.append(f"\t\t# optional custom logic")

    lines.append(f"\t}}")
    lines.append(f"}}")
    return "\n".join(lines)


def _gen_localization(model: ModModel) -> str:
    mod_id = model.mod_id
    lines = []
    lines.append("l_english:")

    # Mod
    lines.append(" # Mod")
    lines.append(f' {mod_id}_name: "{_esc(model.mod_name)}"')
    lines.append(f' {mod_id}_desc: "{_esc(model.mod_desc)}"')

    # Tabs
    if model.tabs:
        lines.append("")
        lines.append(" # Tabs")
        for tab in model.tabs:
            lines.append(f' {mod_id}__{tab.tab_id}_name: "{_esc(tab.name)}"')

    # Groups (deduplicated by group_id)
    seen_groups = {}
    for tab in model.tabs:
        for group in tab.groups:
            if group.group_id not in seen_groups:
                seen_groups[group.group_id] = group.name

    if seen_groups:
        lines.append("")
        lines.append(" # Groups")
        for gid, gname in seen_groups.items():
            lines.append(f' {mod_id}__{gid}_name: "{_esc(gname)}"')

    # Settings by tab and group
    for tab in model.tabs:
        for group in tab.groups:
            has_settings = len(group.settings) > 0
            if has_settings:
                lines.append("")
                lines.append(f" # {_esc(tab.name)} Tab - {_esc(group.name)}")

            for setting in group.settings:
                _emit_setting_loc(lines, mod_id, setting)

    return "\n".join(lines) + "\n"


def _emit_setting_loc(lines: list, mod_id: str, setting: Setting):
    qid = f"{mod_id}__{setting.setting_id}"
    st = setting.setting_type

    lines.append(f' {qid}_name: "{_esc(setting.name)}"')
    lines.append(f' {qid}_desc: "{_esc(setting.desc)}"')

    if st == "button":
        lines.append(f' {qid}_text: "{_esc(setting.button_text or "Run")}"')

    elif st == "dropdown":
        for opt in (setting.options or []):
            lines.append(f' {qid}_option_{opt.index}_name: "{_esc(opt.name)}"')

    elif st == "list":
        lines.append(f' {qid}_item_column_name: "{_esc(setting.item_column_name or "Item")}"')
        for i, name in enumerate(setting.item_names or [], start=1):
            lines.append(f' {qid}_item_{i}_name: "{_esc(name)}"')

        for field in (setting.fields or []):
            fqid = f"{qid}__{field.field_id}"
            lines.append(f' {fqid}_name: "{_esc(field.name)}"')
            if field.field_type == "dropdown":
                for opt in (field.options or []):
                    lines.append(f' {fqid}_option_{opt.index}_name: "{_esc(opt.name)}"')


def _gen_metadata(model: ModModel) -> str:
    data = {
        "name": model.metadata_name or model.mod_name,
        "id": model.metadata_id,
        "version": model.metadata_version,
        "game_id": "eu5",
        "supported_game_version": model.metadata_game_version,
        "short_description": model.metadata_short_description or model.mod_desc,
        "tags": model.metadata_tags,
        "relationships": [
            {
                "rel_type": "dependency",
                "id": "community.mod.menu.dev",
                "display_name": "Community Mod Menu Dev",
                "resource_type": "mod",
                "version": "*",
            }
        ],
        "game_custom_data": {},
    }
    return json.dumps(data, indent=4, ensure_ascii=False)


def _int(v, default=0) -> int:
    if v is None:
        return default
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _num(v, default=0):
    if v is None:
        return default
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except (TypeError, ValueError):
        return default


def _esc(s: str) -> str:
    """Escape a string for Paradox localization YAML."""
    if not s:
        return ""
    return s.replace("\\", "\\\\").replace('"', '\\"')
