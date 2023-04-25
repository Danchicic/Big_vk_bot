from vk_api.keyboard import VkKeyboard


def author_kb():
    kb = VkKeyboard()
    kb.add_button('Как выкладывать свою работу?')
    kb.add_line()
    kb.add_button('Как заливать главы?')
    kb.add_line()
    kb.add_button('Назад', color='negative')
    return kb


