from telebot import types
import telebot
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
import os

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)


def keyboard_1():
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=False)
    button1 = types.KeyboardButton('Курсы валют')
    button2 = types.KeyboardButton('Калькулятор валют')
    button3 = types.KeyboardButton('Динамика курса валют')
    markup1.add(button1), markup1.add(button2), markup1.add(button3)
    return markup1


def keyboard_2():
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=False)
    button4 = types.KeyboardButton('Курс Доллора')
    button5 = types.KeyboardButton('Курс Евро')
    button6 = types.KeyboardButton('Курс Биткоина')
    button7 = types.KeyboardButton('Назад')
    markup2.add(button4), markup2.add(button5), markup2.add(button6), markup2.add(button7)
    return markup2


def keyboard_3():
    markup3 = types.ReplyKeyboardMarkup(resize_keyboard=False)
    button8 = types.KeyboardButton('Доллор в рубли')
    button9 = types.KeyboardButton('Евро в рубли')
    button10 = types.KeyboardButton('Биткоин в рубли')
    button11 = types.KeyboardButton('Назад')
    markup3.add(button8), markup3.add(button9), markup3.add(button10), markup3.add(button11)
    return markup3


def keyboard_4():
    markup4 = types.ReplyKeyboardMarkup(resize_keyboard=False)
    button12 = types.KeyboardButton('Динамика Доллара')
    button13 = types.KeyboardButton('Динамика Евро')
    button14 = types.KeyboardButton('Динамика Биткоина')
    button15 = types.KeyboardButton('Назад')
    markup4.add(button12), markup4.add(button13), markup4.add(button14), markup4.add(button15)
    return markup4


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет! Что тебя интересует? Воспользуйся интерактивной клавиатурой.",
                     reply_markup=keyboard_1())
    bot.register_next_step_handler(message, keyboard)


@bot.message_handler()
def keyboard(message):
    if message.text == 'Курсы валют':
        bot.send_message(message.from_user.id, 'Какая валюта Вас интересует? Воспользуйтесь интерактивной клавиатурой.',
                         reply_markup=keyboard_2())
        bot.register_next_step_handler(message, Courses)
    elif message.text == 'Калькулятор валют':
        bot.send_message(message.from_user.id,
                         'Какую валюту хотите перевести в рубли? Воспользыйтесь интреактивной клавиатурой.',
                         reply_markup=keyboard_3())
        bot.register_next_step_handler(message, Calculator)
    elif message.text == 'Динамика курса валют':
        bot.send_message(message.from_user.id, 'Динамика какой валюты вас интересует?',
                         reply_markup=keyboard_4())
        bot.register_next_step_handler(message, Dynamics)
    else:
        bot.send_message(message.from_user.id, 'Я Вас не понимаю. Что вас интересует?'
                                               ' Воспользуйтесь интерактивной клвавиатурой.',
                         reply_markup=keyboard_1())


def Courses(message):
    parameter = True
    if message.text == 'Курс Доллора':
        dollar(message, parameter)
    elif message.text == 'Курс Евро':
        euro(message, parameter)
    elif message.text == 'Курс Биткоина':
        bitcoin(message, parameter)
    elif message.text == 'Назад':
        f_exit(message)
    else:
        bot.send_message(message.from_user.id, 'Я не понимаю. Что вас интересует?'
                                               ' Воспользуйтесь интерактивной клвавиатурой.',
                         reply_markup=keyboard_2())
        bot.register_next_step_handler(message, Courses)


def Calculator(message):
    if message.text == 'Доллор в рубли':
        bot.send_message(message.from_user.id,
                         'Введите количество долларов.'
                         ' В качестве разделителя между целой и дробной частью используйте "."')
        bot.register_next_step_handler(message, count_dollar)
    elif message.text == 'Евро в рубли':
        bot.send_message(message.from_user.id,
                         'Введите количество евро. В качестве разделителя между целой и дробной частью используйте "."')
        bot.register_next_step_handler(message, count_euro)
    elif message.text == 'Биткоин в рубли':
        bot.send_message(message.from_user.id,
                         'Введите количество биткоинов.'
                         ' В качестве разделителя между целой и дробной частью используйте "."')
        bot.register_next_step_handler(message, count_bitcoin)
    elif message.text == 'Назад':
        f_exit(message)
    else:
        bot.send_message(message.from_user.id,
                         'Я не понимаю. Что вас интересует? Воспользуйтесь интерактивной клвавиатурой.',
                         reply_markup=keyboard_3())
        bot.register_next_step_handler(message, Calculator)


