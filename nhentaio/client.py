import re
from typing import TYPE_CHECKING, List, Union

from .enums import SortType
from .gallery import Gallery
from .http import HTTPClient
from .query import Query


if TYPE_CHECKING:
    from ._types.gallery import Gallery as GalleryType

GALLERY_ID_PATTERN = re.compile(r'<h3 id="gallery_id"><span class="hash">#</span>(\d*)</h3>')


class Client:
    """Represents a client that can be used to interact with nhentai."""

    def __init__(self) -> None:
        self.open: bool = True
        self._state: HTTPClient = HTTPClient()

    async def search(self, query: Union[str, Query], *, limit=25, sort_by=SortType.recent) -> List[Gallery]:
        """Performs an nhentai search with the given query.

        .. note::

            Results from searches are of type :class:`~.PartialGallery`, as opposed to :class:`~.Gallery`, and have less information available.
            To get full information about a gallery, including pages and tags, use :meth:`~Client.fetch_gallery`: or :meth:`~.Client.fetch_galleries`.

        Parameters
        -----------
        query: Union[:class:`str`, :class:`~.Taglike`, :class:`~.Query`]
            The query to use when searching. For ease of use this parameter is implicitly cast to :class:`str` for you.

            .. note::

                For building complex search queries, consider using :class:`~.Query`.

        limit: :class:`int`
            The maximum amount of galleries to return. Defaults to 25.

        sort_by: :class:`~.SortType`
            The method by which results should be sorted. Defaults to `SortType.recent`.

        Returns
        --------
        :class:`~.AsyncIterator`
            An asynchronous iterator yielding the results that were found.
        """
        return await self._state.search(query, sort_by=sort_by, limit=limit)

    async def fetch_gallery(self, id: Union[int, str]) -> Gallery:
        """Fetches a gallery from nhentai with the specified ID.

        Parameters
        -----------
        id: Union[:class:`int`, :class:`str`]
            The ID of the gallery to fetch.

        Returns
        --------
        :class:`~.Gallery`
            The gallery with the passed ID.
        """

        response: GalleryType = await self._state.route(f"https://nhentai.net/g/{id}", {})

        return await self._state.parse_gallery_payload(response)

    async def random_gallery(self) -> Gallery:
        """Fetches a random gallery from nhentai.

        .. note::

            This is equivalent to using the "random" button on the nhentai website.

        Returns
        --------
        :class:`~.Gallery`
            The gallery that was found.
        """

        response: GalleryType = await self._state.route("https://nhentai.net/random", {}, allow_redirects=False)
        return await self._state.parse_gallery_payload(response)

    async def fetch_galleries(self, *args: str) -> List[Gallery]:
        """Fetches multiple galleries using the passed IDs.

        Parameters
        -----------
        args: Iterable[:class:`str`]
            The IDs to use when fetching.

        Returns
        --------
        List[:class:`~Gallery`]
            The galleries returned.
        """

        ret: List[Gallery] = []
        for id_ in args:
            gallery = await self.fetch_gallery(id_)
            ret.append(gallery)

        return ret

    async def close(self) -> None:
        """Closes the internal connection handler and effectively "switches off" the client."""

        await self._state.close()
        self.open = False
