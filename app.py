import os
import logging
import asyncio

from config import BOT_TOKEN, DEBUG
from dispatcher import bot, dp

# from data.models import init_db
# from tests.db_tests import start_test
from handlers.main_handler import user_rt


def start_logging():
    if DEBUG:
        logging.basicConfig(level=logging.INFO)
        return

    if not os.path.isdir('logs'):
        os.mkdir('logs')
    logging.basicConfig(
        filename=f'./logs/bot_{BOT_TOKEN.split(":")[0]}.log',
        level=logging.WARNING,
        format='~%(asctime)s %(message)s'
    )


async def main():
    dp.include_router(user_rt)
    # await start_test()
    # await init_db()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    start_logging()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
