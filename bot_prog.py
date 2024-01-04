import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings['API_TOKEN'])
dp = Dispatcher(bot)


async def start_command(message: types.Message):
    await message.answer("Введите /commands, чтобы ознакомиться со списком доступных комманд")


async def get_crypto_price(message: types.Message):
    try:
        # Получаем аргумент после команды /crypto
        arg = message.get_args().lower()

        # Определяем, является ли введенный аргумент тикером (symbol) или названием криптовалюты (name)
        coin_info_url = f"https://api.coingecko.com/api/v3/coins/{arg}"
        response = requests.get(coin_info_url)

        if response.status_code == 200:
            # Если успешно нашли информацию по тикеру
            coin_info = response.json()
            name = coin_info['name']
            symbol = coin_info['symbol']
            price = coin_info['market_data']['current_price']['usd']
            trading_volume = coin_info['market_data']['total_volume']['usd']
            price_change_24h = coin_info['market_data']['price_change_24h']
            price_change_percentage_24h = coin_info['market_data']['price_change_percentage_24h']

            # Форматируем числа с разделителями тысяч
            formatted_trading_volume = '{:,}'.format(trading_volume)
            formatted_price_change_24h = '{:,.3f}'.format(price_change_24h)
            formatted_price_change_percentage_24h = '{:,.3f}'.format(price_change_percentage_24h)

            text = (
                f"Курс {name} ({symbol}): {price} USD\n"
                f"Объем торгов за 24 часа: {formatted_trading_volume} USD\n"
                f"Изменение цены за 24 часа: {formatted_price_change_24h} USD ({formatted_price_change_percentage_24h}%)"
            )
            await message.answer(text)
        else:
            # Если не удалось найти информацию по тикеру, пробуем найти по названию
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={arg}&vs_currencies=usd"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                # Если успешно нашли информацию по названию
                price = data[arg]['usd']
                text = f"Курс {arg.capitalize()}: {price} USD"
                await message.answer(text)
            else:
                # Если не удалось найти информацию ни по тикеру, ни по названию
                await message.answer(f"Не удалось найти информацию по криптовалюте с тикером или названием: {arg}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")


async def get_top10_cryptos(message: types.Message):
    try:

        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            top10_text = "Топ 10 криптовалют по рыночной капитализации:\n"
            for index, crypto in enumerate(data, start=1):
                name = crypto['name']
                symbol = crypto['symbol']
                price = crypto['current_price']
                top10_text += f"{index}. {name} ({symbol.upper()}): ${price}\n"

            await message.answer(top10_text)
        else:
            await message.answer(f"Ошибка при получении данных: {data['error']['info']}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")


async def list_commands(message: types.Message):
    commands_text = "Доступные команды:\n/start - Начать \n/crypto <код_валюты> - Получить курс криптовалюты \n/commands - Список команд" \
                    "\n/top - топ 10 самых популярных криптовалют"
    await message.answer(commands_text)


dp.register_message_handler(start_command, commands=['start'])
dp.register_message_handler(get_crypto_price, commands=['crypto'])
dp.register_message_handler(list_commands, commands=['commands'])
dp.register_message_handler(get_top10_cryptos, commands=['top'])


executor.start_polling(dp, skip_updates=True)