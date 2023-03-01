from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3

from constant import create_new_user_query
from utils import set_integer_flag, check_illnes, check_recipy

TOKEN = '5901370716:AAHAdCqATJZ6WSQRUm4buzP-fivEBdkYLuU'

bot = TeleBot(TOKEN, parse_mode=None)

def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    ilness = KeyboardButton("Чем вы болеете?😷")
    recipy = KeyboardButton("Какой рецепт вам выписали?📝")
    rep = KeyboardButton("Отзывы и предложения📝")

    markup.add(ilness)
    markup.add(recipy, rep)


    return markup


@bot.message_handler(func=lambda message: message.text == "Введите вашу болезнь")
def update_ilness(message):
    chat_id = message.chat.id
    if not check_illnes(chat_id):
        set_integer_flag(1, 'illnes_being_entered', 'user', chat_id)
        bot.send_message(chat_id, "Введите ваше заболевание: ")

@bot.message_handler(func=lambda message: message.text == "Введите ваш рецепт")
def update_recipy(message):
    chat_id = message.chat.id
    if not check_recipy(chat_id):
        set_integer_flag(1, 'recipy_being_entered', 'user', chat_id)
        bot.send_message(chat_id, "Введите рецепт который вам выписали: ")

@bot.message_handler(commands=["start"])
def start_handler(message):
    chat_id = message.chat.id

    create_user(chat_id)

    reply = f"Welcome to your health supporter{message.from_user.first_name} "
    bot.reply_to(message, reply, reply_markup=get_user_details_keyboard(chat_id))
    print(f'Name_of_user - {message.from_user.first_name}')
    print(f'Username_of_user - @{message.from_user.username}')
    print(f'ID_user - {message.from_user.id}')


def get_user_details_keyboard(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    illnes_exist = False
    recipy_exist = False
    if not check_illnes(chat_id):
        get_illnes = KeyboardButton("Введите ваше заболевание: ")
        markup.add(get_illnes)
    else:
        illnes_exist = True
    if not check_recipy(chat_id):
        get_address_button = KeyboardButton("Введите рецепт который вам выписали: ")
        markup.add(get_address_button)
    else:
        recipy_exist = True
    if illnes_exist or recipy_exist:
        markup = main_menu_keyboard()
    return markup

def create_user(chat_id):
    try:
        conn = sqlite3.connect('Pizza_db')
        cursor = conn.cursor()
        sql = create_new_user_query(chat_id)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)

bot.infinity_polling()