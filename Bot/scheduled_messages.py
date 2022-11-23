from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from Bot.keyboard import BotKeyboard
from Bot.utils.bot_emoji import Emoji

def expiried_account(context: CallbackContext):
    reply_markup = InlineKeyboardMarkup(BotKeyboard.StartKeyBoard)

    mex = f"{Emoji.eye}<b>YOUR SUBSCRIPTION HAS EXPIRED</b>{Emoji.eye}\n\n{Emoji.check}" + \
            "<i>Click the button below to buy another subscription</i>"
    context.bot.send_message(
        chat_id=context.job.context, 
        text=mex,
        reply_markup=reply_markup,
    )


def renew_account(context: CallbackContext):
    chat_id = context.job.context[0]
    account = context.job.context[1]
    time_expiried = context.job.context[2]

    # Renew Account #
    RenewAccountKeyBoard = [
        [
            InlineKeyboardButton("Request Account", callback_data=f'renewAccout-{account}-{time_expiried}')
        ],
    ]

    reply_markup = InlineKeyboardMarkup(RenewAccountKeyBoard)

    mex = f"{Emoji.plug}<b>YOUR ACCOUNT {account} HAS EXPIRED</b>{Emoji.plug}\n\n{Emoji.check}" + \
            "<i>Click the button below to renew it</i>"

    context.bot.send_message(
        chat_id, 
        mex,
        reply_markup=reply_markup,
    )
