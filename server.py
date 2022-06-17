import logging
from aiogram import Bot, Dispatcher, executor, types
from config import token
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold
from services.coin_rate.crypto_parse import get_crypto_course
from services.news.get_news_RSS import get_list_news

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome_message(message: types.Message):
    start_buttons = ["Последние новости 📑", "Топ 3 криптовалюты 💸"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    with open('start_message.txt', 'r') as file:
        start_message = file.read()
    await message.answer(text=start_message, reply_markup=keyboard)


@dp.message_handler(Text(equals="Последние новости 📑"))
async def get_news(message: types.Message):
    await message.answer(text='Собираю новости для вас...')
    news_data = get_list_news()
    await message.answer(news_data)

    # news_dict = get_list_news()
    # for name_source in news_dict:
    #     for news in news_dict[name_source]:
    #         news_data = \
    #             f'Источник: {name_source} \n' \
    #             f'{hitalic(f"Дата публикации:")} {news["publication_time"]} \n' \
    #             f'{hbold(f"Заголовок:")} {news["title"]} \n ' \
    #             f'{hunderline("Содержание:")}' \
    #             f'{news["description"]} \n' \
    #             f'{hlink("Читать далее", news["link"])}'
    #         await message.answer(news_data)



@dp.message_handler(Text(equals="Топ 3 криптовалюты 💸"))
async def get_crypto(message: types.Message):
    await message.answer(text='Собираю данные о валюте для вас...')
    crypto_dict = get_crypto_course()

    for coin in crypto_dict:
        result = \
            f'{hbold(coin["name"])} >>> {coin["price"]}$ \n'  \
            f'Изменение за 24 часа : {coin["changes_24_hours"]}'
        await message.answer(result)


if __name__ == '__main__':
    executor.start_polling(dp)
