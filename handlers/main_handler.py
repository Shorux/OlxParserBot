from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

user_rt = Router(name='user')

@user_rt.message(CommandStart())
async def start_handler(message: Message):
    await message.answer('hello')
