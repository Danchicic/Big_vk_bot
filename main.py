import json
from Users import Bot
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import TOKEN

with open('actions.json', 'r') as f:
    data = json.load(f)

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpolling = VkLongPoll(vk_session)
try:
    for event in longpolling.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()

            bot = Bot(msg, event.user_id, vk_session)
            bot.hand_message()

except Exception as ex:
    print('error', ex)
