from telegram.ext import Updater, CommandHandler, MessageHandler
import json
import datetime

from app.settings import *
from app.utils import *
from app.model import Confession, WatchMe, Chatid



Cf = Confession.Confession
Ch = Chatid.Chatid
Wm = WatchMe.WatchMe

def presentation():
    print("[+] Jcf-bot started on tg !")


def start_callback(bot, update):
    print("[+] start-callback")

    # we try to fetch if that chat_id is already in 
    # the database and if the status of receiving tweet is ok or nok

    # If not we add it with the status ok

    # If yes we say him(her) we already know he is interested having confessions

    ch = list(Ch().find_by({
        "chat-id": str(update.message.chat_id)
    }))

    message = ""
    if len(ch) > 0:
        if ch[0]["status"] != "ok":
            ch[0]["status"] = "ok"
            message = "Your status have been changed, now you can receive Confesions tweets"
            Ch().update({
                "chat-id": str(update.message.chat_id)
            }, ch[0])
        else:
            message = "You're already set to receive confessions tweets"
    else:
        cch = Ch({
            "username": update.message.from_user.username,
            "chat-id": str(update.message.chat_id),
            "status": "ok",
            "date": str(datetime.datetime.today())
        })
        cch.save()
        message = "Starting right now, i will send you Tweets with #Jeudiconfession hashtag !\n\nBy @sanixdarker"
    
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \n" + message        
    )


def stop_callback(bot, update):
    print("[+] stop-callback")

    # we try to fetch if that chat_id is already in 
    # the database and if the status of receiving tweet is ok or nok

    # If not we add it with the status nok

    # If yes, we just update his(her) status to nok
    ch = list(Ch().find_by({
        "chat-id": str(update.message.chat_id)
    }))

    message = ""
    if len(ch) > 0:
        if ch[0]["status"] == "ok":
            ch[0]["status"] = "nok"
            message = "Your status have been changed, now you will never receive again Confessions tweets"
            Ch().update({
                "chat-id": str(update.message.chat_id)
            }, ch[0])
        else:
            message = "You're already set to not receive confessions tweets"
    else:
        cch = Ch({
            "username": update.message.from_user.username,
            "chat-id": str(update.message.chat_id),
            "status": "nok",
            "date": str(datetime.datetime.today())
        })
        cch.save()
        message = "Starting right now, i saved your chat-id but i will not send you Tweets with #Jeudiconfession hashtag !"
    
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \n" + message
    )


def help_callback(bot, update):
    print("[+] help-callback")

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \n" + \
        "Am just a bot that will fetch confessions from twitter and send that to you !\n---\n" + \
        "/start - start the bot/activate the receiving of tweets.\n" + \
        "/stop - stop receiving confessions.\n" + \
        "/help - help, list of command the bot.\n---\nBy @sanixdarker"
    )


start_handler = CommandHandler("start", start_callback)
stop_handler = CommandHandler("stop", stop_callback)
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
