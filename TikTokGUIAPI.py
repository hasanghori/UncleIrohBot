import pyautogui
import time
import pyperclip
import IrohChatBot
from flask import Flask
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import random
from bs4 import BeautifulSoup
import requests

import threading

app = Flask(__name__)
cache = Cache()
app.config['CACHE_TYPE'] = 'simple'
app.secret_key = "PLZWORK"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=30)
cache.init_app(app)

db = SQLAlchemy(app)


class UsedSentences(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    sentence = db.Column(db.String(300))

    def __repr__(self):
        return f"users('{self.username}')"

db.create_all()

time.sleep(2)
print(pyautogui.position())

#Point(x=788, y=756)

#Point(x=522, y=710)
#Point(x=506, y=747)


#find question mark on screen
x, y = pyautogui.locateCenterOnScreen('IntialQuestionMark2.png', confidence=.7)
#right click it
pyautogui.rightClick(x, y, duration=0.2)
#inspect element
time.sleep(1)
a, b = pyautogui.locateCenterOnScreen('InspectElementIcon.png', confidence=.7)
pyautogui.click(a, b, duration=0.2)
time.sleep(5)
print("no sleep")
#find blue question mark
#click twice on it
#cntrl c
c, d = pyautogui.locateCenterOnScreen('BlueQuestionPlusSpan.png', confidence=.9)
pyautogui.doubleClick((c-50), d, duration=0.2)
pyautogui.hotkey('ctrl', 'c')
question = pyperclip.paste()
print("this is question vvv")
print(question)

found_question = UsedSentences.query.filter_by(sentence=question).first()
if not found_question:
    newSentence = UsedSentences(sentence=question)
    db.session.add(newSentence)
    db.session.commit()

    response = IrohChatBot.run(question)
    print(response)

    #x out of inspect
    pyautogui.click(pyautogui.locateCenterOnScreen('LeaveInspectElement.png', confidence=.99))

    time.sleep(1)

    #click reply
    pyautogui.click(pyautogui.locateCenterOnScreen('Reply.png', confidence=.9, region=(0, y, 1100, 100)))

    pyautogui.typewrite(response, interval=0.1)
    pyautogui.hotkey('enter')
else:
    pyautogui.click(pyautogui.locateCenterOnScreen('LeaveInspectElement.png', confidence=.99))

pyautogui.moveTo(x, y)
pyautogui.hotkey('down')
pyautogui.hotkey('down')
pyautogui.hotkey('down')


#


