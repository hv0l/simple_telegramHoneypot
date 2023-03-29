import datetime
from flask import Flask, request
from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

app = Flask(__name__)

# Replace with your Telegram API token
TELEGRAM_API_TOKEN = 'YOUR_TELEGRAM_API_TOKEN'

bot = Bot(token=TELEGRAM_API_TOKEN)
updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)

# Replace with your Telegram user ID
TELEGRAM_USER_ID = 'YOUR_TELEGRAM_USER_ID'

attempt_counter = 0

@app.route("/", methods=["GET", "POST"])
def handle_request():
    global attempt_counter
    attempt_counter += 1

    ip = request.remote_addr
    headers = request.headers
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    message = f"New connection attempt:\nTimestamp: {timestamp}\nAttempt: {attempt_counter}\nIP: {ip}\nHeaders:\n{headers}"
    bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)

    return "OK"

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text('Bot started.')

def main():
    updater.dispatcher.add_handler(CommandHandler('start', start_command))

    updater.start_polling()
    app.run(host="0.0.0.0", port=80)

if __name__ == "__main__":
    main()
