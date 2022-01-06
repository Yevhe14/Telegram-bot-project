from pyowm.weatherapi25 import weather
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from pyowm import OWM

owm = OWM('64c773b8f308d6df08cd4ecb5770ff26')
mgr = owm.weather_manager()

My_place = ''

def start(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Це телеграм бот - прогноз погоди\
        \nФункції\
        \n/weather дізнатися прогноз погоди\
        \n/anweather дізнатися прогноз погоди іншої країни/міста \n(приклад: /anweather Київ)\
        \n/add інформацію по обраному місцю")

def anweather(update, context):
    chat = update.effective_chat

    string = update.message.text
    elements = string.split(' ')

    observation = mgr.weather_at_place(elements[1])
    w = observation.weather
    temp = round(w.temperature('celsius')['temp'])

    context.bot.send_message(chat_id = chat.id, text = f"Температура в {elements[1]} - {str(temp)}°C")
    

def weather1(update, context):
    global My_place
    chat = update.effective_chat
    if My_place == '':
        context.bot.send_message(chat_id = chat.id, text = "Інформація по місту не збережена!\
            \nДля збереження міста/країни /add")
    else:
        observation = mgr.weather_at_place(My_place)
        w = observation.weather
        temp = round(w.temperature('celsius')['temp'])

        context.bot.send_message(chat_id = chat.id, text = f"Температура в {My_place} - {str(temp)}°C")
    
def delplace(update, context):
    global My_place
    chat = update.effective_chat
    last_city = My_place
    My_place = ''
    context.bot.send_message(chat_id = chat.id, text = f"Місто {last_city} успішно видалено!")

def add(update, context):
    global My_place
    chat = update.effective_chat
    if My_place == '':
        context.bot.send_message(chat_id = chat.id, text = "Схоже ви ще не додали місце для перегляду погоди\
            \nЩоб додати місце для відстеження введіть /new\
            \nПриклад(/new Київ)")
    else:
        context.bot.send_message(chat_id = chat.id, text = "Інформацію по обраному місцю\
            \n/myplace Перевірка обраного місця (Скоро)\
            \n/delplace Видалення обраного місця\
            \n/chan Змінити місце (/chan Odesa) (Скоро)")

def new(update, context):
    global My_place
    chat = update.effective_chat
    if My_place != "":
        context.bot.send_message(chat_id = chat.id, text = "Місце вже додано\
            \nДля перегляду обраного місця /myplace")
    else:
        string = update.message.text
        elements = string.split(' ')
        My_place = elements[1]
        context.bot.send_message(chat_id = chat.id, text = f"Місто {My_place} успішно додано!\
            \nДля перегляду прогнозу цього місця /weather")


updater = Updater("5051880383:AAESiChZFO2CFribFzQj_WrGQrb2qfXglqk")
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("weather", weather1))
dispatcher.add_handler(CommandHandler("add", add))
dispatcher.add_handler(CommandHandler("new", new))
dispatcher.add_handler(CommandHandler("delplace", delplace))
dispatcher.add_handler(CommandHandler("anweather", anweather))

updater.start_polling()
updater.idle()