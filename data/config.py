from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
ADMIN_IDS = list(map(int, getenv('ADMIN_IDS').replace(" ", "").split(",")))

DB_DSN = getenv('DB_DSN')

PROVIDER_TOKEN = getenv('PROVIDER_TOKEN')


HEROKU_APP_NAME = getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/token/{BOT_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(getenv('PORT', 80))