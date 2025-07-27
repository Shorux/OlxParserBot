from aiogram.types import InputMediaPhoto, URLInputFile
from aiohttp import ClientSession
from bs4 import BeautifulSoup as BS

from utils.extends import _


class DataParse:
    @staticmethod
    async def get_numbers(product_id: int) -> str:
        url = f"https://www.olx.uz/api/v1/offers/{product_id}/limited-phones/"
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return "*Свяжитесь по номеру*:\n" + '\n'.join(data.get('data').get('phones')).replace(' ', '')
                else:
                    return ""

    @staticmethod
    async def get_photos_urls(soup: BS):
        photos_divs = soup.find('div', class_='swiper-wrapper').find_all('div', class_='swiper-slide')

        photos_urls = []
        for i, photo_div in enumerate(photos_divs):
            photo_div = photo_div.find('div', class_='swiper-zoom-container')
            image_tag = photo_div.find('img')
            photo_url = image_tag.get('src', None)
            if photo_url:
                media = InputMediaPhoto(media=URLInputFile(photo_url))
                photos_urls.append(media)

        return photos_urls

    @staticmethod
    async def get_region(soup: BS):
        div = soup.find('div', class_='css-6u8zs6').find('section', class_='css-wefbef')
        print(div.prettify())
        region = div.find('span', class_='css-1c0ed4l')
        if region:
            return region.text.strip()
        return ''

    @staticmethod
    async def get_parsed_characs(soup: BS, category):
        characs = soup.find('div', class_='css-1g2c38u')
        data = {}
        for charac in characs:
            charac = charac.text.strip()
            if charac.startswith('Количество комнат'):
                data['rooms'] = charac.split(': ')[1]
            elif charac.startswith('Площадь участка'):
                data['meters'] = charac.split(': ')[1]
            elif charac.startswith('Общая площадь'):
                data['meters'] = charac.split(': ')[1].replace(' м²', '')
            elif charac.startswith('Этажность дома'):
                data['house_floors'] = charac.split(': ')[1]
            elif charac.startswith('Этаж'):
                data['floor'] = charac.split(': ')[1]

        if 'kvartiry' in category:
            return _.apartment_characs.format(
                rooms=data.get('rooms', ''),
                floor=data.get('floor', ''),
                house_floors=data.get('house_floors', ''),
                meters=data.get('meters', '')
            )
        elif 'nedvizhimost' in category:
            return _.house_characs.format(
                rooms=data.get('rooms', ''),
                house_floors=data.get('house_floors', ''),
                meters=data.get('meters', '')
            )
