from translator_keyboards import *
from reader.reader_keyboards import if_kb
from main_kb import pass_keyb
pass_kb = pass_keyb()

work_kb = work_kb()
translator_question = translator_question()
translator_money_kb = translator_money_kb()
trans_kb = trans_kb()
if_kb_translator = if_kb()


def translator_main(vk_session: vk_session, user, event, txt):
    if txt == 'переводчик':
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
