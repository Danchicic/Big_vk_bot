import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json


from config import TOKEN

from Users import User
from reader.reader_keyboards import *
from author.author_keyboards import *
from translator.translator_keyboards import *
from main_kb import *

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
print(len(str(if_kb_translator)))

with open('ans.json', 'r') as f:
    data = json.load(f)

pass_kb = pass_keyb()

start_kb = start_kb()

# Авторизация пользователя
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpolling = VkLongPoll(vk_session)
print(type(vk_session))

i = 0
user = User()
states = {}
try:
    for event in longpolling.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id

            if user_id not in states:
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
            print(user_state['data']['stack'])
            txt = event.text.lower()
            if txt == 'начать':
                user.send_msg(vk_session=vk_session, user_id=event.user_id, text='Выбор категории:',
                              keyboard=start_kb)
                user_state['data']['trans'] = False
                user_state['data']['reader'] = False
                user_state['data']['money'] = False
                user_state['data']['link_re'] = False
                user_state['data']['linked?'] = False
                user_state['data']['click_up'] = False
                user_state['data']['how_link'] = False
                user_state['data']['stack'] = [['Выберите пользователя', start_kb], ]

            elif txt == 'читатель':
                user.send_msg(vk_session=vk_session, user_id=event.user_id, text='Вы выбрали читателя',
                              keyboard=create_reader_kb)
                user_state['data']['reader'] = True


                # 1) Re:pass
            elif txt == 're:pass':
                user.send_msg(vk_session=vk_session, user_id=event.user_id, text='Re:pass',
                              keyboard=re_pass_kb)
                i += 1
                if ['Вы выбрали читателя', create_reader_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Вы выбрали читателя', create_reader_kb])
                print(user_state['data']['stack'], i)

            elif txt == 'как начать?':
                i += 1
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text=data['reader']['re:pass']['how_to_start'], keyboard=pass_kb)
                if ['Re:pass', re_pass_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Re:pass', re_pass_kb])

            elif txt == 'нет заданий':
                i += 1
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text=data['reader']['re:pass']['no_tasks'], keyboard=pass_kb)
                if ['Re:pass', re_pass_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Re:pass', re_pass_kb])

            elif txt == 'не засчитывается задание':
                i += 1
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text=data['reader']['re:pass']['task_no_counted'], keyboard=pass_kb)
                if ['Re:pass', re_pass_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Re:pass', re_pass_kb])

                # 2) Вопросы по переводу
            elif txt == 'вопросы по переводу':
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Вопросы по переводу',
                              keyboard=question_kb)
                i += 1
                if ['Вы выбрали читателя', create_reader_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Вы выбрали читателя', create_reader_kb])
                moder = False
            elif txt == 'качество перевода':
                i += 1
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Перевожу вас на общение с модератором',
                              keyboard=pass_kb)
                moder = True
                if ['Вопросы по переводу', question_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Вопросы по переводу', question_kb])

            elif txt == 'переводчики не открывают платки':
                if ['Вопросы по переводу', question_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Вопросы по переводу', question_kb])
                i += 1
                answer = 'читатель>вопросы по переводу>переводчики не открывают платки'
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text=answer, keyboard=pass_kb)

                # 3) Другое
            elif txt == 'другое' and user_state['data']['reader']:
                i += 1
                user_state['data']['reader'] = False
                moder = False
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Выберите из предложенного списка', keyboard=read_event_dif)
                if ['Выберите из предложенного списка', create_reader_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложенного списка', create_reader_kb])

            elif txt == 'хочу предложить фичу':
                i += 1
                user.send_msg(vk_session, event.user_id, text='Опишите фичу',
                              keyboard=pass_kb)
                user_state['data']['click_up'] = True
                if ['Выберите из предложеннго списка', read_event_dif] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', read_event_dif])

            elif txt == 'мне дали бан':
                i += 1
                ans = 'читатель>другое>мне дали бан'
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text=ans,
                              keyboard=pass_kb)
                if ['Выберите из предложеннго списка', read_event_dif] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', read_event_dif])

            elif txt == 'позвать модератора':
                i += 1
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Перевожу вас на общение с модератором',
                              keyboard=pass_kb)
                moder = True
                if ['Выберите из предложеннго списка', read_event_dif] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', read_event_dif])

                # 4) Ошибки
            elif txt == 'у меня возникла ошибка':
                i += 1
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Выберите из предложенного списка', keyboard=error_kb)
                if ['Выберите из предложенного списка', create_reader_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложенного списка', create_reader_kb])

            elif txt == 'не грузятся картинки':
                i += 1
                pic_ans = 'читатель>у меня возникла ошибка>картинки'
                user.send_msg(vk_session, event.user_id, text=pic_ans,
                              keyboard=pass_kb)
                if ['Выберите из предложеннго списка', error_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', error_kb])

            elif txt == 'ошибка 500':
                i += 1
                er_500 = 'читатель>у меня возникла ошибка>500'
                user.send_msg(vk_session, event.user_id, text=er_500,
                              keyboard=pass_kb)
                if ['Выберите из предложеннго списка', error_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', error_kb])

            elif txt == 'ошибка 404':
                i += 1
                er_404 = 'читатель>у меня возникла ошибка>404'
                user.send_msg(vk_session, event.user_id, text=er_404,
                              keyboard=pass_kb)
                if ['Выберите из предложеннго списка', error_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', error_kb])

            elif txt == 'я нашел баг':
                i += 1
                user_state['data']['click_up'] = True
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Опишите ошибку', keyboard=pass_kb)
                if ['Выберите из предложеннго списка', error_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', error_kb])

            elif user_state['data']['click_up']:
                click_up_text = event.text
                user_state['data']['click_up'] = False
                print(click_up_text)
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Мы передали ваше сообщение нашим модераторам',
                              keyboard=pass_kb)
                # 5) Не пришли деньги
            elif txt == 'не пришли деньги/тикеты':
                i += 1
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='Не пришли деньги/тикеты',
                              keyboard=money_kb)
                if ['Выберите из предложенного списка', create_reader_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложенного списка', create_reader_kb])
            elif txt == 'не пришли деньги':
                i += 1
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Прошло 24 часа?',
                              keyboard=if_kb_reader_24)
                user_state['data']['money'] = True
                if ['не пришли деньги/тикеты', money_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['не пришли деньги/тикеты', money_kb])

            # не пришли деньги
            elif user_state['data']['money'] and txt == 'да':
                i += 1
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='Привязан к re?',
                              keyboard=if_kb_reader_re)

                if ['Прошло 24 часа?', if_kb_reader_24] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Прошло 24 часа?', if_kb_reader_24])

                user_state['data']['link_re'] = True
                user_state['data']['money'] = False

            elif user_state['data']['money'] and txt == 'нет':
                i += 1
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='Нужно подождать 24 часа',
                              keyboard=pass_kb)
                if ['Прошло 24 часа?', if_kb_reader_24] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Прошло 24 часа?', if_kb_reader_24])
                user_state['data']['money'] = False
            # Привязан к re?
            elif txt == 'да' and user_state['data']['link_re']:
                i += 1
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='Идет пересчет баланса...',
                              keyboard=pass_kb)
                if ['Привязан к re?', if_kb_reader_24] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Привязан к re?', if_kb_reader_24])

                user_state['data']['link_re'] = False
                print('привязан к re?', user_state['data'], 'Все false должно быть')

            elif txt == 'нет' and user_state['data']['link_re']:
                i += 1
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='Привязать к re?',
                              keyboard=if_kb_reader_linked)
                moder = False
                user_state['data']['link_re'] = False
                user_state['data']['linked?'] = True
                if ['Привязан к re?', if_kb_reader_24] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Привязан к re?', if_kb_reader_24])

            elif txt == 'нет' and user_state['data']['link_re']:
                i += 1
                user.send_msg(
                    vk_session=vk_session,
                    user_id=event.user_id,
                    text='Перевожу вас на общение с модератором',
                    keyboard=pass_kb)
                user_state['data']['link_re'] = False
                moder = True
                if ['Привязан к re?', if_kb_reader_24] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Привязан к re?', if_kb_reader_24])
            # Привязал?
            elif txt == 'да' and user_state['data']['linked?']:
                i += 1
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='Идет пересчет баланса...',
                              keyboard=pass_kb)
                user_state['data']['linked?'] = False

                print(vk.messages.getHistory(user_id=event.user_id))

                if ['Привязать к re?', if_kb_reader_linked] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Привязать к re?', if_kb_reader_linked])
            elif txt == 'нет' and user_state['data']['linked?']:
                i += 1
                moder = True
                user.send_msg(
                    vk_session=vk_session,
                    user_id=event.user_id,
                    text='Перевожу вас на общение с модератором',
                    keyboard=pass_kb)
                user_state['data']['linked?'] = False
                print(user_state['data'], 'All False')
                if ['Привязать к re?', if_kb_reader_linked] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Привязать к re?', if_kb_reader_linked])

            elif txt == 'не пришли тикеты':
                i += 1
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='Вы привязаны к re?',
                              keyboard=if_kb_reader_re)
                user_state['data']['link_re'] = True
                if ['не пришли деньги/тикеты', money_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['не пришли деньги/тикеты', money_kb])
            # Проблемы Авторов
            elif txt == 'автор':
                user.send_msg(vk_session=vk_session, user_id=event.user_id, text='Вы выбрали Автора',
                              keyboard=author_kb)
                # if ['Выберите из предложеннго списка', author_kb] not in user_state['data']['stack']:
                #     user_state['data']['stack'].append(['Выберите из предложеннго списка', author_kb])
            # перебор ивентов автора
            elif txt == 'как заливать главы?':
                glvs_ans = 'автор-как заливать главы-'
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text=glvs_ans,
                              keyboard=pass_kb)
                i += 1
                if ['Выберите из предложеннго списка', author_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', author_kb])
            elif txt == 'как выкладывать свою работу?':
                upload_ans = 'автор-как выкладывать свою работу-'
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text=upload_ans,
                              keyboard=pass_kb)
                i += 1
                if ['Выберите из предложеннго списка', error_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', author_kb])

            # Проблемы Переводчика
            elif txt == 'переводчик':
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Вы выбрали Переводчика',
                              keyboard=trans_kb)
                user_state['data']['trans'] = True
                moder = False
            elif txt == 'монетизация':
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Монетизация',
                              keyboard=translator_money_kb)
                i += 1
                if ['Выберите из предложеннго списка', trans_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', trans_kb])
            elif txt == 'как подключить':
                i += 1
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Есть верификация?',
                              keyboard=if_kb_translator)
                user_state['data']['how_link'] = True
                if ['Выберите из предложеннго списка', translator_money_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', translator_money_kb])

            elif txt == 'да' and user_state['data']['how_link']:
                i += 1
                user_state['data']['how_link'] = False
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='действие поставить платки и ответ',
                              keyboard=pass_kb)
                if ['Есть верификация?', if_kb_translator] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Есть верификация?', if_kb_translator])

            elif txt == 'нет' and user_state['data']['how_link']:
                i += 1
                user_state['data']['how_link'] = False
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='действие нужно подписать и ответ',
                              keyboard=pass_kb)
                if ['Есть верификация?', if_kb_translator] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Есть верификация?', if_kb_translator])

            elif txt == 'вопросы по договорам':
                i += 1
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='вопросы по договорам',
                              keyboard=translator_question)
                if ['Монетизация', translator_money_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Монетизация', translator_money_kb])

            elif txt == 'перенос на другое лицо/расторжение':
                ans = 'переводчик-монетизация-вопросы по договорам-перенос'
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text=ans,
                              keyboard=pass_kb)
                i += 1
                if ['Вопросы по договорам', translator_question] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Вопросы по договорам', translator_question])

            elif txt == 'вопросы по подписанию':
                i += 1

                ans = 'переводчик-монетизация-вопросы по договорам-вопросы по подписанию'
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text=ans,
                              keyboard=pass_kb)
                if ['Вопросы по договорам', translator_question] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Вопросы по договорам', translator_question])

            elif txt == 'работа сайта':
                i += 1
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='Глава не заливается',
                              keyboard=work_kb)
                if ['Выберите из предложеннго списка', trans_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', trans_kb])
            elif txt == 'основа':
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='Вес-ответ',
                              keyboard=pass_kb)
                i += 1
                if ['Выберите из предложеннго списка', work_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', work_kb])

            elif txt == 'зеркало. пояснить про реманга.орг':
                user.send_msg(vk_session=vk_session,
                              user_id=event.user_id,
                              text='Ответ про вес тип вес-ответ',
                              keyboard=pass_kb)
                i += 1
                if ['Выберите из предложеннго списка', work_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Выберите из предложеннго списка', work_kb])

            elif txt == 'другое' and user_state['data']['trans']:
                i += 1
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Перевожу вас на общение с модератором',
                              keyboard=pass_kb)
                if ['Вы выбрали переводчика', trans_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Вы выбрали переводчика', trans_kb])

                user_state['trans'] = False

                moder = True

            elif txt == 'перехват/альта/передача тайтла':
                i += 1
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Перевожу вас на общение с модератором',
                              keyboard=pass_kb)
                moder = True
                if ['Вы выбрали переводчика', trans_kb] not in user_state['data']['stack']:
                    user_state['data']['stack'].append(['Вы выбрали переводчика', trans_kb])

            elif txt in ['у вас остались вопросы?',
                         'сменить пользователя']:
                user.send_msg(vk_session=vk_session, user_id=event.user_id,
                              text='Выбор категории:', keyboard=start_kb)
                i = 0
                user_state['data']['trans'] = False
                user_state['data']['reader'] = False
                user_state['data']['money'] = False
                user_state['data']['link_re'] = False
                user_state['data']['linked?'] = False
                user_state['data']['click_up'] = False
                user_state['data']['how_link'] = False
                user_state['data']['stack'] = [['Выберите пользователя', start_kb], ]

            elif txt == 'назад':
                print('Уровень вложенности: ', i)
                if user_state['data']['stack'][i][0] == user_state['data']['stack'][i][0] == 'Прошло 24 часа?':
                    user_state['data']['money'] = True
                elif user_state['data']['stack'][i][0] == user_state['data']['stack'][i][0] == 'Привязан к re?':
                    user_state['data']['link_re'] = True
                    user_state['data']['money'] = False
                elif user_state['data']['stack'][i][0] == user_state['data']['stack'][i][0] == 'Привязать к re?':
                    user_state['data']['linked?'] = True
                elif user_state['data']['stack'][i][0] == user_state['data']['stack'][i][0] == 'Есть верификация?':
                    user_state['data']['how_link'] = True

                user.send_msg(vk_session=vk_session, user_id=event.user_id, text=user_state['data']['stack'][i][0],
                              keyboard=user_state['data']['stack'][i][1])
                user_state['data']['stack'].pop(i)
                print(len(user_state['data']['stack']), i)
                i -= 1

except Exception as ex:
    print(ex)
