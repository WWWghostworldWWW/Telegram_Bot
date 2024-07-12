import telebot
from currency_converter import CurrencyConverter



bot = telebot.TeleBot('TOKEN')
currency = CurrencyConverter()



bot.polling(non_stop=True)