import time
import random
import json
import sqlite3

conn = sqlite3.connect('./chatid_.db')
c = conn.cursor()
c.execute('UPDATE chatid_table SET last_confession=\"\" WHERE 1=1')
conn.commit()
c.close()