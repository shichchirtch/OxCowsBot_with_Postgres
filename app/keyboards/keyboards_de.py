from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


start_button_1_de = KeyboardButton(text='Ja')
start_button_2_de = KeyboardButton(text='Nein')

keyboard_yes_no_de = ReplyKeyboardMarkup(
    keyboard=[[start_button_1_de, start_button_2_de]],
    resize_keyboard=True)
set_level_button_1 = KeyboardButton(text='SOLO')
set_level_button_2 = KeyboardButton(text='WITH SILLY BOT')
set_level_button_3 = KeyboardButton(text='WITH SMART BOT')
# Создаю клаву после окончания игры
keyboard_game_level_with_NO_de = ReplyKeyboardMarkup(
    keyboard=[[set_level_button_1],
              [set_level_button_2, set_level_button_3],
              [start_button_2_de]],
    resize_keyboard=True)

start_clava_2_de = KeyboardButton(text='Wählen Sie Spieloptionen')

keyboard_after_finish_de = ReplyKeyboardMarkup(
    keyboard=[[start_button_1_de, start_clava_2_de],
              [start_button_2_de]],
    resize_keyboard=True)

schet_button_de = KeyboardButton(text='VS')

keyboard_after_saying_NO_de = ReplyKeyboardMarkup(
    keyboard=[[start_button_1_de], [schet_button_de]],
    resize_keyboard=True)

start_clava_1_de = KeyboardButton(text='Start Spielen')
start_clava_3_de = KeyboardButton(text='Nein, danke')

start_clava_de =  ReplyKeyboardMarkup(
    keyboard=[[start_clava_2_de],[start_clava_1_de, start_clava_3_de]],
    resize_keyboard=True,
    input_field_placeholder='SOLO Standard')
