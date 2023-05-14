import telebot
import os

bot = telebot.TeleBot('6250576783:AAF_bUWCqugDQBbqbQOEBavyv4_y3CJACPo')

from telebot import types
from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
from io import BytesIO

img = []

button_blackWhite = types.InlineKeyboardButton(text = 'Ч/Б', callback_data='blackWhite')
button_turn = types.InlineKeyboardButton(text = 'Показать нормали', callback_data='showNormals')
button_findEdges = types.InlineKeyboardButton(text = 'Найти границы', callback_data='findEdges')
button_findInvertEdges = types.InlineKeyboardButton(text = 'Найти инвертированные границы', callback_data='findInvertEdges')
button_info = types.InlineKeyboardButton(text = 'Информация', callback_data='info')

@bot.message_handler(commands=['start'])
def startBot(message):
  first_mess = f"<b>Здравствуйте!\nПожалуйста, загрузите фотографию для обработки</b>"
  bot.send_message(message.chat.id, first_mess, parse_mode='html')

@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
    global img, button_blackWhite, button_turn, button_findEdges, button_info, button_findInvertEdges
    chat_id = function_call.message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(button_blackWhite, button_turn, button_findEdges, button_findInvertEdges, button_info)

    if function_call.data == "blackWhite":
        mess = "Вот Ч/Б изображение! Попробуете ещё что-нибудь?"
        bot.send_photo(chat_id, photo=loadImage(img.convert("L")))
        bot.send_message(chat_id, mess, reply_markup=markup)
        bot.answer_callback_query(function_call.id)
    if function_call.data == "showNormals":
        mess = "Вот карта нормалей изображения! Попробуете ещё что-нибудь?"
        img_gray = img.convert("L")
        img_gray_smooth = img_gray.filter(ImageFilter.SMOOTH)
        emboss = img_gray_smooth.filter(ImageFilter.EMBOSS)
        bot.send_photo(chat_id, photo=loadImage(emboss))
        bot.send_message(chat_id, mess, reply_markup=markup)
        bot.answer_callback_query(function_call.id)
    if function_call.data == "findEdges":
        mess = "Вот примерные границы объектов на изображении! Попробуете ещё что-нибудь?"
        edges = img.convert("L").filter(ImageFilter.FIND_EDGES)
        bot.send_photo(chat_id, photo=loadImage(edges))
        bot.send_message(chat_id, mess, reply_markup=markup)
        bot.answer_callback_query(function_call.id)
    if function_call.data == "findInvertEdges":
        mess = "Вот инвертированные границы объектов на изображении! Попробуете ещё что-нибудь?"
        edges = ImageOps.invert(img.convert("L").filter(ImageFilter.FIND_EDGES))
        bot.send_photo(chat_id, photo=loadImage(edges))
        bot.send_message(chat_id, mess, reply_markup=markup)
        bot.answer_callback_query(function_call.id)
    if function_call.data == "info":
        infoStr = "Формат: " + str(img.format) + "\n" + "Ширина/Высота: " + str(img.size) + "\n" + "Режим: " + str(img.mode) + "\n"
        mess = "Информация об изображении!\n" + infoStr + " Попробуете ещё что-нибудь?"
        bot.send_message(chat_id, mess, reply_markup=markup)
        bot.answer_callback_query(function_call.id)

@bot.message_handler(content_types=["photo"])
def getPhoto(message):
    global img, button_blackWhite, button_turn, button_findEdges, button_findInvertEdges, button_info

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)    
    src = 'tmp/' + file_info.file_path        
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    img = Image.open(src)
    img.load()
    os.remove(src)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(button_blackWhite, button_turn, button_findEdges, button_findInvertEdges, button_info)
    mess = "Изображение загружено! Пожалуйста, выберите желаемое действие"
    bot.send_message(message.chat.id, mess, reply_markup=markup)

def loadImage(img):
    bio = BytesIO()
    bio.name = 'image.jpeg'
    img.save(bio, 'JPEG')
    bio.seek(0)
    return bio

bot.infinity_polling()