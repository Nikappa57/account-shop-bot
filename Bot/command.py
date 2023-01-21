from random import randint

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from Bot.errors import unknown
from Bot.decorator import chattype, checkuser
from Bot.database.models import Users, Account
from Bot.database import db
from Bot.keyboard import BotKeyboard
from Bot.utils.chat import Chat


# start #
@chattype.private
@checkuser.check()
def start(update, context, currentuser):
    message = update.message.text
    if not context.bot.get_chat_member(Config.channel, 
        currentuser.chat_id).status in ['member', 'creator', 'administrator']:
        update.message.reply_text(
            "🚫<b>HEY</b>🚫\n\n🔒To access this bot," + \
                " you have to join our Telegram channel.\n⬇️Click below!", 
            reply_markup=InlineKeyboardMarkup(BotKeyboard.JoinChannelKeyBoard)
        )
        return
    
    ### ADMIN ###
    if currentuser.admin:
        args = context.args[0].split("_") if "_" in message else None
        if not args:
            update.message.reply_text("welcome back Admin")
        elif args[0] == "sendAccount":
            Chat.sendAccount[currentuser.chat_id] = {
                'chat_id': int(args[1]), 'Plan': int(args[2]), 
                    'Account': args[3], 'Renew': False}
            update.message.reply_text("Now send the account")
        elif args[0] == "renewAccount":
            Chat.sendAccount[currentuser.chat_id] = {'chat_id': int(args[1]), 
                'Renew': True, 'Account': args[2]}
            update.message.reply_text("Now send the account")
        else:
            update.message.reply_text("You are admin, you cannot take accounts")

    elif "_" not in message:
        reply_markup = InlineKeyboardMarkup(BotKeyboard.StartKeyBoard)
        mex = f"🤖<i>welcome to @{Config.bot_username}!</i>\n\n👀" + \
                "<i>Below are buttons for moving in the Bot.</i>"

        context.bot.send_photo(
            chat_id=currentuser.chat_id, 
            caption=mex, 
            photo=open('./Bot/static/logo.jpg', 'rb'),
            reply_markup=reply_markup,
        )
            
        # delete dict #
        if currentuser.chat_id in Chat.buying.keys():
            del Chat.buying[currentuser.chat_id]

    else:
        # Give Account #
        args = context.args[0].split("_")
        try:
            if args[0] == "give":
                if args[1] == "Taken":
                    reply_markup = InlineKeyboardMarkup(BotKeyboard.StartKeyBoard)
                    mex = "❗️ <b>WE'RE SORRY</b> ❗️\n\n✖️ " + \
                            "<b>Another user before you, has redeemed the account.</b>\n\n" + \
                                "<i>Can’t get an account for free?</i>\n<i>Click on the Shop!</i>"
                    context.bot.send_message(
                        chat_id=currentuser.chat_id, 
                        text=mex,
                        reply_markup=reply_markup,
                    )   
                else:
                    messageId = args[2]
                    url = f't.me/{Config.bot_username}?start=give_Taken'
                    keyboard = [
                        [
                            InlineKeyboardButton("Unlock", url=url)
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    context.bot.editMessageReplyMarkup(
                        message_id = messageId,
                        chat_id = Config.channel,
                        reply_markup=reply_markup
                    )

                    account = db.session.query(Account).get(args[1])

                    mex = f"💎<b>WOW!</b>💎\n\n🎁<i>You managed to catch the account {account.account_type} " + \
                            f"in time.</i>\n\n📨 <code>{account.email}</code>\n🔒 <code>{account.temp_password}</code>" + \
                                f"\n\n✋ Before logging into the account {account.account_type}, follow our procedure\n>> {Config.guide}"

                    context.bot.send_message(
                        currentuser.chat_id,
                        mex,
                    )
        except:
            unknown(update, context)

@chattype.private
@checkuser.check(adminrequired=True)
def giveAccount(update, context, currentuser):
    args = update.message.text.split(" ")

    if len(args) == 4:
        account_type = args[1]
        account_email = args[2]
        account_password = str(randint(100, 999)) + args[3]

        if account_type.lower() in Config.give_account.keys():
            img = f"<a href='{Config.give_account[account_type.lower()]['img']}'> </a>"

            emoji = Config.give_account[account_type.lower()]['emoji']

            mex = f"{emoji} <b>{account_type.upper()} PRIVATE</b>\n\n❗️" + \
                    "<i>Click below to take the account</i>" + img

            new_account = Account(
                email=account_email, 
                temp_password=account_password, 
                account_type=account_type
            )
            db.session.add(new_account)
            db.session.commit()

            # KeyBoard #
            keyboard = [
                [
                    InlineKeyboardButton("Unlock", url=f't.me/{Config.bot_username}'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            messageId = context.bot.send_message(Config.channel, mex, reply_markup=reply_markup)

            # KeyBoard #
            url = f't.me/{Config.bot_username}?start=give_{new_account.id}_{messageId.message_id}'

            keyboard = [
                [
                    InlineKeyboardButton("🔒 Unlock 🔒", url=url)
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            context.bot.editMessageReplyMarkup(
                message_id = messageId.message_id,
                chat_id=Config.channel,
                reply_markup=reply_markup
            )

            context.bot.send_message(update.effective_chat.id, "Message sent on the channel")
        else:
            context.bot.send_message(
                update.effective_chat.id,
                "Account not supported.\nAccount supported:\n\n{}".format(
                    '  '.join(str(e) for e in [account for account in Config.give_account.keys()])
                )
            )
    else:
         context.bot.send_message(update.effective_chat.id, "Wrong command, use /give 'account type' 'email' 'password'")

         
# admin #

@chattype.private
@checkuser.check(adminrequired=True)
@checkuser.user_arg
def ban(update, context, currentuser, user):
    user.ban = True
    user.save()

    update.message.reply_text(
        'The user has been banned.'
    )


@chattype.private
@checkuser.check(adminrequired=True)
@checkuser.user_arg
def unban(update, context, currentuser, user):
    user.ban = False
    user.save()

    update.message.reply_text(
        'User unban with success.'
    )


@chattype.private
@checkuser.check(adminrequired=True)
def users(update, context, currentuser):
    update.message.reply_text('Users:\n{}'.format(
        "\n".join(f"{number} - {user}" for number, user in enumerate(db.session.query(Users).all()))))


@chattype.private
@checkuser.check(adminrequired=True)
@checkuser.user_arg
def admin(update, context, currentuser, user):
    user.admin = True
    user.save()
    
    update.message.reply_text(
        "The user has become an admin."
    )


@chattype.private
@checkuser.check(adminrequired=True)
@checkuser.user_arg
def unadmin(update, context, currentuser, user):
    user.admin = False
    user.save()

    update.message.reply_text(
        "The user has been demoted."
    )


@chattype.private
@checkuser.check(adminrequired=True)
@checkuser.user_arg
def info(update, context, currentuser, user):
    update.message.reply_text(
        str(user)
    )
