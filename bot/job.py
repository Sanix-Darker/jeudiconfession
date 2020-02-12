import time
import random
import json
import sqlite3
from main import message_user
import base64

import datetime

print("[+] --------------------------------------")
print("[+] Jeudiconfession Job started...")
print("[+] --------------------------------------")


while True:
    time.sleep(10)
    week_day = datetime.datetime.today().weekday()
    if week_day in [2,3,4]:
        time.sleep(50)
        with open("./last_tweets.json") as frt:
            try:
                results_tweets = json.load(frt)
                current_last_conv = results_tweets[0]["tweet_url"].split("/")[-1]
                if (len(results_tweets) > 0):

                    conn = sqlite3.connect('./chatid_.db')
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM chatid_table")
                    rows3 = cur.fetchall()
                    for row in rows3:
                        chatid, last_confession, username = str(row[0]), str(row[1]), str(row[2])

                        c1 = conn.cursor()
                        print("\n\n[+] ------------ ======>>>>>>")
                        print("\n[+] -------------------------------- ")
                        print("[+] chatid: ", chatid)
                        print("[+] username: ", username)
                        print("[+] ----------------------======>>>>>>\n\n")
                        for tweet in results_tweets:
                            # print("tweet: ", tweet)
                            if len(str(last_confession)) == 0:
                                last_confession = "--234"

                            if tweet["tweet_url"] not in last_confession:
                                print("[+] >>>> Sending the tweet")
                                time.sleep(3)
                                print(message_user(chatid, (base64.b64decode(tweet["text_content"].replace("b'", "").replace("'", "")).decode()).replace("# ", "#")))

                                last_confession += tweet["tweet_url"]

                                print("\n[+] -------------------------------- ")
                                print('[+] tweet_url ', tweet["tweet_url"])
                                print("[+] new_last_confession: ", last_confession)
                                print("[+] ----------------------======>>>>>>\n\n")

                                c1.execute('UPDATE chatid_table SET last_confession=? WHERE chatid=?', (last_confession, chatid))
                        conn.commit()
                        c1.close()
                        time.sleep(0.5)
                        print("\n[+] -------------------------------- ")
                    conn.commit()
                    cur.close()
                else: print("[+] Fetching...")
            except Exception as es: print(es)
    else:
        print("[+] Not a proper day to fetch twitter")
        with open("./last_tweets.json", "w") as frt:
            print("[+] Empty the file")
            frt.write("{}")