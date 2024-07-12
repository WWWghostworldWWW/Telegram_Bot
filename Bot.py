import telebot
from currency_converter import CurrencyConverter

TOKEN = '6893001021:AAFqblDDMntpGcii19ivfPmoVYShr5K4IDg'

bot = telebot.TeleBot(TOKEN)
currency = CurrencyConverter()

keys = {
    'USD': 'USD',
    'EUR': 'EUR',
    'JPY': 'JPY',
}

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Что бы перевести валюту введите команду в следующем формате:\n<имя валюты>  <в какую валюту переdрести> \
    <количество переводимой валюты>')
    bot.reply_to(message, text)

bot.polling(non_stop=True)