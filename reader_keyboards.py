from vk_api.keyboard import VkKeyboard


def create_reader_kb():
    reader_kb = VkKeyboard(one_time=True)
    reader_kb.add_button('Re:pass')
    reader_kb.add_button('Другое')
    reader_kb.add_line()
    reader_kb.add_button('Вопросы по переводу')
    reader_kb.add_button('У меня возникла ошибка')
    reader_kb.add_line()
    reader_kb.add_button('Не пришли деньги/тикеты')
    reader_kb.add_line()
    reader_kb.add_button('Назад', color='negative')
    return reader_kb


def read_event_dif():
    dif_kb = VkKeyboard()
    dif_kb.add_button('Хочу предложить фичу')
    dif_kb.add_line()
    dif_kb.add_button('Мне дали бан')
    dif_kb.add_line()
    dif_kb.add_button('Позвать модератора')
    dif_kb.add_line()
    dif_kb.add_button('Сменить пользователя')
    dif_kb.add_line()
    dif_kb.add_button('Назад')
    return dif_kb


def re_pass_kb():
    kb = VkKeyboard()
    kb.add_button('Как начать?')
    kb.add_button('Нет заданий')
    kb.add_line()

    kb.add_button('Не засчитывается задание')
    kb.add_button('Сменить пользователя')
    kb.add_line()
    kb.add_button('Назад')

    return kb


def question_kb():
    question_kb = VkKeyboard()
    question_kb.add_button('Качество перевода')
    question_kb.add_line()
    question_kb.add_button('Переводчики не открывают платки')
    question_kb.add_line()
    question_kb.add_button('Сменить пользователя')
    question_kb.add_line()
    question_kb.add_button('Назад')

    return question_kb


def create_error_kb():
    kb = VkKeyboard()
    kb.add_button('Не грузятся картинки')
    kb.add_line()
    kb.add_button('Ошибка 500')
    kb.add_button('Ошибка 404')
    kb.add_button('Я нашел баг')
    kb.add_line()
    kb.add_button('Назад')
    return kb


def money_kb():
    money_kb = VkKeyboard()
    money_kb.add_button('Не пришли деньги')
    money_kb.add_button('Не пришли тикеты')
    money_kb.add_line()
    money_kb.add_button('Сменить пользователя')
    money_kb.add_button('Назад')
    return money_kb


def if_kb():
    kb = VkKeyboard()
    kb.add_button('Да')
    kb.add_button('Нет')
    kb.add_line()
    kb.add_button('Сменить пользователя')
    kb.add_button('Назад')
    return kb
