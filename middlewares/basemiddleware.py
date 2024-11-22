from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any

async def is_blocked(user_id: int):
    """Тестовая функция"""
    if user_id == 1795557916:
        return True
    return False

class AdminOnlyMiddleware(BaseMiddleware):
    """
    Middleware - для проверки входящих сообщений,
    для подтверждения дальнейших обработок,
    в зависимости от выполненных условий(состоит в списке администраторов)
    """
    async def __call__(self, handler: Callable, event: Message, data: Dict[str, Any]):
        if event.from_user.id in [6968137417, 1865457293]:
            return await handler(event, data)
        await event.answer('Эта команда доступна только администраторам!')

class UserOnlyMiddleware(BaseMiddleware):
    """
    Middleware - для проверки пользователей на статус блокировки,
    в случае отрицательного статуса, сообщения пользователя будут игнорироваться.
    """
    async def __call__(self, handler: Callable, event: Message, data: Dict[str, Any]):
        if not await is_blocked(user_id=event.from_user.id):
            return await handler(event, data)
        await event.answer("❌")
