from author_keyboards import *
from main4 import pass_kb

author_kb = author_kb()


def author(vk_session, user, event, txt):
    if txt == 'автор':
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
        if ['Выберите из предложеннго списка', author_kb] not in user_state['data']['stack']:
            user_state['data']['stack'].append(['Выберите из предложеннго списка', author_kb])
