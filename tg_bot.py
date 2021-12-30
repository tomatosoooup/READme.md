import telebot
import subForPy
import random
# import logging

from telebot import types

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

bot = telebot.TeleBot(subForPy.TOKEN)
# ----------------Переменные-для-юзера-----------------
name = 'Tom'
surname = 'Bouble'
age = 0
points = 100
messagesToDelete = 0
# --------------------Путь-к-фото----------------------
FILEWAY = 'D:\python\works\static\hello.webp'
FILEWAY2 = 'D:\python\works\static\photo_kh.jpg_large'
# ----------------Пользователи-и-места-----------------
places = [
    'http://bowling.mall.com.ua/',
    'https://icehall.com.ua/,',
    'http://www.izolyatsiya.com.ua/number-1408/'
]

places2 = [
    'https://centralpark.kh.ua/ua/',
    'https://zoo.kharkov.ua/',
    'https://feldman-ecopark.com/uk/'
]
places3 = [
    'http://myasoedov.com.ua/',
    'https://gdeburger.com/',
    'https://eatery.kh.ua/'
]
places4 = [
    'http://morskoimuzei.kh.ua/',
    'http://museum.kh.ua/',
    'https://artmuseum.kh.ua/'
]

our_users = [
    {
        'user':
        {
            'name': name,
            'surname': surname,
            'age': age
        }
    }
]
# ---------------------Работа-бота---------------------


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "If you need a help - use /help")
    sti = open(FILEWAY, 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Выбрать челлендж')
    item2 = types.KeyboardButton('Статистика')
    item3 = types.KeyboardButton('Пожертвования')

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы разнообразить твою рутину. Перед началом используй команду /reg".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['del'])
def deleting(message):
    bot.send_message(message.chat.id, 'Сколько удалить строк ?')
    bot.register_next_step_handler(message, deleteMyMessage)


def deleteMyMessage(message):
    global messagesToDelete
    messagesToDelete = message.text

    while messagesToDelete == 0:
        try:
            messagesToDelete = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Введи цифрами!')

    for id in range((message.message_id-int(messagesToDelete)), message.message_id):
        bot.delete_message(message.chat.id, id)


@bot.message_handler(commands=['help'])
def help_me(message):

    bot.send_message(
        message.chat.id, "1. To start using bot type /start and press ENTER")
    bot.send_message(message.chat.id, "2. Use /reg to create your profile")
    bot.send_message(message.chat.id, "3. Use /del to delete bot's messages")


@bot.message_handler(commands=['reg'])
def registration(message):

    bot.send_message(message.from_user.id,
                     'Я задам парочку вопросов! Как тебя зовут ?')
    bot.register_next_step_handler(message, reg_name)


def reg_name(message):
    global name
    name = message.text
    name = name.lower()
    name = name.capitalize()
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия ?')
    bot.register_next_step_handler(message, reg_surname)


def reg_surname(message):
    global surname
    surname = message.text
    surname = surname.lower()
    surname = surname.capitalize()
    bot.send_message(message.from_user.id, 'Сколько тебе лет ?')
    bot.register_next_step_handler(message, reg_age)


def reg_age(message):
    global age
    age = message.text

    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Введи цифрами!')
    bot.send_message(message.from_user.id, 'Тебя зовут: ' +
                     surname + ' ' + name + ' и тебе: ' + str(age) + ' лет')


@bot.message_handler(content_types=['text'])
def say(message):
    # bot.send_message(message.chat.id,message.text)
    if message.chat.type == 'private':
        if message.text == 'Выбрать челлендж':
            # bot.send_message(message.chat.id, "Nice! Let's try")

            markup = types.InlineKeyboardMarkup(row_width=4)
            item1 = types.InlineKeyboardButton(
                'Развлечения', callback_data='1')
            item2 = types.InlineKeyboardButton('Отдых', callback_data='2')
            item3 = types.InlineKeyboardButton('Еда', callback_data='3')
            item4 = types.InlineKeyboardButton(
                'Культурное наследие', callback_data='4')
            markup.add(item1, item2, item3, item4)

            ph = open(FILEWAY2, 'rb')
            bot.send_message(message.chat.id, 'Выберите категорию: ', bot.send_photo(
                message.chat.id, ph), reply_markup=markup)

        elif message.text == 'Статистика':

            bot.send_message(message.from_user.id, 'Имя: ' + str(name) + '\n' + 'Фамилия: ' + str(surname) + '\n'
                             + 'Возраст: ' + str(age) + '\n' + 'Количество баллов:' + str(points))

            # keyboard
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Изменить данные')
            item2 = types.KeyboardButton('Вернутся обратно')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Всё ли верно ?',
                             reply_markup=markup)

        elif message.text == 'Пожертвования':
            bot.send_message(
                message.chat.id, 'Реквизиты:\n monobank: xxxxxxxxx\n privatbank: xxxxxxxxx')
        elif message.text == 'Изменить данные':  # не реализована
            markup3 = types.InlineKeyboardMarkup(row_width=4)
            item1 = types.InlineKeyboardButton('Имя', callback_data='8')
            item2 = types.InlineKeyboardButton('Фамилия', callback_data='9')
            item3 = types.InlineKeyboardButton('Возраст', callback_data='10')
            markup3.add(item1, item2, item3)
            bot.send_message(
                message.chat.id, 'Что именно стоит поменять ?', reply_markup=markup3)

        elif message.text == 'Вернутся обратно':
            # keyboard
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Выбрать челлендж')
            item2 = types.KeyboardButton('Статистика')
            item3 = types.KeyboardButton('Пожертвования')

            markup.add(item1, item2, item3)

            bot.send_message(
                message.chat.id, 'Вы вернулись обратно!', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Выбрать челлендж')
    item2 = types.KeyboardButton('Статистика')
    item3 = types.KeyboardButton('Пожертвования')

    markup.add(item1, item2, item3)

    markup2 = types.InlineKeyboardMarkup(row_width=4)
    item4 = types.InlineKeyboardButton('Развлечения', callback_data='1')
    item5 = types.InlineKeyboardButton('Отдых', callback_data='2')
    item6 = types.InlineKeyboardButton('Еда', callback_data='3')
    item7 = types.InlineKeyboardButton(
        'Культурное наследие', callback_data='4')
    markup2.add(item4, item5, item6, item7)

    markup3 = types.InlineKeyboardMarkup(row_width=3)
    item8 = types.InlineKeyboardButton("Принять", callback_data='5')
    item9 = types.InlineKeyboardButton("Отказаться", callback_data='6')
    item10 = types.InlineKeyboardButton("Вернутся обратно", callback_data='7')
    markup3.add(item8, item9, item10)

    try:
        if call.message:
            if call.data == '1':
                bot.send_message(call.message.chat.id, random.choice(
                    places), reply_markup=markup3)
            elif call.data == '2':
                bot.send_message(call.message.chat.id, random.choice(
                    places2), reply_markup=markup3)
            elif call.data == '3':
                bot.send_message(call.message.chat.id, random.choice(
                    places3), reply_markup=markup3)
            elif call.data == '4':
                bot.send_message(call.message.chat.id, random.choice(
                    places4), reply_markup=markup3)
            elif call.data == '5':  # принять челлендж
                bot.send_message(
                    call.message.chat.id, 'Отлично! Задание будет помещено к вас в личный кабинет.')
            elif call.data == '6':  # отказаться
                ph = open(FILEWAY2, 'rb')
                bot.send_message(call.message.chat.id, 'Ничего страшного, возможно стоит выбрать что-то другое.',
                                 bot.send_photo(call.message.chat.id, ph), reply_markup=markup2, )
            elif call.data == '7':  # вернуться обратно
                bot.send_message(call.message.chat.id,
                                 'Выберите категорию: ', reply_markup=markup2)
            # elif call.data == '8':
            #     bot.send_message(call.message.chat.id, 'Введите имя: ')
            #     name = call.message.text
            #     bot.send_message(call.message.chat.id,'Имя было изменено!')
            #     return name
            # elif call.data == '9':
            #     bot.send_message(call.message.chat.id, 'Выберите категорию: ', reply_markup=markup)
            # elif call.data == '10':
            #     bot.send_message(call.message.chat.id, 'Выберите категорию: ', reply_markup=markup)

            # remove inline buttons
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вот наше предложение. Ты согласен его выполнить ?",
            #     reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Настало ваше время!")

    except Exception as e:
        print(repr(e))


bot.polling(non_stop=True)








