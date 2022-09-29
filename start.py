import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from create_bot import dp
from tgbot.handiers.users import register_handlers_client
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True)