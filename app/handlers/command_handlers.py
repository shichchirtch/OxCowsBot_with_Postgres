from aiogram import F
import asyncio
from aiogram.filters import Command, CommandStart
from aiogram import Router
from lexicon import (language_dict, start_greeding, language_kit, kit_game_level,
                     language_responce, sticker_dict)
from aiogram.types import Message, ReplyKeyboardRemove
from loggers import std_out_logger
from keyboards import *
from aiogram.fsm.context import FSMContext
from external_functions import (insert_new_user_in_table,
                                    check_user_in_table,
                                    get_user_language,
                                    reset_user_table_over_bot_pobeda,
                                    reset_versusbot_table_over_bot_pobeda,
                                    change_language,
                                    time_counter,
                                    return_user_wins,
                                    check_user_in_versus_table,
                                    return_bot_wins,
                                    return_total_games,
                                    get_start_time,
                                    cancel_reset_user_table,
                                    cancel_reset_versusbot_table)
from external_functions.solo_functions import secret_kit_is_0000
from states import FSM_IN_GAME, ingame_states
from filters import START_ONCE_ONLY

# Инициализируем роутер уровня модуля
command_router = Router()
yes_no_kb = (keyboard_yes_no, keyboard_yes_no_eng, keyboard_yes_no_de)

@command_router.message(START_ONCE_ONLY(), ~CommandStart())
async def before_start(message:Message):
    print("We are in PRE START Handler")
    await message.reply(text='Нажми на кнопку <b>start</b> !',
                         reply_markup=pre_start_clava)

@command_router.message(CommandStart(), START_ONCE_ONLY())
async def start_command(message: Message, state: FSMContext):
    print(f'user {message.chat.first_name} press start')
    user_name = message.chat.first_name
    user_tg_id = message.from_user.id
    await insert_new_user_in_table(user_tg_id, user_name)
    await state.set_state(FSM_IN_GAME.not_in_game)
    await message.answer(
        f'Привет, <b>{message.chat.first_name}</b> !  \U0001F60A\n {start_greeding}',
                    reply_markup=start_clava)
    print("Process finfshed")

@command_router.message(F.text.lower().in_(language_kit))
async def set_language(message: Message):
    print('смена языка')
    user_tg_id = message.from_user.id
    lang = message.text.lower()
    await change_language(user_tg_id, lang)
    language = await get_user_language(user_tg_id)
    await message.answer(text=language_responce[language],
                         reply_markup=ReplyKeyboardRemove())


@command_router.message(F.text.in_(kit_game_level))
async def set_game_level(message: Message, state: FSMContext):
    print("\n SET WORKS")
    user_tg_id = message.from_user.id
    status = await state.get_state()
    language = await get_user_language(user_tg_id)
    if status not in ingame_states:
        await state.set_state(FSM_IN_GAME.choose_level)
        await message.answer(text=f"{language_dict['set game level'][language]}",
                             reply_markup=keyboard_game_level)
    else:
        answer = await state.get_state()
        level = answer.split(':')[1]
        await message.answer(f'{level.upper()}  {language_dict["game level is"][level][language]}')

@command_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    print("HELP START WORKS")
    user_tg_id = message.from_user.id
    user_name = message.from_user.first_name
    language = await get_user_language(user_tg_id)

    if await secret_kit_is_0000(user_tg_id):
        await message.answer(text=language_dict['game rules'][language] + \
                             user_name + language_dict['start ?'][language],
                             reply_markup=help_clava)
    else:
        await message.answer(text=language_dict['game rules'][language],
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(text=language_dict['in game querry'][language],
                             reply_markup=ReplyKeyboardRemove())


start_clava_set = (start_clava, start_clava_eng, start_clava_de)
@command_router.message(F.text.in_(['Нет, спасибо\nЯ просто посмотреть зашел', '/cancel', 'cancel']))
async def process_cancel_command(message: Message, state:FSMContext):
    user_tg_id = message.from_user.id
    user_name = message.from_user.first_name
    language = await get_user_language(user_tg_id)
    status = await state.get_state()
    std_out_logger.info(f"ЮЗЕР  {user_name} нажал команду /cancel ")
    if status in ingame_states:
        await cancel_reset_user_table(user_tg_id)
        if status in ingame_states[1:]:
            await cancel_reset_versusbot_table(user_tg_id)
        await state.set_state(FSM_IN_GAME.not_in_game)
        await message.answer(
            language_dict['exit from game'][language])
        await message.answer_sticker(sticker_dict['process_cancel_command'],
                                     reply_markup=start_clava_set[language])
    else:
        await message.answer(text=language_dict['user not in game now'][language],
                             reply_markup=yes_no_kb[language])


@command_router.message(F.text.in_(['/schet','Узнать Счёт', 'VS']))
async def uznatb_schet(message: Message, state:FSMContext):
    std_out_logger.info('schet works')
    user_tg_id = message.from_user.id
    user_name = message.from_user.first_name
    language = await get_user_language(user_tg_id)
    status = await state.get_state()
    in_versus_table = await check_user_in_versus_table(user_tg_id)
    if not in_versus_table:
        bot_pobeda = 0
    else:
        bot_pobeda = await return_bot_wins(user_tg_id)

    user_start_time = await get_start_time(user_tg_id)
    time_data = await time_counter(user_start_time)

    await message.answer(f"<b><i>{user_name} : {await return_user_wins(user_tg_id)}</i></b>\n"
                         f'<b><i>BOT : {bot_pobeda}</i></b>\n'
                         f'<b><i>Total Game : {await return_total_games(user_tg_id)}</i></b>\n'
                         f'{time_data}')
    await asyncio.sleep(1)
    if status not in ingame_states:
        await message.answer(text=language_dict['had a look at scores ?'][language],
                              reply_markup=start_clava)
    else:
        await message.answer(
            text=language_dict['in game querry'][language],
            reply_markup=ReplyKeyboardRemove())


