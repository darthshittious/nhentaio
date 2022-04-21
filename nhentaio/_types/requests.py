from typing import List

from typing_extensions import TypedDict

from .gallery import Gallery


class SearchPayload(TypedDict):
    result: List[Gallery]
    num_pages: int
    per_page: int
