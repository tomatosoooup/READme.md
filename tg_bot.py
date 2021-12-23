import logging
import random
import requests
import csv
import json 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

url = 'https://innovations.kh.ua/ucan/wp-json/wp/v2/place/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r = requests.get(url,headers=headers)
jsn = r.json()

FILENAME = 'test.json'
with open(FILENAME,'w') as file:
    file.write(json.dumps(jsn,indent= 3))

def get_content():
    info = []
    with open(FILENAME,'r') as file:
        data = json.load(file)
        print(data)

    for i in data:
        info.append(i)
        print(info)
    return info

get_content()

FILENAME = "users.csv"
users = [
    {"name":"Tom", "Age": 18},
    {"name":"Dave", "Age": 23},
    {"name":"Mave", "Age": 19},
    {"name":"Olha", "Age": 22}
]
placesToGo = [
    {"place":"MacDonalds", "adress": "https://objor.com/15522-makdonalds.html"}
]
places = [
    ["https://www.tripadvisor.ru/Restaurant_Review-g295369-d11671887-Reviews-Nikas_Restaurant-Kharkiv_Kharkiv_Oblast.html","https://saycheese.com.ua/biani-champagneria-v-harkove/","https://ru.restaurantguru.com/KFC-Kinnii-rinok-Kharkiv"],
    ["https://zoo.kharkov.ua/","https://mykharkov.info/catalog/park-im-shevchenko.html","https://centralpark.kh.ua/ua/attrakcziony/","https://izvestia.kharkov.ua/obshchestvo/fjentezi-park-v-harkove-kogda-skazka-ozhivaet-fotoreportazh/"],
    ["https://www.svadba.kharkov.ua/cat-16-blagoveshhenskij-kafedralnyj-sobor/","http://hatob.com.ua/rus/","https://mykharkov.info/news/top-5-starinnyh-osobnyakov-v-cherte-harkova-13856.html","https://kh.vgorode.ua/reference/muzey/36487-kharkovskyi-ystorycheskyi-muzei"],
    ["https://kharkov.internet-bilet.ua/ru/events-rubric/8/circus","https://ua-paintball.com/paintball?gclid=EAIaIQobChMI-bKK-fyP9AIVwqfVCh1jGACxEAAYASAAEgLkbPD_BwE","https://www.instagram.com/malina_club_kharkov/?hl=ru","https://south-parka.net/"],
]

def help_me(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("/start - Начало работы с ботом")

def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Развлечения", callback_data='1'),InlineKeyboardButton("Отдых", callback_data='2'),InlineKeyboardButton("Еда", callback_data='3'),InlineKeyboardButton("Культурное наследие", callback_data='4')],]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)


def buttonChoose(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    accept = [[InlineKeyboardButton("Принять", callback_data='11'),InlineKeyboardButton("Отказаться", callback_data='22'),InlineKeyboardButton("Вернутся", callback_data='33')],]
    reply_markup_accept = InlineKeyboardMarkup(accept)


    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    print(query.data)

    if query.data == '1':
        string = random.choice(places)
        query.edit_message_text(text=string, reply_markup=reply_markup_accept)

    elif query.data == '2':
        string = random.choice(places)
        query.edit_message_text(text=string, reply_markup=reply_markup_accept)
        
    elif query.data == '3':
        string = random.choice(places)
        #string = places[1]
        query.edit_message_text(text=string, reply_markup=reply_markup_accept)

    elif query.data == '4':
        string = random.choice(places)
        query.edit_message_text(text=string, reply_markup=reply_markup_accept)

    # elif query.data == '11':
        # task = 
        #Записать в файл Id пользователя (получить по чатId), Id заведения, дату

    else:
        query.string_out = 'Bot doesn`t know what to do'


# def help_command(update: Update, context: CallbackContext) -> None:
#     """Displays info on how to use the bot."""
#     update.message.reply_text("Use /start to test this bot.")

def complete_achievement(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Сдать задание", callback_data='1')],]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Отправьте нам фотографию:', reply_markup=reply_markup)

# открытие файла для записи
def openfile(FILENAME):
    with open(FILENAME, "w", newline = "") as file:
        columns = ["name","Age"]
        writer = csv.DictWriter(file,fieldnames=columns)
        writer.writeheader()
        writer.writerows(users)

# добавление пользователя
def addUser(FILENAME):
    columns = ["name","Age"]
    name = input("Enter your name: ") 
    age = input("Enter your age: ")
    user = {"name":name, "Age": age}
    with open(FILENAME, "a", newline = "") as file:
        writer = csv.DictWriter(file,fieldnames=columns)
        writer.writerow(user)

# чтение из файла
def readFile(FILENAME):
    with open(FILENAME, "r", newline = "") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row["name"], " - ", row["Age"])

def addPlace():
    with open("places.csv","w", newline= "")as file:
        columns = ["place", "adress"]
        writer = csv.DictWriter(file,fieldnames=columns)
        writer.writeheader()
        writer.writerows(placesToGo)


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2036383413:AAG8wRnkkOlAdDHC-8n9kNVx-UxOJSgaZ_8")
    do = updater.dispatcher.add_handler
    do(CommandHandler('start', start))
    do(CallbackQueryHandler(buttonChoose))
    do(CommandHandler('help', help_me))
    do(CallbackQueryHandler('achieve', complete_achievement))


if __name__ == '__main__':
    main()



    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
