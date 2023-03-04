from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3

from constant import create_new_user_query
from utils import set_integer_flag, check_illnes, check_recipy, update_user_filed, get_integer_flag, MenuStack

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

def menu_of_illnesses():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    button1 = KeyboardButton('Простуда')
    button2 = KeyboardButton('Головная боль')
    button3 = KeyboardButton('Температура')
    button4 = KeyboardButton('Лихорадка')
    button5 = KeyboardButton('Ветрянка')
    button6 = KeyboardButton('Коронавирус')
    button7 = KeyboardButton('Рвота')
    button8 = KeyboardButton('Отравление')
    button9 = KeyboardButton('Понос')

    markup.add(button1, button3, button4)
    markup.add(button2, button5, button6)
    markup.add(button7, button8, button9)

    return markup

stack = MenuStack(main_menu_keyboard())
@bot.message_handler(func=lambda message: message.text == "Чем вы болеете?😷")
def update_ilness(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите ваше заболевание: ", reply_markup=menu_of_illnesses())

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

def check_illnes_if_yes_update(chat_id, message):
    if get_integer_flag(column_name='illnes_being_entered',
                        table_name='user',
                        chat_id=chat_id) == 1:
        update_user_filed(chat_id, 'illnes', int(message.text))
        set_integer_flag(0, 'illnes_being_entered', 'user', chat_id)
        bot.send_message(chat_id, "Мы поняли ваше заболевание.", reply_markup=get_user_details_keyboard(chat_id))

def check_recipy_if_yes_update(chat_id, message):
    if get_integer_flag(column_name='recipy_being_entered',
                        table_name='user',
                        chat_id=chat_id) == 1:

        update_user_filed(chat_id, 'recipy', message.text)
        set_integer_flag(0, 'recipy_being_entered', 'user', chat_id)
        bot.send_message(chat_id, "Ваш рецепт принят.", reply_markup=get_user_details_keyboard(chat_id))

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
        conn = sqlite3.connect('pharmacy_db')
        cursor = conn.cursor()
        sql = create_new_user_query(chat_id)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)

@bot.message_handler(func=lambda message: message.text == "Назад⬅️")
def back_handler(message):
    stack.pop()
    menu_to_go_back = stack.top()
    bot.send_message(message.chat.id, "Прошлое меню: ", reply_markup=menu_to_go_back)
    set_integer_flag(0, "quantity_being_entered", "user", message.chat.id)




@bot.message_handler(content_types=['text' , 'contact' , 'location'])
def message_handler(message):

    chat_id = message.chat.id
    create_user(chat_id)
    check_illnes_if_yes_update(chat_id, message)
    check_recipy_if_yes_update(chat_id, message)


    if message.text == "Простуда":
        bot.reply_to(message, "Советуем вам принимать препарат арбидол (Препарат принимают внутрь, до приема пищи. В период эпидемии гриппа и других ОРВИ: детям от 6 до 12 лет - 100 мг, детям старше 12 лет и взрослым - 200 мг 2 раза в неделю в течение 3 недель.) и разводить Терафлю перед сном!")
    '''if message.text == "Головная боль":
        bot.reply_to((message))'''

bot.infinity_polling()

