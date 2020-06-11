from typing import Dict

from .constants import CONTENT_TYPES, HEADERS, ContentTypes, HeaderTypes


def add_content_type_to_header(
    content_type: ContentTypes, headers: Dict[str, str]
) -> None:
    header = HEADERS[HeaderTypes.content_type]
    headers[header] = CONTENT_TYPES[content_type]
