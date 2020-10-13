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
        "photo": photo
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

    text = cf["author-name"] + ":\n"
    text += cf["tweet-text"] + "\n-----\n"
    text += "https://twitter.com" + cf["link"]

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

    return link, avatar, author_name, author_link, tweet_text, origin_media


def get_tweets():
    """
    This method will fetch all tweets with the hashtag

    """

    tweets_json = []

    r =requests.get(HOST + "search?q=%23jeudiconfession&src=typed_query&f=live")

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
            "tweet-text": clean_text(tweet_text),
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
