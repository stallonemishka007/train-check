import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DB_URL = os.getenv("DB_URL")
    def validate(self):
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is not set")
        if not self.DB_URL:
            raise ValueError("DB_URL is not set")
settings = Settings()
settings.validate()