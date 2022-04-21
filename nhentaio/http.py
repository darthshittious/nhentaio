from __future__ import annotations

import datetime
import re
from typing import TYPE_CHECKING, Any, Dict, List, NamedTuple, Optional, Union

import aiohttp

from nhentaio.enums import SortType

from .asset import Asset
from .errors import NHentaiError
from .gallery import Gallery
from .query import Query
from .taglike import Taglike


if TYPE_CHECKING:
    from ._types.gallery import Gallery as GalleryType
    from ._types.requests import SearchPayload

NHENTAI_ACTUAL_ID_PATTERN = re.compile(r'data-src="https://t\.nhentai\.net/galleries/(\d+)/\w+\.jpg"')
NHENTAI_ID_PATTERN = re.compile(r"/g/(\d*)/")
NHENTAI_RESULT_COUNT_PATTERN = re.compile(r"\s*(\d+)\s*results")

TITLE_PREFIX = "/html/body/div[2]/div[1]/div[2]/div"


class GalleryTags(NamedTuple):
    tags: Dict[str, List[Taglike]]
    pages: int
    date: datetime.datetime


class RawSearchResults(NamedTuple):
    total: int
    results: ...


class HTTPClient:
    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None

    async def _create_session(self) -> aiohttp.ClientSession:
        self._session = aiohttp.ClientSession()
        return self._session

    async def route(self, url: str, params: Dict[str, str], *, allow_redirects: bool = True) -> Any:
        if not self._session:
            await self._create_session()
            assert self._session is not None

        async with self._session.get(url, params=params, allow_redirects=allow_redirects) as response:
            if allow_redirects:
                if 300 > response.status >= 200:
                    return await response.json()
                else:
                    raise NHentaiError(f"Error {response.status}: Invalid response :: {response.headers}")
            else:
                if response.status == 302:
                    ## this looks like it returns this code for /random/
                    new_digits = response.headers["location"]  # /g/xxxxx/
                    await self.route(
                        url.replace("/random/", f"/api/gallery/{new_digits}"), params=params, allow_redirects=True
                    )

    async def image_from_url(self, url: str) -> bytes:
        session = self._session or await self._create_session()

        async with session.get(url) as response:
            if 300 > response.status >= 200:
                return await response.read()
            else:
                raise NHentaiError(f"Error {response.status} when attempting to read image.")

    async def parse_gallery_payload(self, payload: GalleryType) -> Gallery:
        id_ = payload["id"]
        media_id = payload["media_id"]
        title = payload["title"]
        images = payload["images"]
        scanlator = payload["scanlator"]
        upload_date = datetime.datetime.fromtimestamp(payload["upload_date"])
        tags_ = payload["tags"]
        tags = [Taglike(tag["name"], tag["count"]) for tag in tags_]
        num_pages = payload["num_pages"]
        num_favorites = payload["num_favorites"]

        cover = Asset(images["cover"]["t"], self)

        return Gallery(
            id=id_,
            media_id=media_id,
            title=(title.get("english") or title.get("japanese")) or "Untitled",
            subtitle=title.get("pretty", "No subtitle"),
            scanlator=scanlator,
            cover=cover,
            tags=tags,
            page_count=num_pages,
            uploaded=upload_date,
            favourites=num_favorites,
            url=f"https://nhentai.net/g/{id_}/",
        )

    async def galleries_from(self, response: SearchPayload, limit: Optional[int]) -> List[Gallery]:
        results: List[Gallery] = []

        for idx, payload in enumerate(response["result"], start=1):
            if limit and idx > limit:
                break

            gallery = await self.parse_gallery_payload(payload)

            results.append(gallery)

        return results

    async def search(self, query: Union[str, Query], *, sort_by: SortType, limit: Optional[int] = None) -> List[Gallery]:
        request_parameters: Dict[str, str] = {"query": str(query), "sort": str(sort_by)}

        search_result: SearchPayload = await self.route("https://nhentai.net/api/galleries/search", request_parameters)

        return await self.galleries_from(search_result, limit=limit)

    async def close(self):
        if self._session is not None:
            await self._session.close()
