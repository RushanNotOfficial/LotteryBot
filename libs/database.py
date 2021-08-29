from tinydb import TinyDB
from libs.custom_exceptions import UserAlreadyEnteredError, NoUsersEnteredError
from datetime import datetime
import time

db = TinyDB("data/raffles.db")

def add_user_to_raffle(user_id: str):
    if len(db.all()) != 0:
        for item in db:
            index = datetime.now().strftime("%d%m%Y%H%M%S")+str(time.time()).replace(".","")
            db.insert({str(index): str(user_id)})
            print(next(iter(item.values())))
            if next(iter(item.values())) == user_id:
                raise UserAlreadyEnteredError("User already entered in raffle")
            else:
                index = datetime.now().strftime("%d%m%Y%H%M%S")+str(time.time()).replace(".","")
                db.insert({str(index): str(user_id)})
    else:
        index = datetime.now().strftime("%d%m%Y%H%M%S")+str(time.time()).replace(".","")
        db.insert({str(index): str(user_id)})
            
def get_all_values():
    values: list = []
    for item in db.all():
        values.append(str(next(iter(item.values()))))
    if len(values) != 0:
        return values
    else: 
        raise NoUsersEnteredError

def remove_all():
    db.truncate()

def start_raffle():
    with open('data/raffles.status', 'w+') as file:
        file.write("RUNNING")
        file.close()

def stop_raffle():
    with open('data/raffles.status', 'w+') as file:
        file.write("STOPPED")
        file.close()

def is_raffle_running():
    with open('data/raffles.status', 'r') as file:
        data = file.read()
        file.close()
    if data == "RUNNING":
        return "yes"
    else:
        return "no"