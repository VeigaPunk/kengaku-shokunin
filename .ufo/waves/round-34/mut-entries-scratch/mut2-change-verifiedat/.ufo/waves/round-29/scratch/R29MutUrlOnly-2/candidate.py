"""Own-work hand-case candidate; never imports or executes upstream code."""
import json

ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")
URL_FIELD_NAMES = frozenset(("start_url", "reference_url", "url"))


def replace_text(text, values):
    for name in ORDER:
        text = text.replace("__" + name + "__", values[name])
    return text


def replace_url_fields(value, values):
    if isinstance(value, list):
        return [replace_url_fields(item, values) for item in value]
    if isinstance(value, dict):
        return {
            key: replace_text(item, values)
            if key in URL_FIELD_NAMES and isinstance(item, str)
            else replace_url_fields(item, values)
            for key, item in value.items()
        }
    return value


def project(raw_text, values):
    return json.loads(replace_text(raw_text, values))
