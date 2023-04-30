from vk_api.utils import get_random_id
import json
from reader.reader_keyboards import *
from author.author_keyboards import *
from translator.translator_keyboards import *
from main_kb import *

import sqlite3

with open('actions.json', 'r', encoding='utf-8') as f:
    actions = json.load(f)

with open('ans.json', 'r', encoding='utf-8') as f:
    answers = json.load(f)
print(actions)
print(answers)

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

pass_kb = pass_keyb()
start_kb = start_kb()


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def send_msg(self, vk_session, text: str, keyboard=None):
        params = {'user_id': self.user_id,
                  'message': text,
                  'keyboard': keyboard.get_keyboard(),
                  'random_id': get_random_id()}
        vk_session.method('messages.send', params)


class Bot:
    def __init__(self, msg, user_id, vk_session):
        self.msg = msg
        self.user_id = user_id
        self.vk_session = vk_session
        self.user = User(self.user_id)

    def check_user(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        users = cursor.execute('SELECT id FROM user_state').fetchall()
        if self.user_id not in users:
            cursor.execute(f"INSERT INTO user_state (id) VALUES ({self.user_id})")
            conn.commit()
            return 'добавил нового пользователя'
        return 'Пользователь есть в бд'

    def hand_message(self):
        for row in actions:
            if self.msg == row['text']:
                x = getattr(self, row['func'])
                return x()

    def reader(self):
        self.user.send_msg(self.vk_session, 'Читатель', create_reader_kb)

        return ['Читатель', create_reader_kb]

    def re_pass(self):
        self.user.send_msg(self.vk_session, 'Re:pass', re_pass_kb)

        return ["Re:pass", re_pass_kb]

    def how_to_start(self):
        self.user.send_msg(self.vk_session, text=answers['reader']['re:pass']['how_to_start'], keyboard=pass_kb)

        # return [actions['reader']['re:pass']['how_to_start'], pass_kb]


if __name__ == '__main__':
    bot = Bot('читатель', 324145624152465)
    user_id = bot.check_user()
    ans = bot.reader_handler()
    print('f', user_id)
