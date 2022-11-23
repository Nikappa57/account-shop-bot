import os
import logging
from dotenv import load_dotenv
from inspect import getmembers, isfunction

from telegram.ext import Defaults, Updater, CommandHandler, MessageHandler, \
    Filters, CallbackQueryHandler, InlineQueryHandler
from telegram import ParseMode

from config import Config
from Bot import command
from Bot.errors import unknown
from Bot.buttons import button
from Bot.photo import paymentScreen
from Bot.message import accountMessage
from Bot.database.models import Users, db

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

if __name__ == "__main__":
    print("loading...")

    TOKEN = os.environ.get('TOKEN')
    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(token=TOKEN, defaults=defaults, use_context=True)
    dispatcher = updater.dispatcher

    # Commands #
    for name, handler in [o for o in getmembers(command) if isfunction(o[1])]:
        dispatcher.add_handler(CommandHandler(name, handler))

    # Buttons #
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # Unknown Command #
    dispatcher.add_handler(
        MessageHandler(Filters.command & Filters.private, unknown)
    )

    ### IMAGE ####
    dispatcher.add_handler(
        MessageHandler(Filters.photo, paymentScreen)
    )

    ### MESSAGE ###
    dispatcher.add_handler(
        MessageHandler(Filters.text, accountMessage)
    )

    updater.start_polling()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    jobs = updater.job_queue

    # Check Admin #
    user = db.session.query(Users).filter_by(chat_id=Config.admin_chat_id).first()
    if not user:
        user = Users(chat_id=Config.admin_chat_id)
        db.session.add(user)
        db.session.commit()

    if not user.admin:
        user.admin = True
        user.save()

    print("Bot started")
