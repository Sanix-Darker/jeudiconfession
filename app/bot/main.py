from telegram.ext import Updater, CommandHandler, MessageHandler
import json

from app.settings import *
from app.utils import *
from app.model import Confession, WatchMe



Cf = Confession.Confession
Wm = WatchMe.WatchMe

def presentation():
    print("[+] Jcf-bot started on tg !")


def start_callback(bot, update):
    print("[+] start-callback")

    # we try to fetch if that chat_id is already in 
    # the database and if the status of receiving tweet is ok or nok

    # If not we add it with the status ok

    # If yes we say him(her) we already know he is interested having confessions

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \n" + \
            "Starting right now, i will send you Tweets with #Jeudiconfession hashtag !"
    )


def stop_callback(bot, update):
    print("[+] stop-callback")

    # we try to fetch if that chat_id is already in 
    # the database and if the status of receiving tweet is ok or nok

    # If not we add it with the status nok

    # If yes, we just update his(her) status to nok

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \n" + \
            "Okay..., i will stop send you Tweets with #Jeudiconfession hashtag !"
    )


def help_callback(bot, update):
    print("[+] help-callback")

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \n" + \
        "Am just a bot that will fetch confessions from twitter and send that to you !\n---\n" + \
        "/start - start the bot/activate the receiving of tweets.\n" + \
        "/stop - stop receiving confessions.\n" + \
        "/help - help, list of command the bot.\n---\n"
    )


start_handler = CommandHandler("start", start_callback)
stop_handler = CommandHandler("stop", start_callback)
help_handler = CommandHandler("help", help_callback)


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(help_handler)


if __name__ == "__main__":
    presentation()

    updater.start_polling()
    updater.idle()
