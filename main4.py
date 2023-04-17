import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import TOKEN

from Users import User
from reader_keyboards import *
from author_keyboards import *
from translator_keyboards import *


def create_kb(buttons: list, one_time: bool = False):
    kb = VkKeyboard(one_time=one_time)
    for el in buttons:
        kb.add_button(el)
    return kb


pass_kb = VkKeyboard(one_time=False)
pass_kb.add_button('У вас остались вопросы?')
pass_kb.add_button('Назад')
start_kb = create_kb(['Читатель', 'Автор', 'Переводчик'], one_time=False)

# Авторизация пользователя
vk_session = vk_api.VkApi(token=TOKEN)
longpolling = VkLongPoll(vk_session)
i = 0
user = User()
states = {}

for event in longpolling.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        click_up = 0
        user_id = event.user_id

        if user_id not in states:
            # Новый пользователь, создаем новое состояние
            states[user_id] = {"state": "start", "data": {}}
            user_state = states[user_id]
            user_state['data']['trans'] = False
            user_state['data']['reader'] = False
            user_state['data']['money'] = False
            user_state['data']['link_re'] = False
            user_state['data']['linked?'] = False
            user_state['data']['click_up'] = False
            user_state['data']['how_link'] = False
            user_state['data']['stack'] = [['Выберите пользователя', start_kb], ]
        user_state = states[user_id]

        print('us s', user_state)
        print(states)
        txt = event.text.lower()
        if txt == 'начать':
            user.send_msg(vk_session=vk_session, user_id=event.user_id, text='Выбор категории:',
                          keyboard=start_kb)

        elif txt == 'читатель':
            click_up = 0
            user.send_msg(vk_session=vk_session, user_id=event.user_id, text='Вы выбрали читателя',
                          keyboard=create_reader_kb())
            user_state['data']['reader'] = True
            # user_state['data']['last_msg'] = ['Выбор категории:', start_kb]
            # перебор ивентов читателя

            # 1) Re:pass
        elif txt == 're:pass':
            user.send_msg(vk_session=vk_session, user_id=event.user_id, text='Re:pass',
                          keyboard=re_pass_kb())
            i += 1
            if ['Вы выбрали читателя', create_reader_kb()] not in user_state['data']['stack']:
                user_state['data']['stack'].append(['Вы выбрали читателя', create_reader_kb()])
            print(user_state['data']['stack'], i)

        elif txt == 'как начать?':
            answer = '1answer??????'
            i += 1
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text=answer, keyboard=pass_kb)
            if ['Re:pass', re_pass_kb()] not in user_state['data']['stack']:
                user_state['data']['stack'].append(['Re:pass', re_pass_kb()])

        elif txt == 'нет заданий':
            i += 1
            answer = '2answer??????'
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text=answer, keyboard=pass_kb)
            user_state['data']['stack'].append(['Re:pass', re_pass_kb()])

        elif txt == 'не засчитывается задание':
            i += 1
            answer = '3answer??????'
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text=answer, keyboard=pass_kb)
            user_state['data']['stack'].append(['Re:pass', re_pass_kb()])

            # 2) Вопросы по переводу
        elif txt == 'вопросы по переводу':
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Вопросы по переводу',
                          keyboard=question_kb())
            i += 1
            user_state['data']['stack'] = ['Вы выбрали читателя', create_reader_kb()]
            moder = False
        elif txt == 'качество перевода':
            i += 1
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Перевожу вас на общение с модератором',
                          keyboard=pass_kb)
            moder = True
            user_state['data']['stack'] = ['Вопросы по перевду', question_kb()]


        elif txt == 'переводчики не открывают платки':
            user_state['data']['stack'] = ['Вопросы по перевду', question_kb()]
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
                          text='Выберите из предложенного списка', keyboard=read_event_dif())
            user_state['data']['stack'] = ['Выберите из предложенного списка', create_reader_kb()]

        elif txt == 'хочу предложить фичу':
            i += 1
            user.send_msg(vk_session, event.user_id, text='Опишите фичу',
                          keyboard=pass_kb)
            user_state['data']['click_up'] = True
            user_state['data']['stack'] = ['Выберите из предложеннго списка', read_event_dif()]


        elif txt == 'мне дали бан':
            i += 1
            ans = 'читатель>другое>мне дали бан'
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text=ans,
                          keyboard=pass_kb)
            user_state['data']['stack'] = ['Выберите из предложеннго списка', read_event_dif()]



        elif txt == 'позвать модератора':
            i += 1
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Перевожу вас на общение с модератором',
                          keyboard=pass_kb)
            moder = True
            user_state['data']['stack'] = ['Выберите из предложеннго списка', read_event_dif()]


            # 4) Ошибки
        elif txt == 'у меня возникла ошибка':
            i += 1
            error_kb = create_error_kb()
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Выберите из предложенного списка', keyboard=error_kb)
            user_state['data']['stack'] = ['Выберите из предложенного списка', create_reader_kb()]

        elif txt == 'не грузятся картинки':
            i += 1
            pic_ans = 'читатель>у меня возникла ошибка>картинки'
            user.send_msg(vk_session, event.user_id, text=pic_ans,
                          keyboard=pass_kb)
            user_state['data']['stack'] = ['Выберите из предложеннго списка', error_kb]

        elif txt == 'ошибка 500':
            i += 1
            er_500 = 'читатель>у меня возникла ошибка>500'
            user.send_msg(vk_session, event.user_id, text=er_500,
                          keyboard=pass_kb)
            user_state['data']['stack'] = ['Выберите из предложеннго списка', error_kb]


        elif txt == 'ошибка 404':
            i += 1
            er_404 = 'читатель>у меня возникла ошибка>404'
            user.send_msg(vk_session, event.user_id, text=er_404,
                          keyboard=pass_kb)
            user_state['data']['stack'] = ['Выберите из предложеннго списка', error_kb]


        elif txt == 'я нашел баг':
            click_up = 1
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Опишите ошибку', keyboard=pass_kb)
            user_state['data']['stack'] = ['Выберите из предложеннго списка', error_kb]

        elif click_up:
            click_up_text = event.text
            click_up = 0
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Мы передали ваше сообщение нашим модераторам',
                          keyboard=pass_kb)
            # 5) Не пришли деньги
        elif txt == 'не пришли деньги/тикеты':
            i += 1
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='Не пришли деньги/тикеты',
                          keyboard=money_kb())
            user_state['data']['stack'] = ['Выберите из предложенного списка', create_reader_kb()]
        elif txt == 'не пришли деньги':
            i += 1
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Прошло 24 часа?',
                          keyboard=if_kb())
            user_state['data']['money'] = True
            # user_state['data']['last_msg'] = ['Не пришли деньги/тикеты', money_kb()]
        ##не пришли деньги
        elif user_state['data']['money'] and txt == 'да':
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='Привязан к ре?',
                          keyboard=if_kb())
            # user_state['data']['last_msg'] = ['Прошло 24 часа?', if_kb()]
            user_state['data']['link_re'] = True
            user_state['data']['money'] = False

        elif user_state['data']['money'] and txt == 'нет':

            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='Нужно подождать 24 часа',
                          keyboard=pass_kb)
            user_state['data']['money'] = False
        ##Привязан к re?
        elif txt == 'да' and user_state['data']['link_re']:
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='Идет пересчет баланса...',
                          keyboard=pass_kb)
            user_state['data']['link_re'] = False
            print('привязан к ре?', user_state['data'], 'Все false должно быть')

        elif txt == 'нет' and user_state['data']['link_re']:
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='Привязать к ре?',
                          keyboard=if_kb())
            moder = False
            user_state['data']['link_re'] = False
            user_state['data']['linked?'] = True
        elif txt == 'нет' and user_state['data']['link_re']:
            user.send_msg(
                vk_session=vk_session,
                user_id=event.user_id,
                text='Перевожу вас на общение с модератором',
                keyboard=pass_kb)
            user_state['data']['link_re'] = False
            moder = True
        ##Привязал?
        elif txt == 'да' and user_state['data']['linked?']:
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='Идет пересчет баланса...',
                          keyboard=pass_kb)
            user_state['data']['linked?'] = False
        elif txt == 'нет' and user_state['data']['linked?']:
            moder = True
            user.send_msg(
                vk_session=vk_session,
                user_id=event.user_id,
                text='Перевожу вас на общение с модератором',
                keyboard=pass_kb)
            user_state['data']['linked?'] = False
            print(user_state['data'], 'All False')

        elif txt == 'не пришли тикеты':
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='Вы привязаны к ре?',
                          keyboard=if_kb())
            user_state['data']['link_re'] = True

        # Проблемы Авторов
        elif txt == 'автор':
            user.send_msg(vk_session=vk_session, user_id=event.user_id, text='Вы выбрали Автора',
                          keyboard=author_kb())
        # перебор ивентов автора
        elif txt == 'как заливать главы?':
            glvs_ans = 'автор-как заливать главы-'
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text=glvs_ans,
                          keyboard=pass_kb)
        elif txt == 'как выкладывать свою работу?':
            upload_ans = 'автор-как выкладывать свою работу-'
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text=upload_ans,
                          keyboard=pass_kb)

        # Проблемы Переводчика
        elif txt == 'переводчик':
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Вы выбрали Переводчика',
                          keyboard=trans_kb())
            user_state['data']['trans'] = True
            moder = False
        elif txt == 'монетизация':
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Монетизация',
                          keyboard=translator_money_kb())
        elif txt == 'как подключить':
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Есть верификация?',
                          keyboard=if_kb())
            user_state['data']['how_link'] = True
        elif txt == 'да' and user_state['data']['how_link']:
            user_state['data']['how_link'] = False
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='действие поставить платки и ответ',
                          keyboard=pass_kb)

        elif txt == 'нет' and user_state['data']['how_link']:
            user_state['data']['how_link'] = False
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='действие нужно подписать и ответ',
                          keyboard=pass_kb)

        elif txt == 'вопросы по договорам':
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='вопросы по договорам',
                          keyboard=translator_question())
        elif txt == 'перенос на другое лицо/расторжение':
            ans = 'переводчик-монетизация-вопросы по договорам-перенос'
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text=ans,
                          keyboard=pass_kb)

        elif txt == 'вопросы по подписанию':
            ans = 'переводчик-монетизация-вопросы по договорам-вопросы по подписанию'
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text=ans,
                          keyboard=pass_kb)

        elif txt == 'работа сайта':
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='Глава не заливается',
                          keyboard=work_kb())
        elif txt == 'основа':
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='Вес-ответ',
                          keyboard=pass_kb)

        elif txt == 'зеркало. пояснить про реманга.орг':
            user.send_msg(vk_session=vk_session,
                          user_id=event.user_id,
                          text='Ответ про вес тип вес-ответ',
                          keyboard=pass_kb)

        elif txt == 'другое' and user_state['data']['trans']:
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Перевожу вас на общение с модератором',
                          keyboard=pass_kb)
            user_state['trans'] = False

            moder = True

        elif txt == 'перехват/альта/передача тайтла':
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Перевожу вас на общение с модератором',
                          keyboard=pass_kb)
            moder = True

        elif txt in ['у вас остались вопросы?',
                     'сменить пользователя']:
            start_kb = create_kb(['Читатель', 'Автор', 'Переводчик'], one_time=False)
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Выбор категории:', keyboard=start_kb)
            i = 0
            user_state['data']['trans'] = False
            user_state['data']['reader'] = False
            user_state['data']['stack'] = [['Выберите пользователя', start_kb], ]

        elif txt == 'назад':
            if user_state['data']['link_re']:
                print(user_state['data']['link_re'], '_-_--___--_----_---_-_--_')
                user_state['data']['link_re'] = False
                user_state['data']['money'] = True

            user.send_msg(vk_session=vk_session, user_id=event.user_id, text=user_state['data']['stack'][i][0],
                          keyboard=user_state['data']['stack'][i][1])
        if user_state['data']['click_up']:
            # Отправить таск на сайт
            click_up_text = event.text
            print(click_up_text)
            user_state['data']['click_up'] = False
            user.send_msg(vk_session=vk_session, user_id=event.user_id,
                          text='Мы передали ваше сообщение нашим модераторам',
                          keyboard=pass_kb)
