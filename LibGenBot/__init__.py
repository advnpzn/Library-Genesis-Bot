from telegram.ext import Updater
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("bot_token", "")

updater = Updater(TOKEN)
dp = updater.dispatcher