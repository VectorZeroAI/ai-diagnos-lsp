from fix_busted_json import repair_json, can_parse_json # pyright: ignore

def optional_repair_json(json: str) -> str:
    if can_parse_json(json):
        return json
    else:
        return repair_json(json)

