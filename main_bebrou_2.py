import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json

from vars_from_bd import *
from config import TOKEN

from Users import User
from reader_keyboards import *
from author_keyboards import *
from translator_keyboards import *
from main_kb import *

from reader import reader

import sqlite3

create_reader_kb = create_reader_kb()
read_event_dif = read_event_dif()
re_pass_kb = re_pass_kb()
question_kb = question_kb()
error_kb = create_error_kb()
money_kb = money_kb()
if_kb_reader_24 = if_kb()
if_kb_reader_re = if_kb()
if_kb_reader_linked = if_kb()

author_kb = author_kb()

work_kb = work_kb()
translator_question = translator_question()
translator_money_kb = translator_money_kb()
trans_kb = trans_kb()
if_kb_translator = if_kb()

with open('ans.json', 'r') as f:
    data = json.load(f)

pass_kb = pass_keyb()

start_kb = start_kb()

# Авторизация пользователя
vk_session = vk_api.VkApi(token=TOKEN)
longpolling = VkLongPoll(vk_session)
i = 0
user = User()
states = {}


conn = sqlite3.connect('database.db')
cursor = conn.cursor()
try:
    for event in longpolling.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            txt = event.text.lower()

            res = cursor.execute('SELECT * FROM user_state').fetchall()
            print(res, 'bd')

            if user_id not in res:
                # Новый пользователь, создаем новое состояние
                states[user_id] = {"data": {}}
                user_state = states[user_id]
                user_state['data']['trans'] = False
                user_state['data']['reader'] = False
                user_state['data']['money'] = False
                user_state['data']['link_re'] = False
                user_state['data']['linked?'] = False
                user_state['data']['click_up'] = False
                user_state['data']['how_link'] = False
                user_state['data']['moder'] = False
                user_state['data']['level'] = False
                user_state['data']['stack'] = [['Выберите пользователя', start_kb], ]
            user_state = states[user_id]
            if len(user_state['data']['stack']) == 0:
                user_state['data']['stack'] = [['Выберите пользователя', start_kb], ]
                i = 0
            print(READER)
            if txt == 'читатель' or READER:
                reader(vk_session, user, event, user_state, i)
            elif txt == 'автор' or AUTHOR:
                pass
            elif txt == 'переводчик' or TRANSLATOR:
                pass

except Exception as ex:
    print(ex)
