from telegram import InlineKeyboardButton

from config import Config


class BotKeyboard:
    # Start #
    StartKeyBoard = [
        [
            InlineKeyboardButton("🛍 Shop 🛍", callback_data='shop')
        ],
        [
            InlineKeyboardButton("🆘 Support 🆘", url=Config.help_link)
        ]
    ]

    # Account #
    _AccountKeyBoard = [
        [
            InlineKeyboardButton("{0} {1} {0}".format(
                Config.shop_account[account]['emoji'], account
            ), callback_data=f'account-{account}')
            
        ] for account in Config.shop_account.keys()
    ]
    _AccountKeyBoard.append([
        InlineKeyboardButton("🏘 Home 🏘", callback_data='back-to-home')
    ])
    AccountKeyBoard = _AccountKeyBoard

    # PeyMethod #
    PayMethodKeyBoard = [
        [
            InlineKeyboardButton("🅿️ PayPal 🅿️", callback_data='pay-PayPal'),
        ],
        [
            InlineKeyboardButton("🅰️ Amazon voucher 🅰️", callback_data='pay-Amazon'),
            InlineKeyboardButton("💶 PaySafeCard 💶", callback_data='pay-PaySafeCard')
        ],
        [
            InlineKeyboardButton("◀️ Back ◀️", callback_data='back-to-account')
        ]
    ]

    # Pay #
    PayKeyBoard = [
        [
            InlineKeyboardButton("🆘 Support 🆘", url=Config.help_link)
        ],
        [
            InlineKeyboardButton("◀️ Back ◀️", callback_data='back-to-plan')
        ]
        
    ]

    # BackhomeKeyBoard #
    BackhomeKeyBoard = [
        [
            InlineKeyboardButton("🏘 Home 🏘", callback_data='back-to-home')
        ]
    ]

    # JoinChannelKeyBoard #
    JoinChannelKeyBoard = [
        [
            InlineKeyboardButton("Join now", url=Config.channel_link)
        ]
    ]