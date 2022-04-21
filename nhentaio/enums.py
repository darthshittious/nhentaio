from .better_enums import Enum


class SortType(Enum):
    """Represents a sorting method when searching."""

    recent = "recent"
    popular_today = "popular-today"
    popular_this_week = "popular-week"
    popular_this_month = "popular-month"
