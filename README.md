# simple_telegramHoneypot

# Honeypot on Linux with Telegram Notifications

This simple honeypot listens on port 80, 22 and 23 and sends a message to your Telegram account with information about incoming connection attempts. The message includes the timestamp, attempt count, IP address, and request headers.

## Setup

1. Install Python (if not already installed) and create a virtual environment:

```
sudo apt-get update
sudo apt-get install python3-venv
python3 -m venv my_honeypot
source my_honeypot/bin/activate
```


2. Install the necessary libraries:

```
pip install Flask python-telegram-bot
```


3. Create a bot on Telegram:

- Start a chat with the BotFather on Telegram.
- Send the `/newbot` command to create a new bot.
- Choose a name and username for your bot.
- You will receive an API token for your bot. Copy it, as you will need it later.

4. Edit the `honeypot.py` file and replace `'YOUR_TELEGRAM_API_TOKEN'` with your Telegram API token and `'YOUR_TELEGRAM_USER_ID'` with your Telegram user ID.

5. To find your Telegram user ID, you can use the `@userinfobot` bot. Start a chat with it and send the `/start` command. You will receive your user ID.

6. Run the `honeypot.py` script:

```
python honeypot.py
```

The honeypot is now active and listening on port 80, 22 and 23. When someone tries to view the content, you will receive a message on Telegram with information about the request.



![Schermata del 2023-03-29 18-18-55](https://user-images.githubusercontent.com/61795418/228603039-5552993a-4dbd-407c-bebe-3d9a6bc10e8b.png)
