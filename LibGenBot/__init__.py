from telegram.ext import Updater
import os

TOKEN = os.environ.get('bot_token')

updater = Updater(TOKEN)
dp = updater.dispatcher