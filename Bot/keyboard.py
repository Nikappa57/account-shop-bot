from telegram import InlineKeyboardButton

from Bot.utils.bot_emoji import Emoji
from config import Config
from emoji import emojize

class BotKeyboard:
    # Start #
    StartKeyBoard = [
        [
            InlineKeyboardButton(f"{Emoji.bags} Shop {Emoji.bags}", callback_data='shop')
        ],
        [
            InlineKeyboardButton(f"{Emoji.sos} Support {Emoji.sos}", url=Config.help_link)
        ]
    ]

    # Account #
    _AccountKeyBoard = [
        [
            InlineKeyboardButton("{0} {1} {0}".format(
                emojize(Config.shop_account[account]['emoji'], language='alias'), account
            ), callback_data=f'account-{account}')
            
        ] for account in Config.shop_account.keys()
    ]
    _AccountKeyBoard.append([
        InlineKeyboardButton(f"{Emoji.house} Home {Emoji.house}", callback_data='back-to-home')
    ])
    AccountKeyBoard = _AccountKeyBoard

    # PeyMethod #
    PayMethodKeyBoard = [
        [
            InlineKeyboardButton(f"{Emoji.p} PayPal {Emoji.p}", callback_data='pay-PayPal'),
        ],
        [
            InlineKeyboardButton(f"{Emoji.a} Amazon voucher {Emoji.a}", callback_data='pay-Amazon'),
            InlineKeyboardButton(f"{Emoji.euro} PaySafeCard {Emoji.euro}", callback_data='pay-PaySafeCard')
        ],
        [
            InlineKeyboardButton(f"{Emoji.back} Back {Emoji.back}", callback_data='back-to-account')
        ]
    ]

    # Pay #
    PayKeyBoard = [
        [
            InlineKeyboardButton(f"{Emoji.sos} Support {Emoji.sos}", url=Config.help_link)
        ],
        [
            InlineKeyboardButton(f"{Emoji.back} Back {Emoji.back}", callback_data='back-to-plan')
        ]
        
    ]

    # BackhomeKeyBoard #
    BackhomeKeyBoard = [
        [
            InlineKeyboardButton(f"{Emoji.house} Home {Emoji.house}", callback_data='back-to-home')
        ]
    ]

    # JoinChannelKeyBoard #
    JoinChannelKeyBoard = [
        [
            InlineKeyboardButton("Join now", url=Config.channel_link)
        ]
    ]