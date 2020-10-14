import requests
import json
import time
from app.utils import *
from app.model import Confession, WatchMe, Chatid



Cf = Confession.Confession
Ch = Chatid.Chatid
Wm = WatchMe.WatchMe

def save_confessions():
    """
    This method will save tweet confession to the database
    if they are not there

    """
    ts = get_tweets()
    print("> Fetched : ", len(ts))

    for t in ts:
        cf_fetched = list(Cf().find_by({
            "link": t["link"]
        }))
        print(".", end="")

        # we add the tweet if it is not already there
        if len(cf_fetched) == 0:
            # we add it in confessions collection
            cf = Cf(t)
            cf.save()

            # we add in watchme
            wm = Wm({
                "link": t["link"],
                "chat-ids": []
            })
            wm.save()


def send_confessions():
    """
    We send confessions to those that not received it yet

    """
    # we loop all chatid,
    # we check if that chat id is in a watchme
    # if not we add it and we send the formated 
    # tweet extract from confession collection

    # if yes, we do nothing

    chs = list(Ch().find_all())
    for ch in chs:
        wms = list(Wm().find_all())
        for w in wms:
            # if the chat id is not in the list of chat-ids
            # and we check the status
            if ch["chat-id"] not in w["chat-ids"] and ch["status"] == "ok":
                cf = list(Cf().find_by({
                    "link": w["link"]
                }))[0]
                
                # We build our image and our capption
                (image, text) = format_text_image(cf)
                
                print(ch["chat-id"] + ", ", end="")

                # We send the message here
                if send_message(ch["chat-id"], text, image):
                    w["chat-ids"].append(ch["chat-id"])
                    # we update that watchme
                    Wm().update({
                        "link": w["link"]
                    }, w)
                    time.sleep(2)
                    print("[-] Sent.")
                else:
                    print("[-] Not Sent.")


while True:
    # we check the date
    if is_good_date():
        save_confessions()
        time.sleep(3)
        send_confessions()
        time.sleep(10)
    else:
        # we erase all confessions 
        # we delete all confessions
        Cf().delete({})
        # We delete all watchme
        Wm().delete({})

        # now we wait
        time.sleep(360)
