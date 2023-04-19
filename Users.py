from vk_api.utils import get_random_id


class User:
    def send_msg(self, vk_session, user_id: str, text: str, keyboard=None):
        params = {'user_id': user_id,
                  'message': text,
                  'keyboard': keyboard.get_keyboard(),
                  'random_id': get_random_id()}
        vk_session.method('messages.send', params)
