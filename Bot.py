import os
from typing import Optional
import telebot
from dotenv import load_dotenv
from telebot.types import (Message, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from values import VALUES
from TOKEN import token
from extensions import Converter, DataValidationException





COMMANDS_BUTTONS = ReplyKeyboardMarkup(resize_keyboard=True) #Создаём переменную встроенныч кнопок в клавиатуре
COMMANDS_BUTTONS.add('/start', '/help', '/values', '/convert') #Называем созданные кнопки


load_dotenv()
#token = os.getenv('TOKEN')
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
            f'\n Выбирите валюту, из которой желаете конвертировать, а также валюту в которую будем конвертировать.'
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
    text = 'Какую валюту нужно конвертировать?'
    reply_markup = COMMANDS_BUTTONS
    bot.send_message(message.chat.id, text, reply_markup=reply_markup)
    bot.register_next_step_handler(message, ask_base)#регистрируем следующий шаг. Функцию запроса первой валюты


def ask_base(message: Message) -> None:#Функция ввода первой валюты

    try:
        base = message.text.strip()
    except AttributeError:#Исключение при неправильном вводе валюты
        text = 'Давайте попробуем ещё раз!!!'
        reply_markup = COMMANDS_BUTTONS
        bot.register_next_step_handler(message, ask_base)#Возврашаем функцию первой валюты
    else:
        text = 'В какую валюту конвертируем?'
        reply_markup = COMMANDS_BUTTONS
        bot.register_next_step_handler(message, ask_quote, base)#Регистрируем следующий шаг.Функцию второй валюты
    finally:
        bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)


def ask_quote(message: Message, base: str) -> None:#Функция ввода второй валюты

    try:
        quote = message.text.strip()
    except AttributeError:#Исключение при неправильном вводе валюты
        text = 'Давайте попробуем ещё раз!!!'
        reply_markup = make_smart_keyboard(key=quote)
        bot.register_next_step_handler(message, ask_quote, quote)#Возвращаем функцию второй валюты
    else:
        text = 'Введите сумму сколько хотите конвертировать!'
        reply_markup = ReplyKeyboardRemove()
        bot.register_next_step_handler(message, ask_base_amount, ask_base, quote)#Регистрируем следующий шаг.Функцию суммы валюты
    finally:
        bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)

def ask_base_amount(message: Message, base: str, quote: str) -> None:#Функция ввода суммы первой валюты

    try:
        base_amount = message.text.strip()
    except AttributeError:#Исключение при неправильном вводе суммы валюты
        text = 'Давайте попробуем ещё раз!!!'
        reply_markup = ReplyKeyboardRemove
        bot.register_next_step_handler(message, ask_base_amount, base, quote)#Возвращаем функцию ввода суммы валюты
    else:
        try:
            text = Converter.convert(base_amount, base, quote)#При соблюдении условий: производим конвертацию
        except DataValidationException as e:#Сообщение об ошибки ввода валют вне диапозона задданых в боте валют
            text = e
        except Exception as e:#Сообщение при невозможности связаться с сайтом для конвертации
            text = f'Что-то пошло не так:\n\n{e}\n\nПопробуйте позже!'
        finally:
            reply_markup = COMMANDS_BUTTONS
    finally:
        bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)









bot.polling(non_stop=True)

