"""
Nhentai API Wrapper
~~~~~~~~~~~~~~~~~~~

An asynchronous, read-only nhentai API wrapper for the damned, depraved, and disillusioned.

:copyright: (c) 2020-Present Kaylynn234
:license: MIT, see LICENSE for more details.

"""

__title__: str = "nhentaio"
__author__: str = "Kaylynn"
__license__: str = "MIT"
__copyright__: str = "Copyright 2020-Present Kaylynn234"
__version__: str = "0.3.0"

from .client import Client as Client
from .enums import SortType as SortType
from .errors import *
from .gallery import Gallery as Gallery
from .gallery import GalleryPage as GalleryPage
from .gallery import PartialGallery as PartialGallery
from .query import Days as Days
from .query import Hours as Hours
from .query import Months as Months
from .query import Query as Query
from .query import Weeks as Weeks
from .query import Years as Years
