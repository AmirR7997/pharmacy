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
    button10 = KeyboardButton('Назад⬅️')

    markup.add(button1, button3, button4)
    markup.add(button2, button5, button6)
    markup.add(button7, button8, button9)
    markup.add(button10)

    return markup

def menu_of_recipy():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    button1 = KeyboardButton('Арбидол и Терафлю')
    button2 = KeyboardButton('Цитрамон или Аспирин')
    button3 = KeyboardButton('Парацетомол и Ибупрофен')
    button4 = KeyboardButton('Aven cicalfate или Алпиразин')
    button5 = KeyboardButton('Амброксол, Нурофен и Энтросгель')
    button6 = KeyboardButton('Амброксол и Эндросол')
    button7 = KeyboardButton('Назад⬅️')

    markup.add(button1, button3, button4)
    markup.add(button2, button5, button6)
    markup.add(button7)

    return markup

stack = MenuStack(main_menu_keyboard())
@bot.message_handler(func=lambda message: message.text == "Чем вы болеете?😷")
def update_ilness(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите ваше заболевание: ", reply_markup=menu_of_illnesses())

@bot.message_handler(func=lambda message: message.text == "Какой рецепт вам выписали?📝")
def update_recipy(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите ваш рецепт: ", reply_markup=menu_of_recipy())

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
        get_illnes = KeyboardButton("Чем вы болеете?😷")
        markup.add(get_illnes)
    else:
        illnes_exist = True
    if not check_recipy(chat_id):
        get_address_button = KeyboardButton("Какой рецепт вам выписали?📝")
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
        bot.reply_to(message, "Советуем вам принимать препарат арбидол (Препарат принимают внутрь, до приема пищи. В период эпидемии гриппа и других ОРВИ: детям от 6 до 12 лет - 100 мг, детям старше 12 лет и взрослым - 200 мг 2 раза в неделю в течение 3 недель.) и разводить Терафлю перед сном! Вы можете найти данные лекарства в Зеленой аптеке, она находится на ц1, рядом с Cake Lab их номер: 71 232 06 83")
    if message.text == "Головная боль":
        bot.reply_to(message, "Советуем вам принять цитрамон, но применять его часто не желательно помимо цитрамона можете использовать ибупрофен, ацетаминофен, напроксен или аспирин. Принимайте анальгетики, содержащие кофеин. В состав большинства обезболивающих, которые помогают при головной боли или мигрени, входит не только анальгезирующий препарат, но и кофеин. Данные препараты имеются в каждой аптеке, можете сходить в ближайшую к вам")
    if message.text == "Температура":
        bot.reply_to(message, "Если ваша температура меньше 38, то сбивать ее не желательно, просто ждите, а если ваша температура 38 и выше, то примите парацетомол, ибупрофен, ацетилсалициловая кислоту или метамизол натрия. Эти лекарства вы сможете найти в аптеке Cardio pharm адресс: 17 Osiyo ko'chasi. Номер телефона: 71 235 79 78")
    if message.text == "Лихорадка":
        bot.reply_to(message, "Прием лекарственных препаратов жаропонижающего действия. Это может быть парацетамол, аспирин (противопоказан детям до 12 лет), ибупрофен в таблетках или сиропе. Преимущества жидкого состава – в возможности его точной дозировке и легкости проглатывания, что особенно актуально для детей. Так же не забывайте пить много воды и достаточно отдыхать. Данные препараты можно найти в аптеках: 999-у них много филлиалов, сходите в ближайших к вам, их номер телефона:(71 202 09 99), Зеленой аптеке, она находится на ц1, рядом с Cake Lab их номер:71 232 06 83 и в аптеке Cardio pharm адресс: 17 Osiyo ko'chasi. Номер телефона: 71 235 79 78 ")
    if message.text == "Ветрянка":
        bot.reply_to(message, "К применению рекомендуется Aven cicalfate лосьон подсушивающий 40 мл, Алпизарин мазь 2% туб 10, Алпизарин таблетки 100 мг n20, Анаферон детский капли для приёма внутрь 25 мл и Ацикловир 200 мг 20 табл, так же советуем не чесать ранки. Эти препараты можно отыскать в аптеках: Данные препараты можно найти в аптеках: 999-у них много филлиалов, сходите в ближайших к вам, их номер телефона:(71 202 09 99), Зеленой аптеке, она находится на ц1, рядом с Cake Lab их номер:71 232 06 83 и в аптеке Cardio pharm адресс: 17 Osiyo ko'chasi. Номер телефона: 71 235 79 78 ")
    if message.text == "Коронавирус":
        bot.reply_to(message, "Рекомендуются отхаркивающие: Амброксол, Бромгексин, Ацетилцистеин и др. Жаропонижающие: Парацетамол (свечи, таблетки, сироп), Нурофен, Аспирин (взрослые старше 18 лет). Сорбенты: Смекта, Энтеросгель, Полифепан и др. Локальные антисептики для полоскания: Шалфей, Эвкалипт, Себидин, Стрепсилс, Спреи антисептические. Данные лекарства можно найти в любой аптеке, сходите в ближайшую к вам!")
    if message.text == "Рвота":
        bot.reply_to(message, "При рвоте и диарее мы теряем большое количество жидкости, которую нужно восполнять. Когда потери не очень обильные, достаточно просто пить воду. Пейте небольшими глотками, но часто — это поможет справиться с тошнотой, не провоцируя рвотный рефлекс. Если пить не получается, можно начать с рассасывания кубиков льда. Имбирь, имбирный чай, эль или леденцы обладают противорвотным эффектом и могут помочь снизить частоту рвотных позывов; ароматерапия, или вдыхание запахов лаванды, лимона, мяты, розы или гвоздики, может приостановить позывы к рвоте; использование акупунктуры также может уменьшить выраженность тошноты.")
    if message.text == "Отравление":
        bot.reply_to(message, "Итак, промывание желудка слабым раствором соды (до чистой воды), прием энтеросорбента (активированный уголь, смекта), питье воды (во избежание обезвоживания) и покой. Важный момент: ни коем случае до приезда врача нельзя принимать обезболивающие, противорвотные и противодиарейные препараты.")
    if message.text == "Понос":
        bot.reply_to(message, "Противодиарейные комбинированные средства – Смекта, Диосмектит, Диоктаб Солюшн таблетки, Неосмектин, Эндосор. Данные лекарства можно найти в любой аптеке, сходите в ближайшую к вам!")
    if message.text == "Назад⬅️":
        bot.reply_to(message, f'Здравствуйте<b>{message.from_user.first_name}💛</b>!\n'
                              f'Вы вернулись в главное меню', parse_mode='html', reply_markup=main_menu_keyboard())
    if message.text == "Арбидол и Терафлю":
        bot.reply_to(message, "Скорее всего у вас простуда, вы можете найти данный препараты в данных аптеках: 999-у них много филлиалов, сходите в ближайших к вам, их номер телефона:(71 202 09 99), Зеленой аптеке, она находится на ц1, рядом с Cake Lab их номер:71 232 06 83 и в аптеке Cardio pharm адресс: 17 Osiyo ko'chasi. Номер телефона: 71 235 79 78")
    if message.text == "Цитрамон или Аспирин":
        bot.reply_to(message, "У вас скорее всего головная боль вы можете найти эти препараты в данных аптеках: 999-у них много филлиалов, сходите в ближайших к вам, их номер телефона:(71 202 09 99), Зеленой аптеке, она находится на ц1, рядом с Cake Lab их номер:71 232 06 83 и в аптеке Cardio pharm адресс: 17 Osiyo ko'chasi. Номер телефона: 71 235 79 78")
    '''if message.text == "Отравление":
        bot.reply_to(message, "999-у них много филлиалов, сходите в ближайших к вам, их номер телефона:(71 202 09 99), Зеленой аптеке, она находится на ц1, рядом с Cake Lab их номер:71 232 06 83 и в аптеке Cardio pharm адресс: 17 Osiyo ko'chasi. Номер телефона: 71 235 79 78")
    if message.text == "Отравление":
        bot.reply_to(message, "999-у них много филлиалов, сходите в ближайших к вам, их номер телефона:(71 202 09 99), Зеленой аптеке, она находится на ц1, рядом с Cake Lab их номер:71 232 06 83 и в аптеке Cardio pharm адресс: 17 Osiyo ko'chasi. Номер телефона: 71 235 79 78")
    if message.text == "Отравление":
        bot.reply_to(message, "999-у них много филлиалов, сходите в ближайших к вам, их номер телефона:(71 202 09 99), Зеленой аптеке, она находится на ц1, рядом с Cake Lab их номер:71 232 06 83 и в аптеке Cardio pharm адресс: 17 Osiyo ko'chasi. Номер телефона: 71 235 79 78")
    if message.text == "Отравление":
        bot.reply_to(message, "999-у них много филлиалов, сходите в ближайших к вам, их номер телефона:(71 202 09 99), Зеленой аптеке, она находится на ц1, рядом с Cake Lab их номер:71 232 06 83 и в аптеке Cardio pharm адресс: 17 Osiyo ko'chasi. Номер телефона: 71 235 79 78")
    if message.text == "Отравление":
        bot.reply_to(message, "999-у них много филлиалов, сходите в ближайших к вам, их номер телефона:(71 202 09 99), Зеленой аптеке, она находится на ц1, рядом с Cake Lab их номер:71 232 06 83 и в аптеке Cardio pharm адресс: 17 Osiyo ko'chasi. Номер телефона: 71 235 79 78")'''



bot.infinity_polling()

