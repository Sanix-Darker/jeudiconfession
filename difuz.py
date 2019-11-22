from bot.main import message_user
import sqlite3

print("[+] This script will diffuz to all chatid the mesage you want to share !")

conn = sqlite3.connect('./chatid.db')
cur = conn.cursor()
cur.execute("SELECT * FROM chatid_table")
rows3 = cur.fetchall()
print("[+] list: ", rows3)
for row in rows3:
    chatid, username = str(row[0]), str(row[2])
    print("[+] Sending to ", username)
    print("[+] Chat-Id ", chatid)
    message = "C'est ao "+username+" !?\n"
    message += "J'esperes que tu as apprecier le bot JeudiConfessionBot.\n"
    message += "Comme j'ai eu a le preciser, c'etait juste le test d'un jour,"
    message += "a moins que je ne trouves un serveur viable sur lequel le deployer.\n"
    message += "Vous avez ete ( 64 ) pour ce test, Merci encore."