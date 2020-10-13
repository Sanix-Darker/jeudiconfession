import configparser as Configparser

conf = Configparser.RawConfigParser()
conf_path = r'config.txt'
conf.read(conf_path)

HOST = conf.get("jcf", "HOST")
DATABASE_HOST = conf.get("jcf", "DATABASE_HOST")
DATABASE_NAME = conf.get("jcf", "DATABASE_NAME")

TOKEN = conf.get("jcf", "TOKEN")
