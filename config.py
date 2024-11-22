import os
import logging

from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(os.getenv('DEBUG', False))
# DATABASE_URL = os.getenv('DATABASE_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logging.error("BOT_TOKEN is not defined neither in .env file nor in environment variables")
    quit()
