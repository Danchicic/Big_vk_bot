import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json

from vars_from_bd import *
from config import TOKEN

from Users import User

from reader.reader_keyboards import *
from author.author_keyboards import *
from translator.translator_keyboards import *

from main_kb import *

from reader.reader import reader

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
            res = cursor.execute('SELECT id FROM user_state').fetchall()
            print(res, 'bd')

            if event.user_id not in [r[0] for r in res]:
                print('excellent')
                cursor.execute(f"INSERT INTO user_state (id) VALUES ({event.user_id})")
                conn.commit()
            data = cursor.execute(
                "SELECT * FROM user_state WHERE id=?", (event.user_id,)
            ).fetchone()

            TRANS = data[1]
            READER = data[2]
            money = data[3]
            link_re = data[4]
            linked = data[5]
            click_up = data[6]
            how_link = data[7]
            moder = data[8]
            print(READER)

            if txt == 'начать':
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Выберите категорию',
                              keyboard=start_kb)

            if txt == 'читатель' or READER:
                reader(vk_session, user, event, i, cursor, conn)
            elif txt == 'автор' or AUTHOR:
                print('Автор')
                pass
            elif txt == 'переводчик' or TRANSLATOR:
                pass

except Exception as ex:
    print(ex, 'EX')