def Dynamics(message):
    if message.text == 'Динамика Доллара':
        dynamics_dollar(message)
    elif message.text == 'Динамика Евро':
        dynamics_euro(message)
    elif message.text == 'Динамика Биткоина':
        dynamics_bitcoin(message)
    elif message.text == 'Назад':
        f_exit(message)
    else:
        bot.send_message(message.from_user.id, 'Я вас не понимаю. '
                                               'Что вас интересует? Воспользуйтесь интерактивной клвавиатурой.',
                         reply_markup=keyboard_4())
        bot.register_next_step_handler(message, Dynamics)


def dollar(message, parameter):
    url = 'https://www.profinance.ru/currency_usd.asp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.257'}
    content = requests.get(url, headers=headers)
    soup = BeautifulSoup(content.text, 'html.parser')
    convert = soup.find_all('td', {'class': 'cell', 'align': 'center', 'colspan': '2'})
    Dollar = convert[1].next_element.next_element.text
    Dollar = '{:.2f}'.format(float(Dollar))
    bot.send_message(message.from_user.id, f'Курс доллара на данный момент: {Dollar} руб')
    if parameter:
        bot.register_next_step_handler(message, Courses)
    return Dollar


def euro(message, parameter):
    url = 'https://www.profinance.ru/currency_eur.asp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.257'}
    content = requests.get(url, headers=headers)
    soup = BeautifulSoup(content.text, 'html.parser')
    convert = soup.find_all('td', {'class': 'cell', 'align': 'center', 'colspan': '2'})
    Euro = convert[1].next_element.next_element.text
    Euro = '{:.2f}'.format(float(Euro))
    bot.send_message(message.from_user.id, f'Курс евро на данный момент: {Euro} руб')
    if parameter:
        bot.register_next_step_handler(message, Courses)
    return Euro


def bitcoin(message, parameter):
    url = 'https://ru.investing.com/crypto/bitcoin/btc-rub'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.257'}
    content = requests.get(url, headers=headers)
    soup = BeautifulSoup(content.text, 'html.parser')
    convert = soup.find('div', class_='top bold inlineblock').next_element.next_element
    Bitcoin = convert.text.replace('.', ' ')
    bot.send_message(message.from_user.id, f'Курс биткоина на данный момент: {Bitcoin} руб')
    if parameter:
        bot.register_next_step_handler(message, Courses)
    return Bitcoin


def f_exit(message):
    bot.send_message(message.from_user.id, 'Что вас интересует? Воспользуйтесь интерактивной клвавиатурой.',
                     reply_markup=keyboard_1())


def count_dollar(message):
    try:
        col = float(message.text)
        result = col * float(dollar(message, False))
        result_format = '{:.2f}'.format(result)
        result = '{:,}'.format(float(result_format)).replace(',', ' ')

        bot.send_message(message.from_user.id, f'{col} $  - это {result} руб. ')
    except ValueError:
        bot.send_message(message.from_user.id, 'Вы введи не число, введите число, разделяя целую и дробную часть "."')
        bot.register_next_step_handler(message, count_dollar)
    else:
        bot.register_next_step_handler(message, Calculator)


def count_euro(message):
    try:
        col = float(message.text)
        result = col * float(euro(message, False))
        result_format = '{:.2f}'.format(result)
        result = '{:,}'.format(float(result_format)).replace(',', ' ')
        bot.send_message(message.from_user.id, f'{col} €  - это {result} руб. ')
    except ValueError:
        bot.send_message(message.from_user.id, 'Вы введи не число, введите число, разделяя целую и дробную часть "."')
        bot.register_next_step_handler(message, count_euro)
    else:
        bot.register_next_step_handler(message, Calculator)


def count_bitcoin(message):
    try:
        col = float(message.text)
        Bitcoin = bitcoin(message, False).replace(' ', '')
        result = col * float(Bitcoin)
        result_format = '{:.2f}'.format(result)
        result = '{:,}'.format(float(result_format)).replace(',', ' ')
        bot.send_message(message.from_user.id, f'{col} Ƀ  - это {result} руб. ')
    except ValueError:
        bot.send_message(message.from_user.id, 'Вы введи не число, введите число, разделяя целую и дробную часть "."')
        bot.register_next_step_handler(message, count_bitcoin)
    else:
        bot.register_next_step_handler(message, Calculator)


