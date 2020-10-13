import requests

r = requests.get("https://mobile.twitter.com/search?q=%23jeudiconfession&src=typed_query&f=live")

with open("ress.html", "w") as frg:
    frg.write(r.content.decode())
