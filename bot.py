import random

import yaml

from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

bot = Bot(token=config['TOKEN'])
dp = Dispatcher(bot, storage=MemoryStorage())

doc = KeyboardButton('Узнать')
doc_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .add(doc)

citats = config['citats']
auth_id = config['authorized_ids']

async def on_startup(x):
    print('Run')
    # asyncio.create_task(scheduler())

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):

    text = f"ID: {message.from_user}"


    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Чтобы сказал Доктор? Задайте вопрос или попробуйте узнать молча",
        reply_markup=doc_markup
    )

    await bot.send_message(
        chat_id=auth_id[0],
        text=text
    )

@dp.message_handler(lambda message: True)
async def process_start_command(message: types.Message):
    citat_id = random.randint(0, 20)

    await bot.send_message(
        chat_id=auth_id[0],
        text=f"{message.from_user.username}: "+message.text+"\n\n{citats[citat_id]}",
        reply_markup=doc_markup
    )

    await bot.send_message(
        chat_id=message.from_user.id,
        text=citats[citat_id]
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
