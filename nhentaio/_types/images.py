from typing import List

from typing_extensions import Literal, TypedDict


__all__ = ("ImageType",)


class ImageKeys(TypedDict):
    t: Literal["j", "p", "g"]
    w: int
    h: int


class ImageType(TypedDict):
    pages: List[ImageKeys]
    cover: ImageKeys
    thumbnail: ImageKeys
