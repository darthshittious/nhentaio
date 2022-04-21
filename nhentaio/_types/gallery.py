from typing import List, Union

from typing_extensions import TypedDict

from .images import ImageType
from .tags import TagType


class _GalleryTitle(TypedDict):
    english: str
    japanese: str
    pretty: str


class Gallery(TypedDict):
    id: Union[int, str]
    media_id: str
    title: _GalleryTitle
    images: ImageType
    scanlator: str
    upload_date: int
    tags: List[TagType]
    num_pages: int
    num_favorites: int
