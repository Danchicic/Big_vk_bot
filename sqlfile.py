import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''CREATE TABLE user_state
                  (id integer, 
                  trans boolean,
                   reader boolean,
                   money boolean,
                   link_re boolean,
                   linked boolean,
                   click_up boolean,
                   how_link boolean,
                   moder boolean,
                   data
                   )''')
