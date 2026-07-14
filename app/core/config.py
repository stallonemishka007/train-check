import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DB_URL = os.getenv("DB_URL")
settings = Settings()