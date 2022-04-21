# Example #2: search.py


import asyncio

import nhentaio


async def main():
    client = nhentaio.Client()

    # You can search with a string as you would on the website
    results = await client.search('"full color"')
    for result in results:
        print(result.title)

    # By default, only 25 results are returned. You can use the limit kwarg to change that.
    results = await client.search("translated", limit=100)
    for result in results:
        print(result.title)

    # You can also change the sorting method
    results = await client.search("english", limit=10, sort_by=nhentaio.SortType.popular_this_week)
    for result in results:
        print(result.title)

    # Valid options are:
    # SortType.recent
    # SortType.popular_today
    # SortType.popular_this_week
    # SortType.popular_this_month

    # SortType.recent is the default.
    # See the documentation for more details.


asyncio.get_event_loop().run_until_complete(main())
