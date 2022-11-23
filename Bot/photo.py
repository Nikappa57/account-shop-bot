from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from Bot.decorator import chattype, checkuser

from config import Config
from Bot.utils.chat import Chat
from Bot.keyboard import BotKeyboard
from Bot.utils.bot_emoji import Emoji

@chattype.private
@checkuser.check()
def paymentScreen(update, context, currentuser):
    chat_id = currentuser.chat_id

    if chat_id in Chat.buying.keys() and Chat.buying[chat_id]['Plan'] is not None:
        plan = "1 month" if not Chat.buying[chat_id]['Plan'] else "6 months" if Chat.buying[chat_id]['Plan'] == 1 else "1 year"

        img = update.message['photo'][0]['file_id']
        mex = f"{currentuser.get_name()}  [{chat_id}]\n\nAccount: {Chat.buying[chat_id]['Account']}\nPlan: {plan}"
        url = f"t.me/{Config.bot_username}?start=sendAccount_{chat_id}_{Chat.buying[chat_id]['Plan']}_{Chat.buying[chat_id]['Account']}"
        SendAccountKeyBoard = [
            [
                InlineKeyboardButton("Send Account", url=url)
            ],
        ]

        reply_markup = InlineKeyboardMarkup(SendAccountKeyBoard)

        context.bot.send_photo(
            chat_id=Config.channel_log,
            caption=mex,
            photo=img,
            reply_markup=reply_markup
        )

        reply_markup = InlineKeyboardMarkup(BotKeyboard.BackhomeKeyBoard)
        
        mex = f"{Emoji.point} <b>YOU PAID YOUR ACCOUNT CORRECTLY</b> {Emoji.point}\n\n{Emoji.worning} " + \
                "<i>An admin will verify your order, and send you the login details of the requested account.</i>" + \
                    f"\n\n{Emoji.clock} <i>It could take</i> <b>more than 48h.</b>"

        context.bot.send_message(
            chat_id=chat_id,
            text=mex,
            reply_markup=reply_markup
        )

        # delete dict #
        if chat_id in Chat.buying.keys():
            del Chat.buying[chat_id]