from bs4 import BeautifulSoup
import json
import datetime


with open("g.html", "r") as frt:
    content = frt.read()

    chatids = BeautifulSoup(content, "html.parser").find("tbody", {
        "id": "table-body"
    }).find_all("tr")

    c_ids = []
    for c in chatids:
        c_ids.append({
            "chat-id": c.find_all("td")[0].find("div").get_text(),
            "username": c.find_all("td")[1].find("div").get_text(),
            "date": str(datetime.datetime.now())
        })

    with open("result.json", "w") as fft:
        json.dump(c_ids, fft, indent=4)

