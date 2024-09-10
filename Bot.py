from typing import Optional
import telebot
from dotenv import load_dotenv
from telebot.types import (Message, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from values import VALUES
from TOKEN import token
from extensions import APIException, CurrencyConverter





COMMANDS_BUTTONS = ReplyKeyboardMarkup(resize_keyboard=True) #Создаём переменную встроенных кнопок в клавиатуре
COMMANDS_BUTTONS.add('/start', '/help', '/values', '/convert') #Называем созданные кнопки


load_dotenv()
bot = telebot.TeleBot(token)


def make_smart_keyboard(key: Optional[str] = None) -> ReplyKeyboardMarkup:#Создаём кнопки


    dictionary = VALUES.copy()

    if key and dictionary.get(key.lower()):
        dictionary.pop(key.lower())

    if not len(dictionary) % 3:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    elif not len(dictionary) % 2:
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(*[key.capitalize() for key in dictionary.keys()])
    return keyboard


@bot.message_handler(commands=['start'])#Оброботчик команды /start
def command_start(message: Message) -> None:
    user_name = message.from_user.full_name
    text = (f'Приветствую вас, {user_name}! \n Я конвертер валют. \n Мои команды: \n Нажмите /help , если нужна помощь;'
            f' \n Нажмите /values, что бы узнать список доступных валют, для конвертации; '
            f'\n Нажмите /convert, для конвертации')
    reply_markup = COMMANDS_BUTTONS
    bot.send_message(message.chat.id, text, reply_markup=reply_markup)



@bot.message_handler(commands=['help'])#Оброботчик команды /help
def command_help(message: Message) -> None:
    text = (f'***ИНСТРУКЦИЯ***\n __________________________ \n \n Для того, что бы конвертировать валюту, нажмите '
            f'кнопку /convert.'
            f'\n Введите валюту, из которой желаете конвертировать, а также валюту в которую будем конвертировать.'
            f'\n Затем введите желаемую сумму для конвертации')
    reply_markup = COMMANDS_BUTTONS
    bot.send_message(message.chat.id, text, reply_markup=reply_markup)



@bot.message_handler(commands=['values'])#Оброботчик команды /values
def command_values(message: Message) -> None:
    values = '\n'.join(VALUES)
    text = (f'Вам доступны следующие валюты для конвертации: \n\n $$$$$$$$$$$$$$$$$$$$$$\n \n {values} \n ')
    reply_markup = COMMANDS_BUTTONS
    bot.send_message(message.chat.id, text, reply_markup=reply_markup)



@bot.message_handler(commands=['convert'])#Оброботчик команды /convert
def command_convert(message: Message) -> None:
    text = (f'Через пробел!!!! \n Введите валюту которую желаете конвертировать, затем в какую конвертируем и сумму')
    reply_markup = COMMANDS_BUTTONS
    bot.send_message(message.chat.id, text, reply_markup=reply_markup)
    bot.register_next_step_handler(message, convert_currency)#регистрируем следующий шаг. Функцию запроса первой валюты


@bot.message_handler(content_types=['text'])
def convert_currency(massage):
    try:
        VALUES = massage.text.split()

        if len(VALUES) != 3:
            raise APIException('Неправильное количество параметров. Введите три параметра!')

        base, quote, amount = VALUES
        converted_amount = CurrencyConverter.get_price(base, quote, amount)
        text = f'Цена {amount} {base} в {quote} - {converted_amount}'
        bot.reply_to(massage, text)

    except APIException as e:
        bot.reply_to(massage, 'Ошибка пользователя. \n{e}')
    except APIException as e:
        bot.reply_to(massage, 'Ошибка при обработке команды. \n{e}')








if __name__ == '__main__':

    bot.polling(non_stop=True)

