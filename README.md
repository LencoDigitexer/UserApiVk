# UserApiVk
Временное решение по приему сообщений через user longpoll api vk

# Настройка

     pip3 install -r requirements.txt

В password.py необходимо записать логин и пароль от вк

    phone = 88005553535
    passwd = "Vasya_pupkin228"

Затем потребуется запустить take_token.py для получения токена от kate_mobile

    python take_token.py

Этот токен запишется в token.txt

# Работа скрипта

В скрипте main.py сделана реализация приёма сообщений.
В функции start

```python
for event in self.long_poll.listen(): # записываем в переменную все события от ВК
    if str(event.type.MESSAGE_NEW) == "VkEventType.MESSAGE_NEW": # если это новое сообщение
        try: # используем обнаружитель ошибок

            # функция получения номера события https://vk.com/dev/messages.getLongPollServer
            master_key = self.vk_api.messages.getLongPollServer()
            keygen = master_key["key"]
            server = master_key["server"]
            ts = master_key["ts"]
            #################################

            # отправляем запрос на получение данных с помощью ключа выше
            response = requests.get("https://{}?act=a_check&key={}&ts={}&wait=25&mode=2&version=3".format(server, keygen, ts)).text

            #загружаем данные в json
            response = json.loads(response)

            # получаем данные см Формат ответа
            print(response["updates"][0])
            '''
            [4, 636184, 8243, 2000000008, 1587111284, 'тест', {'from': '510166866'}, {}]

            '''

        except:
            pass
```

# Формат ответа

Источник - https://vk.com/dev/using_longpoll_3

updates (array) — массив, элементы которого содержат представление новых событий (каждый элемент также является массивом). Длина массива updates может быть равна 0 (это означает, что за время wait новых событий не произошло).

peer_id (integer) — идентификатор назначения. Для пользователя: id пользователя. Для групповой беседы: 2000000000 + id беседы. Для сообщества: -id сообщества либо id сообщества + 1000000000 = 2000000008

    response["updates"][0][3]

timestamp (integer) — время отправки сообщения в Unixtime;

    response["updates"][0][4]

text (string) — текст сообщения;

    response["updates"][0][5]

От кого сообщение:

    response["updates"][0][6]["from"]

[$attachments] (array) — вложения (если mode = 2);

    response["updates"][0][7]
    {'attach1_type': 'doc', 'attach1': '510166866_546393866'}


# Отправка сообщения
Просто отправка текста
```python
    self.send_msg(peer_id, send_text)
    peer_id = response["updates"][0][6]["from"] # отправка пользователю
    # или
    peer_id = response["updates"][0][3] # отправка в беседу
    send_text = "some text"
```

Отправка изображения

```python
    self.send_img(peer_id, send_text, attachment)
    peer_id = response["updates"][0][6]["from"] # отправка пользователю
    # или
    peer_id = response["updates"][0][3] # отправка в беседу
    attachment = "photo" + твой id вк + "_" + id изображения в твоем альбоме
    # пример - photo510166866_457241739
```