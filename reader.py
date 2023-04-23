from reader_keyboards import *
from vars_from_bd import READER
from main_kb import pass_keyb
from test import *

pass_kb = pass_keyb()

create_reader_kb = create_reader_kb()
read_event_dif = read_event_dif()
re_pass_kb = re_pass_kb()
question_kb = question_kb()
error_kb = create_error_kb()
money_kb = money_kb()
if_kb_reader_24 = if_kb()
if_kb_reader_re = if_kb()
if_kb_reader_linked = if_kb()


# todo: Сделать тикеты отдельно


def reader(vk_session, user, event, user_state, i):
    get_true_var('READER')

    txt = event.text.lower()
    if txt == 'читатель':
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
        answer = '1answer??????'
        i += 1
        user.send_msg(vk_session=vk_session, user_id=event.user_id,
                      text=answer, keyboard=pass_kb)
        if ['Re:pass', re_pass_kb] not in user_state['data']['stack']:
            user_state['data']['stack'].append(['Re:pass', re_pass_kb])

    elif txt == 'нет заданий':
        i += 1
        answer = '2answer??????'
        user.send_msg(vk_session=vk_session, user_id=event.user_id,
                      text=answer, keyboard=pass_kb)
        if ['Re:pass', re_pass_kb] not in user_state['data']['stack']:
            user_state['data']['stack'].append(['Re:pass', re_pass_kb])

    elif txt == 'не засчитывается задание':
        i += 1
        answer = '3answer??????'
        user.send_msg(vk_session=vk_session, user_id=event.user_id,
                      text=answer, keyboard=pass_kb)
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
        if ['Вопросы по перевду', question_kb] not in user_state['data']['stack']:
            user_state['data']['stack'].append(['Вопросы по перевду', question_kb])

    elif txt == 'переводчики не открывают платки':
        if ['Вопросы по перевду', question_kb] not in user_state['data']['stack']:
            user_state['data']['stack'].append(['Вопросы по перевду', question_kb])
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
    if txt in ['у вас остались вопросы?',
               'сменить пользователя']:
        get_false_var('READER')
