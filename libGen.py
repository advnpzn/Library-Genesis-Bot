#bot_token=1577577500:AAHQTymtwHZYDPqheOzkfSHMlJx2LcgPMJ4

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, Dispatcher, CallbackContext
from plugins.search_gen import search
from plugins.feelters import f

res = ''

def show(update : Update, context : CallbackContext)->None:
    query =' '.join(context.args)
    global res
    res = search(query,f)
    if len(res) == 0:
        update.message.reply_text('Not found :(')
    else:
        update.message.reply_text(f"<b>Query :</b> : <pre>{query}</pre>\n"
                                f"<b>Total Results :</b> <pre>{len(res)}</pre>\n"
                                f"Do /show (result)\n e.g. /show 1",parse_mode='HTML')

def s(update : Update, context : CallbackContext)->None:
    q = int(context.args[0])
    try:
        r = res[q-1]
        update.message.reply_text(f"<b>ID :</b> <pre>{r['ID']}</pre>\n"
                f"<b>Author :</b> <pre>{r['Author']}</pre>\n"
                f"<b>Title :</b> <pre>{r['Title']}</pre>\n"
                f"<b>Year :</b> <pre>{r['Year']}</pre>\n"
                f"<b>Pages :</b> <pre>{r['Pages']}</pre>\n"
                f"<b>Language :</b> <pre>{r['Language']}</pre>\n"
                f"<b>Size :</b> <pre>{r['Size']}</pre>\n"
                f"<b>Type :</b> <pre>{r['Extension']}</pre>\n"
                f"<b>Link :</b> {r['Mirror_1']}",parse_mode = 'HTML')
    except IndexError:
        update.message.reply_text('Choose the correct result o make sure you did /search before.')


if __name__ == "__main__":
    updater = Updater(token='1577577500:AAHQTymtwHZYDPqheOzkfSHMlJx2LcgPMJ4',use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('search',show,run_async=True))
    dp.add_handler(CommandHandler('show',s,run_async=True))
    updater.start_polling()
    updater.idle()
