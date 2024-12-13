import datetime
import json
import random
import time
import sched

_DOWNLOAD_PATH = "Download/"
_I = 5
_TIME_SEC = 10
_LOG_FILE = f'json/log/serialize-{datetime.datetime.now().strftime("%Y%m%d")}.log'

class Article:
    def __init__(self, title, body=None):
        self.title = title
        self.body = body if body else f'Некоторый текст - {random.randint(1000, 9999999)}'
        self.datetime = datetime.datetime.now().strftime("%A %d-%b-%Y %H:%M:%S")
        self.likes = random.randint(0, 100)  # Random likes from the first code

def log(s):
    with open(_LOG_FILE, "a") as f:
        f.writelines(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {s} \n')

def to_dict(o):
    result = o.__dict__
    result["className"] = o.__class__.__name__
    return result

def json_dump_article(art: Article):
    dt_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = f'{_DOWNLOAD_PATH}{art.title}_{dt_str}.json'
    with open(path, 'a') as f:
        json.dump(to_dict(art), f)

def send_json_data(i):
    try:
        title = f'Заголовок - {random.randint(1, 9999)}'
        art = Article(title)
        fd = f'json/download/{i}-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}-data.json'
        with open(fd, "x") as f:
            json.dump(to_dict(art), f)
        log(f'отправка {i} выполнена')
        json_dump_article(art)  # Save article to JSON
    except Exception as err:
        log(f'ошибка отправки {i} - {err}')

_J = 0
def do_work(sc): 
    global _J
    _J += 1
    print(f'-— {_J} —-')
    send_json_data(_J)
    if _J < _I:
        sc.enter(_TIME_SEC, 1, do_work, (sc,))

log("-= START =-")
s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, do_work, (s,))
s.run()
log("-= STOP =-")
