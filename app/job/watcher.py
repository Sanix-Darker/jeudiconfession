import requests
import json
import time
from app.utils import *
from app.model import Confession, WatchMe



Cf = Confession.Confession
Wm = WatchMe.WatchMe

def save_confessions():
    """
    This method will save tweet confession to the database
    if they are not there

    """
    ts = get_tweets()

    for t in ts:
        cf_fetched = list(Cf().find_by({
            "link": t["link"]
        }))

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
    # we loop all watchme
    wm_fetched = list(Wm().find_by({
        "link": t["link"]
    }))


while True:
    # we check the date
    if is_good_date():
        save_confessions()
        time.sleep(5)
        send_confessions()
        time.sleep(10)
    else:
        # we erase all confessions 
        time.sleep(86400)
