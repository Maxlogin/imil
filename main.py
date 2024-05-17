import telebot
import sqlite3
import random
import csv
TOKEN = '7103782951:AAEdkkP9DlvYBLEN2bc13Z1NCDgtygrFVXM'

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Введите следующую информацию:")
    bot.send_message(message.chat.id, "Фамилия:")
    bot.register_next_step_handler(message, get_lastname)

def get_lastname(message):
    lastname = message.text
    bot.send_message(message.chat.id, "Имя:")
    bot.register_next_step_handler(message, get_firstname, lastname)

def get_firstname(message, lastname):
    firstname = message.text
    bot.send_message(message.chat.id, "Отчество:")
    bot.register_next_step_handler(message, get_middlename, lastname, firstname)

def get_middlename(message, lastname, firstname):
    middlename = message.text
    bot.send_message(message.chat.id, "Дата рождения (в формате ГГГГ-ММ-ДД):")
    bot.register_next_step_handler(message, save_data, lastname, firstname, middlename)

def save_data(message, lastname, firstname, middlename):
    birthday = message.text
    userid = message.chat.id
    username = message.chat.first_name

    con = sqlite3.connect('Tatarin.db')
    cur = con.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS tgbot
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid integer,
        username TEXT,
        f TEXT,
        i TEXT,
        o TEXT,
        birthday TEXT)'''
    )
    cur.execute('''INSERT INTO tgbot (userid, username, f, i, o, birthday) VALUES (?, ?, ?, ?, ?, ?)''',
                (userid, username, lastname, firstname, middlename, birthday))


    cur.execute('''SELECT * FROM tgbot''')
    with open('TGBOTExport.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writter = csv.writer(csvfile)
        csv_writter.writerow(['id', 'userid', 'username', 'f', 'i', 'o', 'birthday'])
        csv_writter.writerows(cur)

    con.commit()
    con.close()

    bot.reply_to(message, "Ваши данные!")

if __name__ == '__main__':
    bot.polling()
