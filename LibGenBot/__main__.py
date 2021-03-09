from telegram import (Update,
                      ParseMode,
                      InlineKeyboardMarkup,
                      InlineKeyboardButton,
                      InlineQueryResultArticle,
                      InputTextMessageContent)
from telegram.error import BadRequest
import logging
from telegram.ext import CommandHandler, CallbackContext, InlineQueryHandler, CallbackQueryHandler
from LibGenBot import updater, dp
from LibGenBot.plugins.strings import *
from libgen_api import LibgenSearch
from uuid import uuid4

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def search_book_title(text, user):
    try:
        res = LibgenSearch().search_title(text)
        return res
    except IndexError:
        logger.info(f'@{user} is Searching....')


def search_book_author(text, user):
    try:
        res = LibgenSearch().search_author(text)
        return res
    except IndexError:
        logger.info(f'@{user} is Searching....')


def result_article(update: Update, context: CallbackContext, books_list):
    res = []
    for i in range(0, len(books_list)):
        title = books_list[i]['Title']
        author = books_list[i]['Author']
        publisher = books_list[i]['Publisher']
        pages = books_list[i]['Pages']
        lang = books_list[i]['Language']
        year = books_list[i]['Year']
        taipe = books_list[i]['Extension'].upper()
        size = books_list[i]['Size']
        dwn_links = [books_list[i]['Mirror_1'], books_list[i]['Mirror_2'], books_list[i]['Mirror_3'],
                     books_list[i]['Mirror_4'], books_list[i]['Mirror_5']]
        res.append(
            InlineQueryResultArticle(id=uuid4(),
                                     title=title,
                                     input_message_content=InputTextMessageContent(
                                         message_text=BOOK_MSG.format(
                                             title, author, lang, year, pages, size, taipe),
                                         parse_mode=ParseMode.MARKDOWN
                                     ),
                                     reply_markup=InlineKeyboardMarkup(
                                         [
                                             [
                                                 InlineKeyboardButton('Mirror 1', url=dwn_links[0]),
                                                 InlineKeyboardButton('Mirror 2', url=dwn_links[1]),
                                                 InlineKeyboardButton('Mirror 3', url=dwn_links[2]),
                                             ],
                                             [
                                                 InlineKeyboardButton('Mirror 4', url=dwn_links[3]),
                                                 InlineKeyboardButton('Mirror 5', url=dwn_links[4]),
                                             ],
                                         ]
                                     ),
                                     description=f"{author} | {lang} | {year} | {taipe}"
                                     )
        )
    return res


def inline_search_book(update: Update, context: CallbackContext):
    user = update.effective_user.username
    query = update.inline_query.query
    to_search = ['author', 'title']
    if to_search[1] in query:
        res = result_article(update, context,  search_book_title(query.replace('title ', ''), user))
        try:
            update.inline_query.answer(res, auto_pagination=True)
            logger.info(f'@{user} searched {query} ..')
        except (TypeError, IndexError, BadRequest):
            logger.info('Idle...')
    elif to_search[0] in query:
        res = result_article(update, context, search_book_author(query.replace('author ', ''), user))
        try:
            update.inline_query.answer(res, auto_pagination=True)
            logger.info(f'@{user} searched {query} ..')
        except (TypeError, IndexError, BadRequest):
            logger.info('Idle...')
    else:
        res = []
        for i in range(0, len(to_search)):
            res.append(
                InlineQueryResultArticle(id=uuid4(), title=to_search[i],
                                         input_message_content=InputTextMessageContent(message_text=
                                                                                       'Click the Button below'),
                                         reply_markup=InlineKeyboardMarkup(
                                             [
                                                 [InlineKeyboardButton(f"Search {to_search[i]}",
                                                                       switch_inline_query_current_chat=
                                                                       to_search[i] + " ")]
                                             ]
                                         ))
            )
        update.inline_query.answer(results=res)


def search_btn_clicked(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Search by Author", switch_inline_query_current_chat='author '),
             InlineKeyboardButton('Search by Title', switch_inline_query_current_chat='title ')],
            [InlineKeyboardButton('🔙', callback_data='back_to_start')],
        ]
    )
    query.message.edit_text("You can search by two methods,\n"
                            "1. Search by Title\n"
                            "2. Search by Author.",
                            reply_markup=keyboard)


def back_to_start(update: Update, context: CallbackContext):
    query = update.callback_query
    st = Start(context.bot.username)
    user = update.effective_user.username
    logger.info(f'@{user} pressed /start ...')
    query.message.edit_text(text=st.msg,
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=st.keyboard)


class Start:
    def __init__(self, bot_username):
        self.keyboard = InlineKeyboardMarkup(
                                  [
                                      [InlineKeyboardButton('Github', url=GITHUB_URL),
                                       InlineKeyboardButton('Developer', url=TG_URL)],
                                      [InlineKeyboardButton('Search 🔍', callback_data='by_title_or_author')],
                                  ]
                              )
        self.msg = START_MSG.format(bot_username)


def start(update: Update, context: CallbackContext):
    st = Start(context.bot.username)
    user = update.effective_user.username
    logger.info(f'@{user} pressed /start ...')
    update.message.reply_text(text=st.msg,
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=st.keyboard)


def main():
    dp.add_handler(CallbackQueryHandler(back_to_start, pattern='back_to_start'))
    dp.add_handler(CallbackQueryHandler(search_btn_clicked, pattern='by_title_or_author'))
    dp.add_handler(CommandHandler('start', start, run_async=True))
    dp.add_handler(InlineQueryHandler(inline_search_book, run_async=True))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

