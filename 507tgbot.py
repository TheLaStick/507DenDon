import telebot
import random
from telebot import types

# Обходим блокировку с помощью прокси
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

token = "902421898:AAHQOBPp2EQfjIs9bpqhDaSxxgCZaiTeGf4"
bot = telebot.TeleBot(token=token)

role = {}  # список людей
information = {}  # словарь новостей
homework = {}  # словарь домашки
active = {}  # индикатор

active[1] = 0
active[2] = 0
active[3] = 0
active[4] = 0
codes = [147258369, 123654789, 963258741, 9517538462, 486217935, 963852741]  # коды
code = random.choice(codes)


@bot.message_handler(commands=["start"])
def main_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    user = message.chat.id
    # добавляем на нее две кнопки
    buthw = types.InlineKeyboardButton(text="Домашние задания", callback_data="buthw")
    butinfo = types.InlineKeyboardButton(text="Новости", callback_data="butinfo")
    if user not in role:
        butnewrole = types.InlineKeyboardButton(text="Войти как преподаватель", callback_data="butnewrole")
        keyboard.add(butnewrole)
    keyboard.add(buthw)
    keyboard.add(butinfo)
    if user in role:
        butnew = types.InlineKeyboardButton(text="Создать", callback_data="butnew")
        keyboard.add(butnew)
        butdel = types.InlineKeyboardButton(text="Удалить контент", callback_data="butdel")
        keyboard.add(butdel)
    # отправляем сообщение пользователю
    bot.send_message(user, "Выберете действие", reply_markup=keyboard)


# функция запустится, когда пользователь нажмет на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    keyboard = types.InlineKeyboardMarkup()
    user = call.message.chat.id
    if call.message:
        if call.data == "buthw":
            bot.send_message(user, "На какую дату?")
            active[1] = 1
        if call.data == "butinfo":
            bot.send.message(user, "На какую дату?")
            active[2] = 1
        if call.data == "butnew":
            if user in role:
                butnewhw = types.InlineKeyboardButton(text="Домашнее задание", callback_data="butnewhw")
                butnewinfo = types.InlineKeyboardButton(text="Новость", callback_data="butnewinfo")
                keyboard.add(butnewhw)
                keyboard.add(butnewinfo)
                bot.send_message(user, "", reply_markup=keyboard)
        if call.data == "butnewhw":  # Новая домашка
            active[3] = 1
            bot.send_message(user, "Чтобы создать новое домашнее задание, напишите сначала текст, потом дату")
        if call.data == "butnewinfo":  # Новая новость
            active[4] = 1
            bot.send_message(user, "Чтобы создать новость, напишите сначала текст, потом дату")
        if call.data == "butnewrole":  # Вход за преподавателя
            print(code)
            active[5] = 1
            bot.send_message(user, "Введите пароль")
        if call.data == "butdel":  # Удаление контента
            active[6] = 1
            bot.send_message(user, "")


@bot.message_handler(content_types=["text"])
def new(message):
    if active[1] == 1:  # Домашка
        user = message.chat.id
        text = message.text
        if homework[text] in homework:
            bot.send_message(user, homework[text])
        else:
            bot.send_message(user, "Ничего нет на эту дату")

    elif active[2] == 1:  # Новости
        user = message.chat.id
        text = str(message.text)
        if information[text] in information:
            bot.send_message(user, information[text])
        else:
            bot.send_message(user, "Ничего нет на эту дату")

    elif active[3] == 1:
        user = message.chat.id
        text = message.text
        if user in role:
            hw = text
            homework[user] = hw
            active[1] = 0
            bot.send_message(user, "Сохранено")
            print(homework)
        else:
            bot.send_message(user, "У вас нет прав на это действие")

    elif active[4] == 1:
        user = message.chat.id
        text = message.text
        active[2] = 0
        if user in role:
            info = text
            information[user] = info
            active[2] = 0
            bot.send_message(user, "Сохранено")
            print(information)
        else:
            bot.send_message(user, "У вас нет прав на это действие")

    elif active[5] == 1:
        user = message.chat.id
        text = int(message.text)
        active[3] == 0
        if text == code:
            role[user] = user
            bot.send_message(user, "Вы добавлены")
            print(role)
        else:
            bot.send_message(user, "Неправильный пароль")

    elif active[6] == 1:
        user = message.chat.id

    else:
        bot.send_message(message.chat.id, "Ошибка")


bot.polling(none_stop=True)
