import re

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

from Bot.decorator import checkuser, chattype
from Bot.database import db
from Bot.database.models import Users
from Bot.utils.bot_emoji import Emoji
from Bot.keyboard import BotKeyboard
from Bot.utils.chat import Chat
from config import Config


@checkuser.check()
def button(update, context, currentuser) :
    query = update.callback_query
    data = query.data
    bot = context.bot

    chat_id = update.effective_chat.id
    name = update.effective_chat.first_name
    username = update.effective_chat.username    

    if data == "back-to-home":
        bot.delete_message(
            chat_id=chat_id, 
            message_id=update.callback_query.message.message_id,
        )

        reply_markup = InlineKeyboardMarkup(BotKeyboard.StartKeyBoard)

        mex = f"{Emoji.robot}<i>Welcome to @{Config.bot_username}</i>\n\n{Emoji.eyes}" + \
            "<i>Below are buttons for moving in the Bot.</i>"

        context.bot.send_photo(
            chat_id=chat_id, 
            caption=mex, 
            photo=open('./Bot/static/logo.jpg', 'rb'),
            reply_markup=reply_markup
        )

        # delete dict #
        if chat_id in Chat.buying.keys():
            del Chat.buying[chat_id]

    elif data == "shop" or data == "back-to-shop":
        if data == "shop":
            bot.delete_message(
                chat_id=chat_id, 
                message_id=update.callback_query.message.message_id,
            )

        reply_markup = InlineKeyboardMarkup(BotKeyboard.AccountKeyBoard)

        mex = f"{Emoji.bags}<b>Welcome to our shop</b>{Emoji.bags}\n\n{Emoji.flash}" + \
            "<i>Select our service below.</i>"

        bot.send_message(chat_id, mex, reply_markup=reply_markup)

        # delete dict #
        if chat_id in Chat.buying.keys():
            del Chat.buying[chat_id]

    elif data[:8] == "account-" or (data == "back-to-account" and chat_id in Chat.buying.keys()):
        account = data[8:] if data[:8] == "account-" else Chat.buying[chat_id]['Account']
        price = Config.shop_account[account]['pricing']
        
        # Plan #
        PlanKeyBoard = [
            [
                InlineKeyboardButton(f"1 Month ({price[0]}€)", callback_data='plan-0'),
                InlineKeyboardButton(f"6 Months ({price[1]}€)", callback_data='plan-1')
            ],
            [
                InlineKeyboardButton(f"{Emoji.orange_diamond} 1 Year ({price[2]}€) {Emoji.orange_diamond}", callback_data='plan-2')
            ],
            [
                InlineKeyboardButton(f"{Emoji.back} Back {Emoji.back}", callback_data='back-to-shop')
            ],
        ]

        reply_markup = InlineKeyboardMarkup(PlanKeyBoard)

        mex = f"{Emoji.gift}<b>Select a subscription</b>{Emoji.gift}\n\n<i>Here are our available subscriptions:</i>" + \
            f"\n\n{Emoji.blue_diamond}<b>Monthly</b>\n{Emoji.blue_diamond}<b>half-yearly</b>\n{Emoji.orange_diamond}<b>Annual</b> <i>recommended</i>"

        context.bot.editMessageText(
            message_id = update.callback_query.message.message_id,
            chat_id = update.callback_query.message.chat.id,
            text = mex,
            reply_markup=reply_markup
        )

        account = account if data[:8] == "account-" else Chat.buying[chat_id]['Account']

        # save new info #
        Chat.buying[chat_id] = {'Account': account, 'Plan': None}

    elif (data[:5] == "plan-" or data == "back-to-plan") and chat_id in Chat.buying.keys():
        plan = int(data[5:]) if data[:5] == "plan-" else Chat.buying[chat_id]['Plan']
        account = Chat.buying[chat_id]['Account']
        price = Config.shop_account[account]['pricing'][plan]

        reply_markup = InlineKeyboardMarkup(BotKeyboard.PayMethodKeyBoard)

        mex = f"{Emoji.card}<b>Payment method</b>{Emoji.card}\n\n<i>Select a payment method.</i>"

        context.bot.editMessageText(
            message_id = update.callback_query.message.message_id,
            chat_id = update.callback_query.message.chat.id,
            text = mex,
            reply_markup=reply_markup
        )

        Chat.buying[chat_id]['Plan'] = plan

    elif data[:4] == "pay-":
        method = data[4:]
        account = Chat.buying[chat_id]['Account']
        price = Config.shop_account[account]['pricing'][Chat.buying[chat_id]['Plan']]

        reply_markup = InlineKeyboardMarkup(BotKeyboard.PayKeyBoard)

        mex_add = f"Now send the screen of the Voucher <b>Amazon</b> of {price} €." if method == "Amazon" else \
            f"Now send the screen of the <b>PaySafeCard Code</b> di {price} €." if method == "PaySafeCard" else \
                f"Now pay {price} € on <a href='{Config.paypal_account}'>this Paypal</a> and send the screen."

        mex = f"{Emoji.money}<b>CHECKOUT</b>{Emoji.money}\n\n{Emoji.check}<b>Perfect</b> {mex_add}\n\n<b>{Emoji.bell}" + \
            "If you’re having trouble paying, contact Support.</b>"

        context.bot.editMessageText(
            message_id = update.callback_query.message.message_id,
            chat_id = update.callback_query.message.chat.id,
            text = mex,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    elif data[:12] == 'renewAccout-':
        args = data[12:].split("-") #Account-Expiried
        
        reply_markup = InlineKeyboardMarkup(BotKeyboard.BackhomeKeyBoard)

        context.bot.editMessageText(
            message_id = update.callback_query.message.message_id,
            chat_id = update.callback_query.message.chat.id,
            text = f"{Emoji.check}<b>Account required</b>{Emoji.check}\n\n<i>" + \
                "An admin will verify your request, and send you the account.</i>",
            reply_markup=reply_markup
        )

        Account = args[0]
        expiried = args[1]

        mex = f"{username} {name} [{chat_id}]\n\nRequires the new account {Account} ({expiried})"
        mex = "@" + mex if username else mex

        SendAccountKeyBoard = [
            [
                InlineKeyboardButton("Send Account", url=f"t.me/{Config.bot_username}?start=renewAccount_{chat_id}_{Account}")
            ],
        ]

        reply_markup = InlineKeyboardMarkup(SendAccountKeyBoard)

        context.bot.send_message(
            chat_id=Config.channel_log,
            text=mex,
            reply_markup=reply_markup
        )

        # delete dict #
        if chat_id in Chat.buying.keys():
            del Chat.buying[chat_id]  

    query.answer()
