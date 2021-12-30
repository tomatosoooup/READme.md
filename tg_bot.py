import telebot
import subForPy
import random
# import logging

from telebot import types

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, replymarkup
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

# -------------------Все-панели-бота-------------------
# 1. Панель выбора челленджей, статистики и доната
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Choose challenge')
item2 = types.KeyboardButton('Statistics')
item3 = types.KeyboardButton('Donation')
markup.add(item1, item2, item3)
# 2. Панель выбора категорий заданий
markup2 = types.InlineKeyboardMarkup(row_width=4)
item4 = types.InlineKeyboardButton(
    'Entertainment', callback_data='1')
item5 = types.InlineKeyboardButton('Rest', callback_data='2')
item6 = types.InlineKeyboardButton('Food', callback_data='3')
item7 = types.InlineKeyboardButton(
    'Culture', callback_data='4')
markup2.add(item4, item5, item6, item7)
# 3. Панель возврата или изменения информации
markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
item8 = types.KeyboardButton('Change information')
item9 = types.KeyboardButton('Return')
markup3.add(item8, item9)
# 4. Панель принятия изменений информации об пользователе
# Указана в коде, из-за проблем с областью видимости
# 5. Панель принятия, отказа или возврата
markup5 = types.InlineKeyboardMarkup(row_width=3)
item12 = types.InlineKeyboardButton("Accept", callback_data='5')
item13 = types.InlineKeyboardButton("Deny", callback_data='6')
item14 = types.InlineKeyboardButton("Return", callback_data='7')
markup5.add(item12, item13, item14)

# ---------------------Работа-бота---------------------


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "If you need a help - use /help")
    sti = open(FILEWAY, 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Welcome, {0.first_name}!\nI am - <b>{1.first_name}</b>, bot, created to diversify your routine. Before starting use /reg command".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['del'])
def deleting(message):
    bot.send_message(message.chat.id, 'How many lines to delete ?')
    bot.register_next_step_handler(message, deleteMyMessage)


def deleteMyMessage(message):
    global messagesToDelete
    messagesToDelete = message.text

    while messagesToDelete == 0:
        try:
            messagesToDelete = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Enter numbers!')

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
                     'I will give you a couple of questions! What is your name ?')
    bot.register_next_step_handler(message, reg_name)


def reg_name(message):
    global name
    name = message.text
    name = name.lower()
    name = name.capitalize()
    bot.send_message(message.from_user.id, 'What is your surname ?')
    bot.register_next_step_handler(message, reg_surname)


def reg_surname(message):
    global surname
    surname = message.text
    surname = surname.lower()
    surname = surname.capitalize()
    bot.send_message(message.from_user.id, 'How old are you ?')
    bot.register_next_step_handler(message, reg_age)


def reg_age(message):
    global age
    age = message.text

    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Enter numbers!')
    bot.send_message(message.from_user.id, 'Your name: ' +
                     surname + ' ' + name + ' and you are: ' + str(age) + ' y.o')

    bot.send_message(message.chat.id, 'Well ! Information was added',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def say(message):

    markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item10 = types.KeyboardButton('Yes')
    item11 = types.KeyboardButton('No')
    markup4.add(item10, item11)

    if message.chat.type == 'private':
        if message.text == 'Choose challenge':
            ph = open(FILEWAY2, 'rb')
            bot.send_message(message.chat.id, 'Choose cathegory: ', bot.send_photo(
                message.chat.id, ph), reply_markup=markup2)

        elif message.text == 'Statistics':

            bot.send_message(message.from_user.id, 'Name: ' + str(name) + '\n' + 'Surname: ' + str(surname) + '\n'
                             + 'Age: ' + str(age) + '\n' + 'Points:' + str(points))

            bot.send_message(message.chat.id, 'Is everything right ?',
                             reply_markup=markup3)

        elif message.text == 'Donation':
            bot.send_message(
                message.chat.id, 'Requisites:\n monobank: xxxxxxxxx\n privatbank: xxxxxxxxx')
        elif message.text == 'Change information':
            bot.send_message(
                message.chat.id, 'Please choose Yes/No', reply_markup=markup4)

        elif message.text == 'Return':
            bot.send_message(
                message.chat.id, 'You went back!', reply_markup=markup)
        elif message.text == 'Yes':
            bot.send_message(message.from_user.id,
                             'What is your name ?')
            bot.register_next_step_handler(message, reg_name)
        elif message.text == 'No':
            markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item11 = types.KeyboardButton('Change information')
            item12 = types.KeyboardButton('Return')
            markup4.add(item11, item12)
        else:
            bot.send_message(message.chat.id, "I don't know what to say 😢")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    try:
        if call.message:
            if call.data == '1':
                bot.send_message(call.message.chat.id, random.choice(
                    places), reply_markup=markup5)
            elif call.data == '2':
                bot.send_message(call.message.chat.id, random.choice(
                    places2), reply_markup=markup5)
            elif call.data == '3':
                bot.send_message(call.message.chat.id, random.choice(
                    places3), reply_markup=markup5)
            elif call.data == '4':
                bot.send_message(call.message.chat.id, random.choice(
                    places4), reply_markup=markup5)
            elif call.data == '5':  # принять челлендж
                bot.send_message(
                    call.message.chat.id, 'Well.This challenge will be added to your cabinet')
            elif call.data == '6':  # отказаться
                ph = open(FILEWAY2, 'rb')
                bot.send_message(call.message.chat.id, 'Sad :( Probably you can choose another one).',
                                 bot.send_photo(call.message.chat.id, ph), reply_markup=markup2)
            elif call.data == '7':  # вернуться обратно
                bot.send_message(call.message.chat.id,
                                 'Choose cathegory: ', reply_markup=markup2)

            # remove inline buttons
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вот наше предложение. Ты согласен его выполнить ?",
            #     reply_markup=None)

            # show alert
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            #                           text="It's your time!")

    except Exception as e:
        print(repr(e))


bot.polling(non_stop=True)




