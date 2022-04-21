from typing_extensions import TypedDict


__all__ = ("TagType",)


class TagType(TypedDict):
    id: int
    type: str
    name: str
    url: str
    count: int
