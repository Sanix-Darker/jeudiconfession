import requests
from bs4 import BeautifulSoup
import json
import datetime

from app.settings import HOST, TOKEN
from hashlib import md5



def send_message(chat_id: str, text: str, photo: str):
    """
    This method will just send a message to the appropriate client

    """
    datas = {
        "chat_id": chat_id,
        "caption": text,
        "photo": photo,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    r = requests.post(
        "https://api.telegram.org/bot" + TOKEN + "/sendPhoto", 
        data=datas
    )
    
    return True if r.status_code == 200 else False


def format_text_image(cf):
    # We build our image and our capption
    image = cf["avatar"]
    if (len(cf["media"]) > 5):
        image = cf["media"]

    text = "<a href='https://twitter.com" + cf["author-link"] + "'>" 
    text += cf["author-name"] + "</a>:<br>"
    text += cf["tweet-text"] + "<br>-----<br>"
    text += "<a href='"+cf["link"]+"'>LINK</a>"

    return image, text


def clean_text(strr: str):
    """
    This will remove spaces...

    """
    return " ".join(strr.split())


def extract_infos(item):
    """
    Just a basic formater for a tweet

    """
    link = item["href"]

    # Because we are not sure to always have media here
    try:
        origin_media = item.find("td", {"class": "tweet-content"}) \
            .find("div", {"class": "media"}).find("img")["src"]
    except Exception as es:
        origin_media = ""

    # The user avatar
    avatar = item.find("td", {
        "class": "avatar"
    }).find("img")["src"]

    user_info = item.find("td", {
        "class": "user-info"
    })

    author_name = user_info.find("div", {
        "class": "username"
        }).get_text()
    author_link = user_info.find("a")["href"]

    # The tweet content
    tweet_text = item.find("td", {
        "class": "tweet-content"
    }).find("div", {"class": "tweet-text"}) \
    .get_text()

    return link, avatar, author_name, author_link, tweet_text, media


def get_tweets():
    """
    This method will fetch all tweets with the hashtag

    """

    tweets_json = []

    r =requests.get(HOST + "search?q=%23jecficonfession&src=typed_query&f=live")

    confessions = BeautifulSoup(r.content.decode(), "html.parser").find_all("table", {
        "class": "tweet"
    })

    for item in confessions:
        (link, 
        avatar, 
        author_name, 
        author_link, 
        tweet_text,
        media) = extract_infos(item)

        tweets_json.append({
            "link": link,
            "avatar": avatar,
            "author-name": clean_text(author_name),
            "author-link": author_link,
            "tweet-text": clean_text(tweet_text)
            "media": media
        })
    
    return tweets_json


def is_good_date():
    """
    This is a simple method that will say if we are Wenesday, Thursday or Friday
    The appropriate time to send confessions to recipients

    """

    if 2 <= datetime.datetime.today().weekday() <= 4:
        return True
    else:
        return False


def get_cf_id(Cf, result):
    """
    Let's get ObjectId from the tweet

    """
    # We fetch the object id
    return str(list(Cf().find_by({
        "origin": result["origin"]
    }))[0]["_id"]).replace("ObjectId(", "").replace(")", "")


def save_watcher(Wm, cf_id, result, chat_id):
    """
    THis method will only save the new watching

    """
    wm = Wm({
        "origin-id": cf_id, 
        "origin-url": result["origin"]["link"], 
        "chat-ids": [chat_id]
    })
    wm.save()


def save_confession(url, Cf, Wm, chat_id, result, undelete_fetch):
    """
    This method will just save the Confession using pyMongo

    """
    # we check first if the confession not already saved

    print("{+} Saving confession ")
    cf = Cf(result)
    cf.save()

    print("[+] Successfully saved...")

    # We fetch the object id 
    # and we save the WatchMe
    save_watcher(Wm, get_cf_id(Cf, result), result, chat_id)
    
    print("[+] returning the message...")
    
    return {
        "status": "success",
        "message": "{}".format(chat_id)
    }


def append_new_watcher(Cf, Wm, url, result, chat_id, watchme_fetch):
    """
    We append a new watcher or we just don't do it if it's already in the list

    """
    # if NO, we save it
    if len(watchme_fetch) == 0:
        # We fetch the object id
        # and we save the WatchMe
        save_watcher(Wm, get_cf_id(Cf, result), result, chat_id)

        return {
            "status": "success",
            "message": "{}, An entry already exist for this tweet, ".format(chat_id) +
                        "{} is been watching for you !".format(url.split("/")[-1])
        }
    else:
        # let's check if the chat_id is in the array of chat_id
        if chat_id in watchme_fetch[0]["chat-ids"]:
            print("[-] You are already watching this tweet !")

            return {
                "status": "error",
                "message": "{}, An entry allready exist for this UnDelete, ".format(chat_id) +
                            "and you're already watching this tweet !"
            }
        else:
            print("{+} Update watchme_fetch chat-ids ")

            watchme_fetch[0]["chat-ids"].append(chat_id)

            Wm().update({
                "origin-url": result["origin"]["link"]
            }, watchme_fetch[0])

            return {
                "status": "success",
                "message": "{}, An entry allready exist for this tweet, ".format(chat_id) +
                            "now you have been added to the watcher list (" + 
                            str(len(watchme_fetch[0]["chat-ids"])) + ") !"
            }


def remove_new_watcher(Cf, Wm, url, result, chat_id, watchme_fetch):
    """
    We remove a new watcher

    """
    # if NO, we save it
    if len(watchme_fetch) != 0:

        if chat_id in watchme_fetch[0]["chat-ids"]:
            # We fetch the object id
            # and we save the WatchMe
            watchme_fetch[0]["chat-ids"].remove(chat_id)

            Wm().update({
                "origin-url": result["origin"]["link"]
            }, watchme_fetch[0])

            return {
                "status": "success",
                "message": "{}, you have been removed from watcher for this tweet, ".format(chat_id)
            }
        else:
            # not there
            return {
                "status": "success",
                "message": "{}, you're not watching this tweet at the moment, ".format(chat_id)
            }
    else:
        # not there
        return {
            "status": "success",
            "message": "{}, you're not watching this tweet at the moment, ".format(chat_id)
        }


def unwatch(Cf, Wm, url: str, chat_id: str):

    result = get_tweet_and_comments(url, chat_id)

    # we check if that Undelete already exist
    watchme_fetch = list(Wm().find_by({
        "origin-url": result["origin"]["link"]
    }))
    
    return remove_new_watcher(Cf, Wm, url, result, chat_id, watchme_fetch)


def watch_this(Cf, Wm, url: str, chat_id: str):
    """
    Start watching this tweet...

    """

    # Save on MongoDb
    # we check if the confession already exist
    undelete_fetch = list(Cf().find_by({
        "origin": result["origin"]
    }))

    # if NO, we save it
    if len(undelete_fetch) == 0:
        return save_confession(url, Cf, Wm, chat_id, result, undelete_fetch)
    else:
        print("[x] An entry allready exist for this UnDelete...")
        # if an unDelete allready exist then let's try to save the WatchMe

        # we check if that Undelete already exist
        watchme_fetch = list(Wm().find_by({
            "origin-url": result["origin"]["link"]
        }))

        return append_new_watcher(Cf, Wm, url, result, chat_id, watchme_fetch)