def dynamics_dollar(message):
    bot.send_message(message.from_user.id, 'Ожидайте, запрос выполнется!')
    now = datetime.datetime.now()
    new_data = now.strftime("%d.%m.%Y")
    old_data = now - timedelta(days=30)
    old_data = old_data.strftime("%d.%m.%Y")
    url = 'https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.' \
          'so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.' \
        f'VAL_NM_RQ=R01235&UniDbQuery.From={old_data}&UniDbQuery.To={new_data}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.257'}
    content = requests.get(url, headers=headers)
    page = content.text
    soup = BeautifulSoup(page, 'lxml')
    result = soup.find('div', class_='table-wrapper').find_all('tr')
    data = []
    new_dollar = []
    Dollar = []
    for i in range(0, len(result)):
        if i > 1:
            try:
                data.append(result[i].find_all('td')[0].text)
                Dollar.append(result[i].find_all('td')[2].text)
            except IndexError:
                print('Ошибка')
    for i in Dollar:
        c = i.replace(',', '.')
        new_dollar.append(float(c))
    new_dollar.reverse()
    data.reverse()
    # Строим график
    plt.figure(figsize=(16, 8), dpi=100)
    if new_dollar[len(new_dollar) - 2] > new_dollar[len(new_dollar) - 1]:
        plt.plot(data, new_dollar, color='r', lw=3, ls='-', marker='o', markersize=6)
    else:
        plt.plot(data, new_dollar, color='g', lw=3, ls='-', marker='o', markersize=6)
    plt.title("Динамина доллара за последний месяц")
    plt.grid(which='major', color='k')
    plt.tick_params(labelrotation=45)
    plt.savefig('dollar.png')
    bot.send_photo(message.from_user.id, photo=open("dollar.png", 'rb'))
    bot.register_next_step_handler(message, Dynamics)


def dynamics_euro(message):
    bot.send_message(message.from_user.id, 'Ожидайте, запрос выполнется!')
    now = datetime.datetime.now()
    new_data = now.strftime("%d.%m.%Y")
    old_data = now - timedelta(days=30)
    old_data = old_data.strftime("%d.%m.%Y")
    url = 'https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=' \
          '1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01239&UniDbQuery.' \
          f'From={old_data}&UniDbQuery.To={new_data}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.257'}
    content = requests.get(url, headers=headers)
    page = content.text
    soup = BeautifulSoup(page, 'lxml')
    result = soup.find('div', class_='table-wrapper').find_all('tr')
    data = []
    new_euro = []
    Euro = []
    for i in range(0, len(result)):
        if i > 1:
            try:
                data.append(result[i].find_all('td')[0].text)
                Euro.append(result[i].find_all('td')[2].text)
            except IndexError:
                print('Ошибка')
    for i in Euro:
        c = i.replace(',', '.')
        new_euro.append(float(c))
    new_euro.reverse()
    data.reverse()
    # Строим график
    plt.figure(figsize=(16, 8), dpi=100)
    if new_euro[len(new_euro) - 2] > new_euro[len(new_euro) - 1]:
        plt.plot(data, new_euro, color='r', lw=3, ls='-', marker='o', markersize=6)
    else:
        plt.plot(data, new_euro, color='g', lw=3, ls='-', marker='o', markersize=6)
    plt.title("Динамина евро за последний месяц")
    plt.grid(which='major', color='k')
    plt.tick_params(labelrotation=45)
    plt.savefig('euro.png')
    bot.send_photo(message.from_user.id, photo=open("euro.png", 'rb'))
    bot.register_next_step_handler(message, Dynamics)


def dynamics_bitcoin(message):
    bot.send_message(message.from_user.id, 'Ожидайте, запрос выполнется!')
    url = 'https://creditpower.ru/currency/crypto/btcrur/1month/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.257'}
    content = requests.get(url, headers=headers)
    page = content.text
    soup = BeautifulSoup(page, 'lxml')
    result = soup.find('table', class_='table table-condensed table-hover').find_all('tr')
    data = []
    new_bitcoin = []
    Bitcoin = []
    for i in range(0, len(result)):
        if i > 0:
            try:
                if result[i].find_all('td')[0].text != '':
                    data.append(result[i].find_all('td')[0].text)
                Bitcoin.append(result[i].find_all('td')[1].text)
            except IndexError:
                print('Ошибка')
    for i in Bitcoin:
        new_bitcoin.append(float(i[0] + i[2:5] + i[6:9] + '.' + i[10:12]))
    new_bitcoin.reverse()
    data.reverse()
    # Строим график
    plt.figure(figsize=(16, 8), dpi=100)
    if new_bitcoin[len(new_bitcoin) - 2] > new_bitcoin[len(new_bitcoin) - 1]:
        plt.plot(data, new_bitcoin, color='r', lw=3, ls='-', marker='o', markersize=6)
    else:
        plt.plot(data, new_bitcoin, color='g', lw=3, ls='-', marker='o', markersize=6)
    plt.title("Динамина биткоина за последний месяц")
    plt.grid(which='major', color='k')
    plt.tick_params(labelrotation=45)
    plt.savefig('bitcoin.png')
    bot.send_photo(message.from_user.id, photo=open("bitcoin.png", 'rb'))
    bot.register_next_step_handler(message, Dynamics)


if __name__ == "__main__":
    bot.polling()
