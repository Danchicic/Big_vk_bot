from vk_api.keyboard import VkKeyboard


def trans_kb():
    kb = VkKeyboard()
    kb.add_button('Монетизация')
    kb.add_button('Работа сайта')
    kb.add_button('Другое')
    kb.add_line()
    kb.add_button('Перехват/альта/передача тайтла')
    kb.add_line()
    kb.add_button('Назад', color='negative')
    return kb


def translator_money_kb():
    kb = VkKeyboard()
    kb.add_button('Как подключить')
    kb.add_button('Вопросы по договорам')
    kb.add_line()
    kb.add_button('Сменить пользователя')
    kb.add_button('Назад')
    return kb


def translator_question():
    kb = VkKeyboard()
    kb.add_button('Перенос на другое лицо/расторжение')
    kb.add_line()
    kb.add_button('Вопросы по подписанию')
    kb.add_line()
    kb.add_button('Сменить пользователя')
    kb.add_button('Назад')

    return kb


def work_kb():
    kb = VkKeyboard()
    kb.add_button('Основа')
    kb.add_line()
    kb.add_button('Зеркало. пояснить про реманга.орг')
    kb.add_line()
    kb.add_button('Сменить пользователя')
    kb.add_button('Назад')
    return kb
