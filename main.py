from password import passwd, phone
import requests
import json
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkChatEventType



class Server:

        def __init__(self, server_name: str="Empty"):

            self.server_name = server_name
            global api_token
            f = open("token.txt")
            api_token = f.read()

            self.vk = vk_api.VkApi(token=api_token)
            self.long_poll = VkLongPoll(self.vk)

            self.vk_api = self.vk.get_api()


        def send_img(self, send_id, attachment):
                """
                Отправка сообщения через метод messages.send
                :param send_id: vk id пользователя, который получит сообщение
                :param message: содержимое отправляемого письма
                :return: None
                """
                self.vk_api.messages.send(peer_id=send_id,
                                          attachment = attachment,
                                          random_id=123456 + random.randint(1,27))
        def send_msg(self, send_id, message):
            """
            Отправка сообщения через метод messages.send
            :param send_id: vk id пользователя, который получит сообщение
            :param message: содержимое отправляемого письма
            :return: None
            """
            self.vk_api.messages.send(peer_id=send_id,
                                    message=message,
                                    random_id=123456 + random.randint(1,27))

        def start(self):
            for event in self.long_poll.listen():

                if str(event.type.MESSAGE_NEW) == "VkEventType.MESSAGE_NEW":
                    try:
                        master_key = self.vk_api.messages.getLongPollServer()

                        keygen = master_key["key"]
                        server = master_key["server"]
                        ts = master_key["ts"]
                        response = requests.get("https://{}?act=a_check&key={}&ts={}&wait=25&mode=2&version=3".format(server, keygen, ts)).text
                        response = json.loads(response)
                        print(response["updates"][0])

                    except:
                        pass


if __name__ ==  "__main__":
    server1 = Server("server1")
    server1.start() 
