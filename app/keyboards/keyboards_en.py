from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_button_1_eng = KeyboardButton(text='YES')
start_button_2_eng = KeyboardButton(text='NO')

keyboard_yes_no_eng = ReplyKeyboardMarkup(
    keyboard=[[start_button_1_eng, start_button_2_eng]],
    resize_keyboard=True)


start_clava_2_eng = KeyboardButton(text='Select game options')

set_level_button_1 = KeyboardButton(text='SOLO')
set_level_button_2 = KeyboardButton(text='WITH SILLY BOT')
set_level_button_3 = KeyboardButton(text='WITH SMART BOT')
# Создаю клаву после окончания игры
keyboard_game_level_with_NO_en = ReplyKeyboardMarkup(
    keyboard=[[set_level_button_1],
              [set_level_button_2, set_level_button_3],
              [start_button_2_eng]],
    resize_keyboard=True)

keyboard_after_finish_eng = ReplyKeyboardMarkup(
    keyboard=[[start_button_1_eng, start_clava_2_eng],
              [start_button_2_eng]],
    resize_keyboard=True)

schet_button_eng = KeyboardButton(text='VS')

keyboard_after_saying_NO_eng = ReplyKeyboardMarkup(
    keyboard=[[start_button_1_eng], [schet_button_eng]],
    resize_keyboard=True)

start_clava_1_eng = KeyboardButton(text='Start game')
start_clava_3_eng = KeyboardButton(text='No, thanks')

start_clava_eng =  ReplyKeyboardMarkup(
    keyboard=[[start_clava_2_eng],[start_clava_1_eng, start_clava_3_eng]],
    resize_keyboard=True,
    input_field_placeholder='SOLO default')
