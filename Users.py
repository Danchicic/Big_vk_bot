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
        conn = sqlite3.connect('database.db')

        self.msg = msg
        self.user_id = user_id
        self.vk_session = vk_session
        self.user = User(self.user_id)
        self.cursor = conn.cursor()
        self.conn = conn
        users = self.cursor.execute('SELECT id FROM user_state').fetchall()

        if self.user_id not in [r[0] for r in users]:
            self.cursor.execute(f"INSERT INTO user_state (id) VALUES ({self.user_id})")
            self.conn.commit()
        data = self.cursor.execute(
            f"SELECT * FROM user_state WHERE id={self.user_id}"
        ).fetchone()
        self.TRANS = data[1]
        self.READER = data[2]
        self.money = data[3]
        self.link_re = data[4]
        self.linked = data[5]
        self.click_up = data[6]
        self.how_link = data[7]
        self.moder = data[8]
        self.last_answer = data[9]

    def hand_message(self):
        for row in actions:
            if self.msg == row['text']:
                x = getattr(self, row['func'])
                return x()

    def start(self):
        self.user.send_msg(self.vk_session, 'Выберите пользователя', start_kb)

    def reader(self):
        self.user.send_msg(self.vk_session, 'Читатель', create_reader_kb)
        self.cursor.execute(f"UPDATE user_state SET reader=? WHERE id={self.user_id}", (True,))
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                            ('Начать',))
        self.conn.commit()

    def re_pass(self):
        self.user.send_msg(self.vk_session, 'Re:pass', re_pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}", ('Читатель',))
        self.conn.commit()

    def how_to_start(self):
        self.user.send_msg(self.vk_session, text=answers['reader']['re:pass']['how_to_start'], keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}", ('Re:pass',))
        self.conn.commit()

    def no_tasks(self):
        self.user.send_msg(self.vk_session, text=answers['reader']['re:pass']['no_tasks'], keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}", ('Re:pass',))
        self.conn.commit()

    def task_no_counted(self):
        self.user.send_msg(self.vk_session, text=answers['reader']['re:pass']['task_no_counted'], keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}", ('Re:pass',))
        self.conn.commit()

    def translation_questions(self):
        self.user.send_msg(self.vk_session, text='Вопросы по переводу', keyboard=question_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}", ('Читатель',))
        self.conn.commit()

    def translation_quality(self):
        self.user.send_msg(self.vk_session, text='Перевожу вас на общение с модератором', keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}", ('Вопросы по переводу',))
        self.conn.commit()

    def translators_dont_open(self):
        self.user.send_msg(self.vk_session, text=answers['reader']['translation_questions']['trans_no_open_hand'],
                           keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}", ('Вопросы по переводу',))
        self.conn.commit()

    def another(self):
        if self.READER:
            self.user.send_msg(self.vk_session, text='Выберите из предложенного списка',
                               keyboard=read_event_dif)
            self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                                ('Читатель',))
            self.conn.commit()
        """Еще одно условие """

    def want_to_idea(self):
        self.user.send_msg(self.vk_session, text='Опишите фичу', keyboard=pass_kb)
        """посмотреть что с кликапом"""
        self.click_up = True

        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                            ('Другое',))
        self.conn.commit()

    def i_banned(self):
        self.user.send_msg(self.vk_session, text=answers['reader']['other']['i_banned'], keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                            ('Другое',))
        self.conn.commit()

    def invite_moder(self):
        self.user.send_msg(self.vk_session, text='модератор вошел в чат', keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                            ('Другое',))
        self.conn.commit()
        """посмотреть что с модератором"""

    def some_wrong(self):
        self.user.send_msg(self.vk_session, text=' Выберите из предложенного списка', keyboard=error_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                            ('Читатель',))
        self.conn.commit()

    def error_404(self):
        self.user.send_msg(self.vk_session, text=answers['reader']['error_messages']['er404'], keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                            ('У меня возникла ошибка',))
        self.conn.commit()

    def error_500(self):
        self.user.send_msg(self.vk_session, text=answers['reader']['error_messages']['er500'], keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                            ('У меня возникла ошибка',))
        self.conn.commit()

    def no_pic(self):
        self.user.send_msg(self.vk_session, text=answers['reader']['error_messages']['no_pic'], keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                            ('У меня возникла ошибка',))
        self.conn.commit()

    def find_bug(self):
        self.user.send_msg(self.vk_session, text='Опишите ошибку', keyboard=pass_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                            ('У меня возникла ошибка',))
        self.conn.commit()
        """посмотреть что с click_up'ом"""

    def no_money_or_tickets(self):
        self.user.send_msg(self.vk_session, text='Не пришли деньги/тикеты', keyboard=money_kb)
        self.cursor.execute(f"UPDATE user_state SET last_answer=? WHERE id={self.user_id}",
                            ('Читатель',))
        self.conn.commit()
    def no_money(self):
        pass
    def no_tickets(self):
        pass

    def back(self):
        for row in actions:
            print(self.last_answer)
            if self.last_answer.lower() == row['text']:
                x = getattr(self, row['func'])
                return x()

    def last_message(self):
        self.user.send_msg(self.vk_session, text='Выберите категорию', keyboard=start_kb)

        self.cursor.execute(
            f"UPDATE user_state SET trans=?,reader=?, money=?, link_re=?, linked=?, click_up=?, how_link=?, moder=?, last_answer=?  WHERE id={self.user_id}",
            (False, False, False, False, False, False, False, False, ''))
        self.conn.commit()
