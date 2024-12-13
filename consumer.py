import time
import sched
import json
import random
from datetime import datetime
import shutil
import os
from os import walk

class Article:
    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.datetime = datetime.now().strftime("%A %d-%b-%Y %H:%M:%S") 
        self.likes = random.randint(10, 100)

_I = 20
_LOG_FILE = f'json/log/deserialize-{datetime.now().strftime("%Y%m%d")}.log'
_PATH_DOWN = "json/download/"

def log(s):
    with open(_LOG_FILE, "a") as f:
        f.writelines(f'{datetime.now().strftime("%H:%M:%S")} | {s} \n')

def print_article(o):
    print(o.title, o.body, o.datetime, o.likes, sep='\n')
    log(f'даные обработаны {o.title}')

def read_file(path, f_name):
    with open(f'{path}{f_name}', "r") as f:
        art_load = json.load(f)
        return art_load

def copy_file(f_name):
    shutil.copy(f'{_PATH_DOWN}{f_name}', "json/loaded/")

def error_copy_file(f_name):
    shutil.copy(f'json/error/{f_name}', "json/loaded/")

def remove_file(f_name):
    os.remove(f'{_PATH_DOWN}{f_name}')

def from_dict(o, f_name):
    try:
        article = Article(o["title"], o["body"])
        article.datetime = o["datetime"]
        article.likes = o["likes"]
        copy_file(f_name)
        return article
    except Exception as err:
        log(f'ошибка - {err}')
        error_copy_file(f_name)
    else: 
        print("ELSE")
    finally: 
        remove_file(f_name)

def watch_dir(path):
    for root, dirs, files in walk(path):
        for file in files:
            log(f'обнаружен файл {file}')
            art_load = read_file(path, file)
            art = from_dict(art_load,  file)
            print_article(art)

def do_work(sc): 
    global _I
    print(f'--- {_I} ---')
    watch_dir(_PATH_DOWN)
    _I = _I - 1
    if _I > 0:
        s.enter(10, 1, do_work, (sc,))

# New functionality to handle JSON serialization
def serialize_article(article):
    return {
        "title": article.title,
        "body": article.body,
        "datetime": article.datetime,
        "likes": article.likes
    }

def save_article(article):
    file_name = f'json/download/{article.title.replace(" ", "_")}.json'
    with open(file_name, 'w') as f:
        json.dump(serialize_article(article), f)
        log(f'Сохранен файл {file_name}')

# Example of creating and saving an article
new_article = Article("Новый заголовок", "Это тело нового статьи.")
save_article(new_article)

log("-= START =-")
s = sched.scheduler(time.time, time.sleep)
s.enter(5, 1, do_work, (s,))
s.run()
log("-= STOP =-")
