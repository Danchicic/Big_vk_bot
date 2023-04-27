import json
from Users import User
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import TOKEN

user = User()

with open('actions.json', 'r') as f:
    data = json.load(f)

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpolling = VkLongPoll(vk_session)


def get_func(name_def: str):
    pass


for event in longpolling.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        for row in data:
            if msg in row['text']:
                user.send_msg(vk_session=vk_session, user_id=event.user_id, text='Re:pass',
                              keyboard=row['func'])
