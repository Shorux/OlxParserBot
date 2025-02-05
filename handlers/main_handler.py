from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from services.olx.requests import get_parsed_data

from utils.extends import _

user_rt = Router(name='user')

@user_rt.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(_.greetings)

@user_rt.message(F.text.startswith('https://www.olx'))
async def start_handler(message: Message):
    try:
        media = await get_parsed_data(message.text.replace('oz/', ''))
    except:
        await message.answer(_.wrong_url)
        raise AssertionError(message.text)

    if media:
        await message.answer_media_group(media[:10])
        if len(media) > 10:
            await message.answer_media_group(media[10:])
    else:
        await message.answer(_.wrong_url)
