import asyncio
import json


from bs4 import BeautifulSoup as BS
from aiohttp import ClientSession

from services.olx.helpers import DataParse
from utils.extends import _


async def get_html(url: str) -> str:
    async with ClientSession(trust_env=True) as session:
        async with session.get(url) as resp:
            return await resp.text()


async def get_data(url: str) -> dict | None:
    soup = BS(await get_html(url), 'html.parser')

    try:
        script_tag = soup.find("script", {"type": "application/ld+json"})
        raw_data = json.loads(script_tag.string.strip())

        data = {
            'title': raw_data.get('name'),
            'price': f'{raw_data.get("offers").get("price")}$',
            # 'region': await DataParse.get_region(soup),
            'characs': await DataParse.get_parsed_characs(soup, raw_data.get('category')),
            'numbers': await DataParse.get_numbers(raw_data.get('sku')),
            'photos_urls': await DataParse.get_photos_urls(soup)
    }
    except Exception as e:
        print(e)
        return None

    return data


async def get_parsed_data(url: str) -> list | None:
    data = await get_data(url)

    if not data:
        return None

    media = data.get('photos_urls')
    text = _.data.format(**data)

    if media:
        media[0].caption = text
        return media


async def main():
    url = 'https://www.olx.uz/d/obyavlenie/4-xonalik-kvartita-ID3ROSf.html'
    parsed_data = await get_parsed_data(url)
    print(parsed_data)

if __name__ == '__main__':
    asyncio.run(main())