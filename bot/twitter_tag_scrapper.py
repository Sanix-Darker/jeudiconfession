import requests
import json
from lxml import html
import time

import base64

hash_tag_array = ["jeudiconfession"]

def scrapy_splash_request(to_fetch_url):

    json_data = {
        "response_body":False,
        "lua_source":"function main(splash, args)\r\n  assert(splash:go(args.url))\r\n  assert(splash:wait(0.5))\r\n  return {\r\n    html = splash:html(),\r\n    png = splash:png(),\r\n    har = splash:har(),\r\n  }\r\nend",
        "url":to_fetch_url,
        "html5_media":False,
        "save_args":[],
        "viewport":"1024x768",
        "http_method":"GET",
        "resource_timeout":0,
        "render_all":False,
        "png":1,
        "har":1,
        "timeout":90,
        "request_body":False,
        "load_args":{},
        "html":1,
        "images":1,
        "wait":0.5
    }

    url = "http://0.0.0.0:8050/execute"

    r = requests.post(url, json=json_data)
    result = r.content
    json_result = json.loads(result)
    html_string = json_result["html"]

    return html_string


def run_scrap(count_per_tweet):
    results = []
    for hashtag in hash_tag_array:
        twitter_url = "https://twitter.com/search?q=%23"+hashtag+"&src=typeahead_click&f=live"
        tree = html.fromstring(scrapy_splash_request(twitter_url))
        tweets_url = tree.xpath("//a[contains(@class, 'tweet-timestamp')]/@href")

        for i, turl in enumerate(tweets_url):
            url = "https://twitter.com"+turl
            print("[+] ------------------")
            print("[+] url: ", url)
            print("[+] ------------------")

            tree2 = html.fromstring(scrapy_splash_request(url))
            tweet_content = tree2.xpath("//p[contains(@class, 'TweetTextSize')]//text()")
            text_content = str(base64.b64encode((' '.join(tweet_content)+"\n\n\nLink: "+url).encode()))

            results.append({
                "hashtag":hashtag,
                "tweet_url":url,
                "text_content":text_content # astuce lors de l'envoies, send juste avec le .decode()
            })

            if (i >= count_per_tweet-1): break

    # print("[+] results: ",json.dumps(results))
    with open("./last_tweets.json", "w+") as frt:
        frt.write(json.dumps(results))
    print("[+] A tour Ended Here")
    time.sleep(5)


# while True:
#     time.sleep(10)
#     run_scrap(10)

run_scrap(10)