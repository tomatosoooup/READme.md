import logging
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

places3 = ["https://objor.com/15522-makdonalds.html","https://www.tripadvisor.ru/Restaurant_Review-g295369-d11671887-Reviews-Nikas_Restaurant-Kharkiv_Kharkiv_Oblast.html","https://saycheese.com.ua/biani-champagneria-v-harkove/","https://ru.restaurantguru.com/KFC-Kinnii-rinok-Kharkiv"]
places1=["https://zoo.kharkov.ua/","https://mykharkov.info/catalog/park-im-shevchenko.html","https://centralpark.kh.ua/ua/attrakcziony/","https://izvestia.kharkov.ua/obshchestvo/fjentezi-park-v-harkove-kogda-skazka-ozhivaet-fotoreportazh/"]
places2=["https://www.svadba.kharkov.ua/cat-16-blagoveshhenskij-kafedralnyj-sobor/","http://hatob.com.ua/rus/","https://mykharkov.info/news/top-5-starinnyh-osobnyakov-v-cherte-harkova-13856.html","https://kh.vgorode.ua/reference/muzey/36487-kharkovskyi-ystorycheskyi-muzei"]
places4=["https://kharkov.internet-bilet.ua/ru/events-rubric/8/circus","https://ua-paintball.com/paintball?gclid=EAIaIQobChMI-bKK-fyP9AIVwqfVCh1jGACxEAAYASAAEgLkbPD_BwE","https://www.instagram.com/malina_club_kharkov/?hl=ru","https://south-parka.net/"]
def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Развлечения", callback_data='11'),InlineKeyboardButton("Отдых", callback_data='22'),InlineKeyboardButton("Еда", callback_data='33'),InlineKeyboardButton("Культурное наследие", callback_data='44')],]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    accept = [[InlineKeyboardButton("Принять", callback_data='1'),InlineKeyboardButton("Отказаться", callback_data='2'),InlineKeyboardButton("Показать все", callback_data='3')],]
    reply_markup_accept = InlineKeyboardMarkup(accept)


    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    print(query.data)

    if query.data == '11':
        string = random.choice(places4)
        query.edit_message_text(text=string, reply_markup=reply_markup_accept)
    elif query.data == '22':
        string = random.choice(places1)
        query.edit_message_text(text=string, reply_markup=reply_markup_accept)
    elif query.data == '33':
        string = random.choice(places3)
        #string = places[1]
        query.edit_message_text(text=string, reply_markup=reply_markup_accept)
    elif query.data == '44':
        string = random.choice(places2)
        query.edit_message_text(text=string, reply_markup=reply_markup_accept)
    else:
        query.string_out = 'Bot doesn`t know what to do';

def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2036383413:AAG8wRnkkOlAdDHC-8n9kNVx-UxOJSgaZ_8")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
