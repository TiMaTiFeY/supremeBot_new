import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_bot_database import VkBotDataBase
from vk_bot_enums import *
import random


class VkBot:
    def __init__(self, api_token, group_id, bot_name: str = "Empty"):
        # Даем боту имя
        self._bot_name = bot_name

        # Для Long Poll
        self._vk = vk_api.VkApi(token=api_token)

        # Для использования Long Poll API
        self._long_poll = VkBotLongPoll(self._vk, group_id)

        # Для вызова методов vk_api
        self._vk_api = self._vk.get_api()

        # База данных бота
        self._db = VkBotDataBase()

    def _send_msg(self, send_id, message):
        self._vk_api.messages.send(peer_id=send_id,
                                   random_id=int(random.randint(1, 1000)),
                                   message=message)

    def _remove_user(self, peer_id, user_id):
        self._vk_api.messages.removeChatUser(chat_id=peer_id,
                                             user_id=user_id)

    def _get_user_name_by_id(self, user_id):
        response = self._vk_api.users.get(user_ids=user_id)[0]
        return response['first_name'] + ' ' + response['last_name']

    def start(self):
        print("Bot has started")
        self._db.add_user_permission('210025769', 'ADMIN')
        for event in self._long_poll.listen():  # Слушаем сервер
            if event.type == VkBotEventType.MESSAGE_NEW:
                self._parse_command(event)

    def _parse_command(self, event):
        msg = event.obj['message']['text']
        from_id = event.obj['message']['from_id']
        peer_id = event.obj['message']['peer_id']

        if msg.startswith('/'):
            command_name = msg.split(' ')[0][1::]

            if not(command_name in ALL_COMMANDS):
                self._send_msg(peer_id, "Неверная команда")
            else:

                # Get user permission
                user_permission = self._db.get_user_permission(from_id)
                if len(user_permission) == 0:
                    self._db.add_user_permission(from_id, UserType.simple.to_name())
                    user_permission = UserType.simple
                else:
                    user_permission = UserType.from_name(user_permission[0][0])

                print(user_permission)

                if command_name in Commands.respect.value[1]:
                    self._command_respect(event, user_permission)

                if command_name in Commands.mafia.value[1]:
                    self._command_mafia(event, user_permission)

    def _command_respect(self, event, user_permission):
        msg = event.obj['message']['text']
        from_id = event.obj['message']['from_id']
        peer_id = event.obj['message']['peer_id']
        if user_permission.value >= Commands.respect.value[0].value:
            other_part = msg.split(' ')[1::]

            user_id = ''.join(other_part)
            if user_id[0] == '[' and user_id[-1] == ']':
                user_id = user_id.split('|')[0][3::]
            else:
                user_id = ''

            if user_id == '':
                self._send_msg(peer_id, 'Неверный ввод пользователя')
            else:
                user_id = int(user_id)
                name = self._get_user_name_by_id(user_id)

                if user_id == from_id:
                    self._send_msg(peer_id, 'Нарцисс чертов! А ну пошел вон')
                else:
                    score_now = self._db.get_user_respect(user_id)
                    new_score = 1
                    if len(score_now) != 0:
                        new_score = score_now[0][0] + 1
                        self._db.update_user_respect(user_id, new_score)
                    else:
                        self._db.add_user_respect(user_id, new_score)

                    self._send_msg(peer_id, name + ' ' + str(new_score) + ' уважуха_score')
        else:
            self._send_msg(peer_id, 'Недостаточно прав')

    def _command_mafia(self, event, user_permission):
        msg = event.obj['message']['text']
        from_id = event.obj['message']['from_id']
        peer_id = event.obj['message']['peer_id']
        if user_permission.value >= Commands.respect.value[0].value:
            other_part = list(map(int, msg.split(' ')[1::]))
        #     мирных, мафии, дон, комиссар, доктор
            if len(other_part) != 5:
                self._send_msg(peer_id,
                               "Неправильно введены данные, введите кол-во мирных, мафии, дона, комиссара, доктора "
                               "через пробел. Например /mafia 3 2 1 0 1 ")
            else:
                list_of_players = []
                for i in range(other_part[0]):
                    list_of_players.append("Мирный")
                for i in range(other_part[1]):
                    list_of_players.append("Мафия")
                for i in range(other_part[2]):
                    list_of_players.append("Дон")
                for i in range(other_part[3]):
                    list_of_players.append("Комиссар")
                for i in range(other_part[4]):
                    list_of_players.append("Доктор")
                result = ''
                i = 1
                while len(list_of_players) != 0:
                    random_index = random.randint(0, len(list_of_players) - 1)
                    result += "{} - {}\n".format(i, list_of_players[random_index])
                    list_of_players.pop(random_index)
                    i += 1
                self._send_msg(peer_id, result)
        else:
            self._send_msg(peer_id, 'Недостаточно прав')