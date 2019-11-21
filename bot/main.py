# main.py
# Made by S@n1X-d4rk3r
# This is the core where anything is done

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, RegexHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

import logging
from datetime import datetime
import sqlite3
import configparser as ConfigParser
import json
import requests

conn = sqlite3.connect('./chatid.db')
c = conn.cursor()
c.execute('create table if not exists chatid_table (chatid string, last_confession string, username string, _date string)')
conn.commit()
c.close()

with open('logs.log', 'w') as fill: fill.write(".")

# Create a custom logger
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
# Create handlers
f_handler = logging.FileHandler('logs.log')
# Create formatters and add it to handlers
f_format = logging.Formatter(' %(asctime)s > %(process)d-%(levelname)s-%(message)s')
f_handler.setFormatter(f_format)
# Add handlers to the logger
logger.addHandler(f_handler)

separator = "# -------------------------------------------------------------"

# Configs parameters configParser.get('your-config', 'path1')
configParser = ConfigParser.RawConfigParser()
configFilePath = r'config.txt'
configParser.read(configFilePath)
# Configs parameters
TOKEN = configParser.get('jcf-config', 'token')


# Lang management
def get_lang_string_by_code(lang_code, code):
    with open('lang/'+lang_code+'.json', 'r+', encoding='utf-8') as f:
        lang_string = json.load(f)
        return lang_string[code]

def presentation():
    #os.system("clear")
    print(separator)
    print("[+] # ----------------- JeudiConfessionBot Started! -----------")
    print(separator)
    print("[+] #                                      By 🐼Sanix darker")
    print(separator)

# To print a log and save it in logs.log
def printLog(command, Telegram_user):
    tolog = command + " by: first_name: {}, last_name: {}, username: {}, language_code: {}, is_bot: {}".format(str(Telegram_user.first_name),
                                                                                                                str(Telegram_user.last_name),
                                                                                                                str(Telegram_user.username),
                                                                                                                str(Telegram_user.language_code),
                                                                                                                str(Telegram_user.is_bot))
    logger.info(tolog)
    print(tolog)

# To rejects other bots that wanted to query the bot
def reject_bots(bot, update):
    if(update.message.from_user.is_bot == True):
        logger.info(("OUPS BOT, not authorized here!"))
        bot.send_message(chat_id=update.message.chat_id,
                            text="NOT AUTHORIZED")
        return False

    return True


# ---------------------------------------------
# -----------COMMAND CALLBACK -----------------
# ---------------------------------------------
# message = telegram.Message(
#     message_id=0,
#     from_user=telegram.User(0, 'greenkey'),
#     date=datetime.now(),
#     chat=telegram.Chat(0, ''),
#     text=message_text
# )
# define a command callback function : /start
def start_callback(bot, update):
    #global thebot
    #thebot = bot
    lang_code = update.message.from_user.language_code
    print(separator)
    printLog("command: /start ",update.message.from_user)
    bot.send_message(chat_id=update.message.chat_id,
                        text="Hello " + str(update.message.from_user.first_name) + " " + str(update.message.from_user.last_name))
    # profil, options, help, add, revoke, news, complex search
    if(reject_bots(bot, update) == True):
        bot.send_message(chat_id=update.message.chat_id,
                            text=get_lang_string_by_code(lang_code, "WELCOME_MESSAGE"))


        conn = sqlite3.connect('./chatid.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM chatid_table WHERE chatid=\""+str(update.message.chat_id)+"\"")
        rows3 = cur.fetchall()
        if(len(rows3) == 0):
            conn = sqlite3.connect('./chatid.db')
            c = conn.cursor()
            c.execute('INSERT INTO chatid_table VALUES (?,?,?,?)', (str(update.message.chat_id), "", (str(update.message.from_user.first_name) + " " + str(update.message.from_user.last_name)), str(datetime.now()).split('.')[0]))
            conn.commit()
            c.close()
            print("[+] ", str(update.message.from_user.first_name), " added successfully !")
            logger.info("[+] "+ str(update.message.from_user.first_name)+ " added successfully !")
        else:
            print("[+] ", str(update.message.from_user.first_name), " Allready saved !")
            logger.warning("[+] "+ str(update.message.from_user.first_name)+ " Allready saved !")


# Handler
start_handler = CommandHandler("start", start_callback)


# The Help function
def help_callback(bot, update):
    #global thebot
    #thebot = bot
    lang_code = update.message.from_user.language_code

    print(separator)
    printLog("command: /help ",update.message.from_user)
    if(reject_bots(bot, update) == True):
        bot.send_message(chat_id=update.message.chat_id,
                        text=get_lang_string_by_code(lang_code, "HELP_MESSAGE"))
# Handler
help_handler = CommandHandler("help", help_callback)



# To send messageto some one init's Telegram
def message_user(chatid, message):
        payload = {
            'chat_id': chatid,
            'text': message
        }
        return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TOKEN),
                             data=payload).content


def error(bot, update, error):
    #global thebot
    #thebot = bot
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)



def main():
    # Starting with the presentation
    presentation()

    # Cheker for new messages from elegram API -> polling
    updater = Updater(token=TOKEN)
    # Allow us to register handlers -> command, text, video, audio, etc
    dispatcher = updater.dispatcher

    # Add a command handler for dispatcher
    dispatcher.add_handler(start_handler)

    # Add a command handler for dispatcher
    dispatcher.add_handler(help_handler)

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()