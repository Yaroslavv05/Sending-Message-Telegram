import telethon.tl.types
from telethon.sync import TelegramClient
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, dp
from aiogram.dispatcher.filters import Text

markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
markup.add('Начать!')


async def spam(target_channel, message, bot, chat_id):
    async with TelegramClient('name', 12345678, 'API_HASH') as client:  # 1 session name 2 api_id 3 api_hash
        async def get_channel():
            mass = []
            for i in await client.get_dialogs():
                if type(i.message.peer_id) == telethon.tl.types.PeerChat:
                    mass.append([i.name, i.message.peer_id])
            return mass

        for i in await get_channel():
            if i[0] == target_channel:
                if type(i[1]) == telethon.tl.types.PeerChat:
                    await bot.send_message(chat_id, 'Рассылка начата')
                    for j in await client.get_participants(i[1].chat_id, aggressive=True):
                        try:
                            await client.send_message(j.username, message)
                        except Exception:
                            pass
                    await bot.send_message(chat_id, 'Рассылка окончена')
                    return

        await bot.send_message(chat_id, 'Группа не найдена, убедитесь что чат является группой\nПовторите еще раз: /start')

        client.run_until_disconnected()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await bot.send_message(message.from_user.id, 'Нажми кнопку "Начать!"', reply_markup=markup)


class fmain(StatesGroup):
    name_group = State()
    message = State()


async def main(message: types.Message):
    await fmain.name_group.set()
    await bot.send_message(message.from_user.id, 'Введите название группы которая у вас есть в чатах!')


async def message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_group'] = message.text
    await fmain.message.set()
    await bot.send_message(message.from_user.id, 'Введите наполнения рассылки')


async def start_sending(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text
    await spam(data['name_group'], data['message'], bot, message.chat.id)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(main, Text(equals='Начать!'))
    dp.register_message_handler(message, state=fmain.name_group)
    dp.register_message_handler(start_sending, state=fmain.message)