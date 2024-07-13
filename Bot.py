import telebot
from currency_converter import CurrencyConverter
import json
import requests

TOKEN = '6893001021:AAFqblDDMntpGcii19ivfPmoVYShr5K4IDg'

bot = telebot.TeleBot(TOKEN)
currency = CurrencyConverter()

keys = {
    'доллор': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
}

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    user_name = message.from_user.first_name
    text = (f'Здравствуйте, {user_name}!\n Что бы перевести валюту введите команду в следующем формате:\n<имя валюты>  '
            f'<в какую валюту переврести> \ <количество переводимой валюты> \n Список доступных валют /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(messadge: telebot.types.Message):
    user_name = messadge.from_user.first_name
    text = f'{user_name}. \n Вам доступны следующие валюты для перевода:'
    for key in keys.keys():
        text = '\n'.join((text, keys[key]))
    bot.reply_to(messadge, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    b = requests.get(f'Сдесь будет ссылка на сайт конвертации')
    total_base = json.loads(b.content)[keys[base]]
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)






bot.polling(non_stop=True)