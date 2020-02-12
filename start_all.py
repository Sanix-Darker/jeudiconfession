from threading import Thread
from os import system as ss

print("[+] Starting all process for JeveuConfessionBot...")

def scrapy_splash_process():
    print("[+] Starting The main_bot")
    ss("sudo docker run -p 8050:8050 scrapinghub/splash")


def bot_process():
    print("[+] Starting The main_bot")
    ss("python ./bot/main.py")


def bot_job_process():
    print("[+] Starting The job_bot")
    ss("python ./bot/job.py")


def twitter_parser_process():
    print("[+] Starting The twitter_parser")
    ss("python ./bot/twitter_tag_scrapper.py")


Thread(target = scrapy_splash_process).start()
Thread(target = bot_process).start()
Thread(target = bot_job_process).start()
Thread(target = twitter_parser_process).start()
