import telethon.tl.types
from telethon.sync import TelegramClient
from config import api_hash, api_id


def spam(target_channel, message):
    with TelegramClient('name', api_id, api_hash) as client:  # 1 session name 2 api_id 3 api_hash
        def get_channel():
            mass = []
            for i in client.get_dialogs():
                if type(i.message.peer_id) == telethon.tl.types.PeerChat:
                    mass.append([i.name, i.message.peer_id])
            return mass

        for i in get_channel():
            if i[0] == target_channel:
                if type(i[1]) == telethon.tl.types.PeerChat:
                    for j in client.get_participants(i[1].chat_id, aggressive=True):
                        try:
                            client.send_message(j.username, message)
                            print(f'Сообщение было отправлено пользователю: {j.username}')
                        except Exception:
                            pass
                    print('Рассылка завершена')
                    exit(0)

        print('Группа не найдена, убедитесь что чат является группой\nПерезапустите скрипт для повтора')

        client.run_until_disconnected()

target = str(input('Введите название группы: '))
message = str(input('Введите сообщение: '))
spam(target, message)