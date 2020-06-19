from typing import Any, Dict, Tuple

from .constants import CONTENT_TYPES, HEADERS, ContentTypes, HeaderTypes


def add_content_type_to_header(
    content_type: ContentTypes, headers: Dict[str, str]
) -> None:
    header = HEADERS[HeaderTypes.content_type]
    headers[header] = CONTENT_TYPES[content_type]


def change_dict_keys(keys: Tuple[str, str], data: Dict[str, Any]):
    for old_k, new_k in keys:
        if old_k in data:
            data[new_k] = data[old_k]
            del data[old_k]
