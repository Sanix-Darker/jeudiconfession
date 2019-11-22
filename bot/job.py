import time
import random
import json
import sqlite3
from main import message_user
import base64

print("[+] --------------------------------------")
print("[+] Jeudiconfession Job started...")
print("[+] --------------------------------------")


while True:
    rand = random.randint(1, 5)
    print ("[+] rand: ", rand)
    time.sleep(rand)
    conn = sqlite3.connect('./chatid_.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM chatid_table")
    rows3 = cur.fetchall()
    print("[+] rows3: ", rows3)

    with open("./last_tweets.json") as frt:
        try:
            results_tweets = json.load(frt)
            current_last_conv = results_tweets[0]["tweet_url"].split("/")[-1]
            if (len(results_tweets) > 0):
                for row in rows3:
                    chatid, last_confession, username = str(row[0]), str(row[1]), conn.cursor()

                    print("\n[+] -------------------------------- ")
                    print("[+] chatid: ", chatid)
                    print("[+] last_confession: ", last_confession)
                    print("[+] username: ", username)
                    conn = sqlite3.connect('./chatid_.db')
                    c = conn.cursor()
                    for tweet in results_tweets:
                        print("tweet: ", tweet)
                        if len(str(last_confession)) == 0:
                            last_confession = "--234"

                        print("\n\n[+] ======>>>>>>")
                        print("[+] ======>>>>>>")
                        print("[+] BEFORE ==============================================")
                        print('[+] username: ', username)
                        print('[+] tweet["tweet_url"]: ', tweet["tweet_url"])
                        print("[+] new_last_confession: ", last_confession)
                        print("[+] ======>>>>>>")
                        print("[+] ======>>>>>>\n\n")

                        if tweet["tweet_url"] not in last_confession:
                            time.sleep(2)
                            print("[+] >>>> Sending the tweet")
                            print(message_user(chatid, (base64.b64decode(tweet["text_content"].replace("b'", "").replace("'", "")).decode()).replace("# ", "#")))

                            last_confession += tweet["tweet_url"]

                            print("\n\n[+] ======>>>>>>")
                            print("[+] ======>>>>>>")
                            print("AFTER ==============================================")
                            print('[+] tweet["tweet_url"]: ', tweet["tweet_url"])
                            print("[+] new_last_confession: ", last_confession)
                            print("[+] ======>>>>>>")
                            print("[+] ======>>>>>>\n\n")


                            c.execute('UPDATE chatid_table SET last_confession=? WHERE chatid=?', (last_confession, chatid))
                    conn.commit()
                    c.close()

                    print("\n[+] -------------------------------- ")
            else: print("[+] Fetching...")
        except Exception as es: print(es)