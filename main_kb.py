from vk_api.keyboard import VkKeyboard


def start_kb():
    kb = VkKeyboard(one_time=False)
    kb.add_button('Читатель')
    kb.add_button('Автор')
    kb.add_button('Переводчик')
    return kb


def pass_keyb():
    kb = VkKeyboard(one_time=False)
    kb.add_button('У вас остались вопросы?')
    kb.add_button('Назад')
    return kb
