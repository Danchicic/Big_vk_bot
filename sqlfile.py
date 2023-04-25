import sqlite3
import inspect
from Users import User
from reader.reader_keyboards import if_kb

if_kb_reader_linked = if_kb()
last_msg = ['Выберите из предложенного списка', if_kb_reader_linked]
user = User()

print(type(user), type(if_kb_reader_linked))

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("INSERT INTO user_state (reader) VALUES (True)")
# class_source = inspect.getsource(if_kb_reader_linked)
# cursor.execute("INSERT INTO user_state (last_text, last_keyboard) VALUES (?, ?)",
#                (last_msg[0], class_source))
conn.commit()
conn.close()

"""# создание соединения с базой данных
conn = sqlite3.connect('database.db')
c = conn.cursor()

# определение класса

# сохранение определения класса в базе данных
class_source = inspect.getsource(User)
c.execute("INSERT INTO user_state (last_text, last_keyboard) VALUES (?, ?)", ('MyClass', class_source))
conn.commit()

# закрытие соединения с базой данных
conn.close()
conn = sqlite3.connect('database.db')
c = conn.cursor()

# выборка данных из таблицы
c.execute("SELECT * FROM user_state")
rows = c.fetchall()

# вывод результатов
for row in rows:
    print(row[-1])

# закрытие соединения
conn.close()"""
#Создание таблички
cursor.execute('''CREATE TABLE user_state
                  (id integer
                  trans boolean,
                   reader boolean,
                   money boolean,
                   link_re boolean,
                   linked boolean,
                   click_up boolean,
                   how_link boolean, 
                   moder boolean
                   )''')
