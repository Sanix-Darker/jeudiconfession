from app.model import Chatid
import json

Ch = Chatid.Chatid


with open("result.json", "r") as ff:
    chs = json.loads(ff.read())

    for c in chs:
        ch = list(Ch().find_by({
            "chat-id": c["chat-id"]
        }))
        print("> ", c)
        message = ""
        if len(ch) > 0:
            if ch[0]["status"] != "ok":
                ch[0]["status"] = "ok"
                message = "Your status have been changed, now you can receive Confesions tweets"
                Ch().update({
                    "chat-id": c["chat-id"]
                }, ch[0])
            else:
                message = "You're already set to receive confessions tweets"

            print("< not insert.\n")
        else:
            cch = Ch({
                "username": c["username"],
                "chat-id": c["chat-id"],
                "status": "ok",
                "date": c["date"]
            })
            cch.save()
            message = "Starting right now, i will send you Tweets with #Jeudiconfession hashtag !\n\nBy @sanixdarker"

            print("< insert.\n")
