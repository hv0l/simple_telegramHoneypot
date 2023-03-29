import socket
import threading
import datetime
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import matplotlib.pyplot as plt
import os
import tempfile
from telegram import CallbackQuery
from telegram.ext import CallbackQueryHandler





TELEGRAM_API_TOKEN = 'YOUR_TELEGRAM_API_TOKEN'
TELEGRAM_USER_ID = 'YOUR_TELEGRAM_USER_ID'
bot = Bot(token=TELEGRAM_API_TOKEN)
updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)



access_attempts = []




def handle_connection(client_socket, client_address):
    global access_attempts
    attempt_counter = 0
    while True:
        data = client_socket.recv(1024)
        attempt_counter += 1
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        access_attempts.append((timestamp, client_address[0], client_address[1]))
        message = f"New connection attempt:\nTimestamp: {timestamp}\nAttempt: {attempt_counter}\nIP: {client_address[0]}\nPort: {client_address[1]}\nData: {data}"
        bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)
        if not data:
            break
    client_socket.close()

    
    
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Listening on port {port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        connection_thread = threading.Thread(target=handle_connection, args=(client_socket, client_address))
        connection_thread.start()

        
        
def start_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("graph", callback_data='graph'),
         InlineKeyboardButton("history", callback_data='history')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Select an option:', reply_markup=reply_markup)

    
def graph_command(update: Update, context: CallbackContext):
    global access_attempts
    if not access_attempts:
        update.message.reply_text('No access attempts to show.')
        return

    
    ip_count = {}
    for _, ip, _ in access_attempts:
        ip_count[ip] = ip_count.get(ip, 0) + 1

        
    plt.figure(figsize=(10, 5))
    plt.bar(ip_count.keys(), ip_count.values())
    plt.xlabel('IP Address')
    plt.ylabel('Access Attempts')
    plt.title('Access Attempts by IP Address')

    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        plt.savefig(temp_file.name, format='png')
        temp_file.close()
        with open(temp_file.name, 'rb') as img_file:
            bot.send_photo(chat_id=TELEGRAM_USER_ID, photo=img_file)
        os.unlink(temp_file.name)

        
def history_command(update: Update, context: CallbackContext):
    global access_attempts
    if not access_attempts:
        update.message.reply_text('No access attempts to show.')
        return

    
    history_text = "Access attempts:\n\n"
    for timestamp, ip, _ in access_attempts:
        history_text += f"{timestamp} - {ip}\n"

        
    update.message.reply_text(history_text)


    
def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'graph':
        graph_command(query, context)
    elif query.data == 'history':
        history_command(query, context)

        
        
        
def main():
    updater.dispatcher.add_handler(CommandHandler('start', start_command))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_callback))
    
    ports = [80, 22, 23]
    for port in ports:
        server_thread = threading.Thread(target=start_server, args=(port,))
        server_thread.start()

    updater.start_polling()

if __name__ == "__main__":
    main()
