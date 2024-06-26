from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,)

#Создаю кнопки
start_button_1 = KeyboardButton(text='ДА')
start_button_2 = KeyboardButton(text='НЕТ')
set_button = KeyboardButton(text='Выбрать уровень игры')
schet_button = KeyboardButton(text='Узнать Счёт')

start_clava_1 = KeyboardButton(text='Начать игру')
start_clava_2 = KeyboardButton(text='Выбрать уровень игры')
start_clava_3 = KeyboardButton(text='Нет, спасибо\nЯ просто посмотреть зашел')

start_clava =  ReplyKeyboardMarkup(
    keyboard=[[start_clava_2],[start_clava_1, start_clava_3]],
    resize_keyboard=True,
    input_field_placeholder='SOLO default')

#  Создаю клавиатуру на согласие играть
keyboard_yes_no = ReplyKeyboardMarkup(
    keyboard=[[start_button_1, start_button_2]],
    resize_keyboard=True)

set_level_button_1 = KeyboardButton(text='SOLO')
set_level_button_2 = KeyboardButton(text='WITH SILLY BOT')
set_level_button_3 = KeyboardButton(text='WITH SMART BOT')

#  Создаю клавиатуру для выбора уровня
keyboard_game_level = ReplyKeyboardMarkup(
    keyboard=[[set_level_button_1],
              [set_level_button_2, set_level_button_3]],
    resize_keyboard=True)
# Создаю клаву после окончания игры
keyboard_game_level_with_NO_rus = ReplyKeyboardMarkup(
    keyboard=[[set_level_button_1],
              [set_level_button_2, set_level_button_3],
              [start_button_2]],
    resize_keyboard=True)

keyboard_after_saying_NO = ReplyKeyboardMarkup(
    keyboard=[[start_button_1], [schet_button]],
    resize_keyboard=True)

keyboard_after_finish = ReplyKeyboardMarkup(
    keyboard=[[start_button_1, start_clava_2 ],
              [start_button_2]],
    resize_keyboard=True)

pre_start_button = KeyboardButton(text='/start')

pre_start_clava = ReplyKeyboardMarkup(
    keyboard=[[pre_start_button]],
    resize_keyboard=True,
    input_field_placeholder='Жми на кнопку !'
)

help_clava = ReplyKeyboardMarkup(
    keyboard=[[start_button_1, set_button],[start_button_2]],
    resize_keyboard=True)

button_emoji = '*  *  *  \U0001f680  *  *  *'
usual_button = KeyboardButton(text=button_emoji)
usual_clava = ReplyKeyboardMarkup(
        keyboard=[[usual_button]],
        resize_keyboard=True,
        input_field_placeholder='Жми на кнопку !')