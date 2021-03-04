from telegram import (Update,
                      ParseMode,
                      InlineKeyboardMarkup,
                      InlineKeyboardButton,
                      InlineQueryResultArticle,
                      InputTextMessageContent)
from telegram.error import BadRequest
import logging
from telegram.ext import CommandHandler, CallbackContext, InlineQueryHandler
from LibGenBot import updater, dp
from LibGenBot.plugins.strings import *
from libgen_api import LibgenSearch
from uuid import uuid4


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def search_book(text, user):
    try:
        res = LibgenSearch().search_title(text)
        return res
    except IndexError:
        logger.info(f'@{user} is Searching....')


def inline_search_book(update: Update, context: CallbackContext):
    query = update.inline_query.query
    user = update.effective_user.username
    try:
        books_list = search_book(query, user)
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
            update.inline_query.answer(res, auto_pagination=True)
            logger.info(f'@{user} searched {title} ..')
    except (TypeError, IndexError, BadRequest):
        logger.info('Idle...')


def start(update: Update, context: CallbackContext):
    user = update.effective_user.username
    logger.info(f'@{user} pressed /start ...')
    update.message.reply_text(text=START_MSG.format(context.bot.username),
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=InlineKeyboardMarkup(
                                  [
                                      [InlineKeyboardButton('Github', url=GITHUB_URL),
                                       InlineKeyboardButton('Developer', url=TG_URL)],
                                      [InlineKeyboardButton('Search 🔍', switch_inline_query_current_chat='')],
                                  ]
                              ))


def main():
    dp.add_handler(CommandHandler('start', start, run_async=True))
    dp.add_handler(InlineQueryHandler(inline_search_book, run_async=True))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

