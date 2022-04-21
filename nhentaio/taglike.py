from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Type


if TYPE_CHECKING:
    from typing_extensions import Self


@dataclasses.dataclass
class Taglike:
    """Taglike()

    Represents an nhentai tag.
    This class should not be instantiated manually.

    Attributes
    -----------
    name: :class:`str`
        The name of this tag.
    count: :class:`int`
        The number of galleries with this tag.

        .. note::

            Nhentai does not provide exact numbers above 1000, instead opting for rounded numbers such as 1000, 3000 and so on.
    """

    name: str
    count: int

    @classmethod
    def from_label(cls: Type[Self], name: str, count_label: str) -> Self:
        return cls(name, int(count_label[:-1]) * 1000 if "K" in count_label else int(count_label))

    def __str__(self) -> str:
        return self.name
