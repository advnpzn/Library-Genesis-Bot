import os
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, Dispatcher, CallbackContext
from plugins.search_gen import search

res = ''

def show(update : Update, context : CallbackContext)->None:
    query =' '.join(context.args)
    update.message.reply_text('Bot has been stopped and is currently under further development.')
    global res
    res = search(query)
    if len(res) == 0:
        update.message.reply_text('Not found :(')
    else:
        update.message.reply_text(f"<b>Query :</b> : <pre>{query}</pre>\n"
                                f"<b>Total Results :</b> <pre>{len(res)}</pre>\n"
                                f"Do /show (result)\n e.g. /show 1",parse_mode='HTML')

def s(update : Update, context : CallbackContext)->None:
    update.message.reply_text('Bot has been stopped and is currently under further development.')                          
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
        update.message.reply_text('Choose the correct result or make sure you did /search before.')

def help(update : Update, context : CallbackContext)->None:
    update.message.reply_text("Library Genesis is a library collection of pirated books.\n"
                    "Search the books and get the results via\nSTEP 1 : "
                    "/search (book name)\ne.g. /search Wimpy Kid\n"
                    "This show currently how many books are there for the given search query.\n"
                    "STEP 2 : /show (number)\ne.g. /show 4\n"
                    " Put a number that's in inclusive range of the Total no.of books you got in /search.\n"
                    "Wanna Contact Dev ?\n"
                    "Telegram username : @ATPnull")                                  
                                  
def start(update : Update, context : CallbackContext)->None:
    update.message.reply_text("Welcome!\nPress /help for more information.")
                                  
                                  
if __name__ == "__main__":
    TOKEN = os.environ.get("bot_token","")
    updater = Updater(token=TOKEN,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('search',show,run_async=True))
    dp.add_handler(CommandHandler('show',s,run_async=True))
    dp.add_handler(CommandHandler('help',help,run_async=True))
    dp.add_handler(CommandHandler('start',start,run_async=True))                               
    updater.start_polling()
    updater.idle()
