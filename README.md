# Telegram Account Give and Shop Bot

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/Nikappa57/account-shop-bot?style=for-the-badge) ![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/Nikappa57/account-shop-bot/python-telegram-bot?style=for-the-badge) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Nikappa57/account-shop-bot?style=for-the-badge) ![GitHub](https://img.shields.io/github/license/Nikappa57/tg-bot-bootstrap?style=for-the-badge)

A telegram bot for account sales channels.

This bot uses my base 
[g-bot-bootstrap](https://github.com/Nikappa57/tg-bot-bootstrap).
## Features
- all the basic features of [g-bot-bootstrap](https://github.com/Nikappa57/tg-bot-bootstrap)
- a shop to buy account
- create a public give on your channel
the user will be sent to the bot and the first will take the credentials in private chat
- monthly account expiration management

## Installation

1. Clone this repo: 
```console
git clone https://github.com/Nikappa57/account-shop-bot.git
```
2. Install requirements.
```console
pipenv install
pipenv shell
```

#### Setup
Create `.env` with your bot token 
```
TOKEN=yourtoken
```

Put your logo in `Bot/static/logo.jpg`.

Configure `config.py` with your information.

Now you should be able to start your bot.
```console
python run.py