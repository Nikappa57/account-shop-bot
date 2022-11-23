class Config:
    channel_log = "" # Your private channel-id
    channel = "" # @channel Your pubblic channel-id
    channel_link = "" # Link to your pubblich channel (t.me/...)
    admin_chat_id = "" # Your chat-id

    shop_account = {
        'Netflix': {'pricing': [2.99, 14.99, 19.99], 'emoji': '⁣:movie_camera:'},
        'Spotify': {'pricing': [1.99, 6.99, 9.99], 'emoji': ':headphones:'},
        'Infinity': {'pricing': [1.99, 6.99, 9.99], 'emoji': ':video_camera:'},
        'DaznIT': {'pricing': [1.49, 5.99, 8.99], 'emoji': ':soccer:'},
        'DaznDE': {'pricing': [1.49, 5.99, 8.99], 'emoji': ':soccer:'}
    }

    paypal_account = "" # PayPal link for buyers

    give_account = {
        'netflix': {'img': 'https://i.imgur.com/4aqCR4U.jpg', 'emoji': '⁣:movie_camera:'},
        'nowtv': {'img': 'https://i.imgur.com/j7OPWza.jpg', 'emoji': ':tv:'},
        'spotify': {'img': 'https://i.imgur.com/5Sjrhvm.jpg1', 'emoji': ':headphones:'},
        'infinity': {'img': 'https://i.imgur.com/4H3ZNC8.jpg', 'emoji': ':video_camera:'},
        'dazn': {'img': 'https://i.imgur.com/YmyWHq0.jpg', 'emoji': ':soccer:'}
    }

    bot_username = "" # without @
    help_link = "" # generic link (also t.me/...)
    guide = "" # @cannel of your guide

# Remember to setup /Bot/static/logo.jpg
# ad define your token in .env