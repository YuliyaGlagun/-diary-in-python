import requests
import json
import os

city = 'Ефремов'

url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

w_data = requests.get(url).json()

weather_data_structure = json.dumps(w_data, indent=2)

# получаем данные о температуре и о том, как она ощущается
temperature = round(w_data['main']['temp'])
temperature_feels = round(w_data['main']['feels_like'])

print('Сейчас в городе', city, str(temperature), '°C')
print('Ощущается как', str(temperature_feels), '°C')

import pandas as pd
from datetime import datetime
from datetime import date

# СОЗДАТЬ ПУСТОЙ ДАТАФРЕЙМ (ПРИ ЗАПУСКЕ ПРОГРАММЫ В ПЕРВЫЙ РАЗ) И ЗАПИСАТЬ В ФАЙЛ
if not os.path.isfile('todolist2.csv'):  # ЕСЛИ ФАЙЛ НЕ СУЩЕСТВУЕТ
    data = pd.DataFrame(columns=['date', 'task', 'status'])
    data.to_csv('todolist2.csv', index=False)

data = pd.read_csv('/data/notebook_files/todolist2.csv')
today = date.today()
print("Сегодня:", today)

# date К ФОРМАТУ ДАТЫ
data['date'] = pd.to_datetime(data['date']).dt.date


def show_tasks(data):
    data = data.reset_index()
    print(data)


def show_task_date(data, date):
    data = data[data['date'] == date]
    print(data)


def add_task(data, date, task):
    new_task = pd.DataFrame({'date': [date], 'task': [task], 'status': [False]})
    data = pd.concat([data, new_task], ignore_index=True)
    return data


def delete_task(data, index):
    data = data.drop(index=index)
    print('Дело под номером', index, 'удалено.')
    print(data)
    return data


def update_status(data, index):
    data.at[index, 'status'] = True
    return data


def completed_cases(data):
    print(date['status'] == True)


def depending_on_the_weather(data):
    if temperature_feels <= 10:
        data = add_task(data, today, 'Приготовить горячий напиток')
        print('Надень пальто и шарф.')
    if temperature_feels >= 11 and temperature_feels <= 18:
        data = add_task(data, today, 'Погулять')
        print('Надевай куртку. Идеальная температура для прогулки')
    if temperature_feels >= 18:
        data = add_task(data, today, 'Завтрак на веранде')
        print('Сегодня отличная погода.')
    return data


while True:
    print('''
    ДОСТУПНЫЕ КОМАНДЫ:
    1 - показать весь список
    2 - добавить новое дело
    3 - удалить дело
    4 - изменить статус на Тrue
    5 - показать все дела на день
    6 - показать все выполненые дела
    7 - добавить дело в зависимости от погоды
    0 - выход из программы
    ''')
    show = int(input('Введите команду: '))
    if show == 1:
        show_tasks(data)

    if show == 2:
        date = input('Введите дату в формате ГГГГ-ММ-ДД: ')
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except Exception as error:
            print('Ошибка в формате даты:', error)
            date = input('Введите дату в формате ГГГГ-ММ-ДД: ')
        task = input('Введите дело: ')
        data = add_task(data, date, task)

    if show == 3:
        index = int(input('Введите номер дела: '))
        data = delete_task(data, index)
        show_tasks(data)
    if show == 4:
        index = int(input('Введите номер дела: '))
        data = update_status(data, index)
        show_tasks(data)
    if show == 5:
        date = input('Введите дату в формате ГГГГ-ММ-ДД: ')
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            show_task_date(data, date)
        except Exception as error:
            print('Ошибка в формате даты:', error)
            date = input('Введите дату в формате ГГГГ-ММ-ДД: ')

    if show == 6:
        completed_cases(data)
    if show == 7:
        data = depending_on_the_weather(data)
    if show == 0:
        data.to_csv('todolist2.csv', index=False)  # index=False
        break
print('Программа завершена!')

