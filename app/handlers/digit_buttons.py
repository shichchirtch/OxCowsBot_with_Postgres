from aiogram.types import CallbackQuery
from lexicon import language_dict
from aiogram import Router, F
from external_functions.digit_functions import (check_len_inline_combo,
                                                    format_string,
                                                    return_data_from_inline_user_kit,
                                                    insert_digit_combo_in_inline_user_kit,
                                                    reset_inline_user_kit)
from external_functions.external_functions import get_user_language
from filters.digit_filters import VERIFY_LEN_INLINE_COMBO
from random import choice
from aiogram.filters import StateFilter
from states import FSM_IN_GAME

digit_router = Router()

@digit_router.callback_query(F.data == '1_pressed', VERIFY_LEN_INLINE_COMBO(),
                             StateFilter(FSM_IN_GAME.with_smart_bot,
                                         FSM_IN_GAME.with_silly_bot,
                                         FSM_IN_GAME.solo))
async def button_1_press(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    language = await get_user_language(user_tg_id)
    sett = await return_data_from_inline_user_kit(user_tg_id)
    print('sett = ', sett)
    new_set = sett + '1'
    pattern = await format_string(new_set)
    print('pattern = ', pattern)
    enter = language_dict["you enter"][language]
    if await check_len_inline_combo(new_set):
        print('*** here')
        await insert_digit_combo_in_inline_user_kit(user_tg_id, new_set)
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=None)
    await callback.answer()

@digit_router.callback_query(F.data == '2_pressed', VERIFY_LEN_INLINE_COMBO(),
                             StateFilter(FSM_IN_GAME.with_smart_bot,
                                         FSM_IN_GAME.with_silly_bot,
                                         FSM_IN_GAME.solo))
async def button_2_press(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    language = await get_user_language(user_tg_id)
    sett = await return_data_from_inline_user_kit(user_tg_id)
    new_set = sett + '2'
    pattern = await format_string(new_set)
    enter = language_dict["you enter"][language]
    if await check_len_inline_combo(new_set):
        await insert_digit_combo_in_inline_user_kit(user_tg_id, new_set)
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=None)
    await callback.answer()

@digit_router.callback_query(F.data == '3_pressed', VERIFY_LEN_INLINE_COMBO(),
                             StateFilter(FSM_IN_GAME.with_smart_bot,
                                         FSM_IN_GAME.with_silly_bot,
                                         FSM_IN_GAME.solo))
async def button_3_press(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    language = await get_user_language(user_tg_id)
    sett = await return_data_from_inline_user_kit(user_tg_id)
    new_set = sett + '3'
    pattern = await format_string(new_set)
    enter = language_dict["you enter"][language]
    if await check_len_inline_combo(new_set):
        await insert_digit_combo_in_inline_user_kit(user_tg_id, new_set)
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=None)
    await callback.answer()


@digit_router.callback_query(F.data == '4_pressed', VERIFY_LEN_INLINE_COMBO(),
                             StateFilter(FSM_IN_GAME.with_smart_bot,
                                         FSM_IN_GAME.with_silly_bot,
                                         FSM_IN_GAME.solo))
async def button_4_press(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    language = await get_user_language(user_tg_id)
    sett = await return_data_from_inline_user_kit(user_tg_id)
    new_set = sett + '4'
    pattern = await format_string(new_set)
    enter = language_dict["you enter"][language]
    if await check_len_inline_combo(new_set):
        await insert_digit_combo_in_inline_user_kit(user_tg_id, new_set)
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=None)
    await callback.answer()

@digit_router.callback_query(F.data == '5_pressed', VERIFY_LEN_INLINE_COMBO(),
                             StateFilter(FSM_IN_GAME.with_smart_bot,
                                         FSM_IN_GAME.with_silly_bot,
                                         FSM_IN_GAME.solo))
async def button_5_press(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    language = await get_user_language(user_tg_id)
    sett = await return_data_from_inline_user_kit(user_tg_id)
    new_set = sett + '5'
    pattern = await format_string(new_set)
    enter = language_dict["you enter"][language]
    if await check_len_inline_combo(new_set):
        await insert_digit_combo_in_inline_user_kit(user_tg_id, new_set)
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=None)
    await callback.answer()


@digit_router.callback_query(F.data == '6_pressed', VERIFY_LEN_INLINE_COMBO(),
                             StateFilter(FSM_IN_GAME.with_smart_bot,
                                         FSM_IN_GAME.with_silly_bot,
                                         FSM_IN_GAME.solo))
async def button_6_press(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    language = await get_user_language(user_tg_id)
    sett = await return_data_from_inline_user_kit(user_tg_id)
    new_set = sett+ '6'
    pattern = await format_string(new_set)
    enter = language_dict["you enter"][language]
    if await check_len_inline_combo(new_set):
        await insert_digit_combo_in_inline_user_kit(user_tg_id, new_set)
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=None)
    await callback.answer()

@digit_router.callback_query(F.data == '7_pressed', VERIFY_LEN_INLINE_COMBO(),
                             StateFilter(FSM_IN_GAME.with_smart_bot,
                                         FSM_IN_GAME.with_silly_bot,
                                         FSM_IN_GAME.solo))
async def button_7_press(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    language = await get_user_language(user_tg_id)
    sett = await return_data_from_inline_user_kit(user_tg_id)
    new_set = sett + '7'
    pattern = await format_string(new_set)
    enter = language_dict["you enter"][language]
    if await check_len_inline_combo(new_set):
        await insert_digit_combo_in_inline_user_kit(user_tg_id, new_set)
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=None)
    await callback.answer()


@digit_router.callback_query(F.data == '8_pressed', VERIFY_LEN_INLINE_COMBO(),
                             StateFilter(FSM_IN_GAME.with_smart_bot,
                                         FSM_IN_GAME.with_silly_bot,
                                         FSM_IN_GAME.solo))
async def button_8_press(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    language = await get_user_language(user_tg_id)
    sett = await return_data_from_inline_user_kit(user_tg_id)
    new_set = sett+ '8'
    pattern = await format_string(new_set)
    enter = language_dict["you enter"][language]
    if await check_len_inline_combo(new_set):
        await insert_digit_combo_in_inline_user_kit(user_tg_id, new_set)
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=None)
    await callback.answer()

@digit_router.callback_query(F.data == '9_pressed', VERIFY_LEN_INLINE_COMBO(),
                             StateFilter(FSM_IN_GAME.with_smart_bot,
                                         FSM_IN_GAME.with_silly_bot,
                                         FSM_IN_GAME.solo))
async def button_9_press(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    language = await get_user_language(user_tg_id)
    sett = await return_data_from_inline_user_kit(user_tg_id)
    new_set = sett + '9'
    pattern = await format_string(new_set)
    enter = language_dict["you enter"][language]
    if await check_len_inline_combo(new_set):
        await insert_digit_combo_in_inline_user_kit(user_tg_id, new_set)
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=None)
    await callback.answer()

@digit_router.callback_query(F.data == '0_pressed', VERIFY_LEN_INLINE_COMBO(),
                             StateFilter(FSM_IN_GAME.with_smart_bot,
                                         FSM_IN_GAME.with_silly_bot,
                                         FSM_IN_GAME.solo))
async def button_0_press(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    language = await get_user_language(user_tg_id)
    sett = await return_data_from_inline_user_kit(user_tg_id)
    new_set = sett + '0'

    pattern = await format_string(new_set)
    enter = language_dict["you enter"][language]
    if await check_len_inline_combo(new_set):
        await insert_digit_combo_in_inline_user_kit(user_tg_id, new_set)
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(
            text='\U0001f928' + ' ' * 19 + f'{enter}  <b>{pattern}</b>' + ' ' * 19 + '\u27A1\uFE0F',
            reply_markup=None)
    await callback.answer()


@digit_router.callback_query(F.data == 'del_pressed')
async def button_del_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    language = await get_user_language(user_id)
    len_combo = await return_data_from_inline_user_kit(user_id)
    if len(len_combo)>1:
        cut_combo = len_combo[:-1]
        await insert_digit_combo_in_inline_user_kit(user_id, cut_combo)
        enter = language_dict['inline combo'][language]
        pattern = await format_string(cut_combo)
        await callback.message.edit_text(
            text=f"\u27A1\uFE0F           {enter}   {pattern}      \U0001f535",
            reply_markup=callback.message.reply_markup)
    elif len(len_combo) == 1:
        cut_combo = ''
        await insert_digit_combo_in_inline_user_kit(user_id, cut_combo)
        enter = language_dict['inline again'][language]
        await callback.message.edit_text(
            text=f"\u27A1\uFE0F         {enter}       \U0001f535",
            reply_markup=callback.message.reply_markup)
    elif len(len_combo)==0:
        enter = language_dict['nothing'][language]
        await callback.message.edit_text(
            text=f'\u21AA\uFE0F                   {enter}            \U0001f937\u200D\u2642\uFE0F',
            reply_markup=callback.message.reply_markup)
    await callback.answer('*****')



@digit_router.callback_query(F.data == 'clear_pressed')
async def button_clear_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    language = await get_user_language(user_id)
    len_combo = await return_data_from_inline_user_kit(user_id)
    await callback.answer('clear')
    if len(len_combo) > 0:

        await reset_inline_user_kit(user_id)
        await callback.message.edit_text(
            text=f"{language_dict['not repeat'][language]}",
            reply_markup=callback.message.reply_markup)
    else:
        enter = language_dict['nothing'][language]
        await callback.message.edit_text(
            text=f'\u21AA\uFE0F                  {enter}            \U0001f937\u200D\u2642\uFE0F',
            reply_markup=callback.message.reply_markup)
    await callback.answer('*****')


emo_tuple = ('\U0001f951', '\U0001f346', '\U0001f954', '\U0001f33d', '\U0001f336\uFE0F', '\U0001fad1', '\U0001f952',
             '\U0001f96c', '\U0001f966', '\U0001f9c4', '\U0001f9c5', '\U0001f95c', '\U0001fad8', '\U0001f330',
             '\U0001fada', '\U0001fadb')

@digit_router.callback_query(F.data == 'send_pressed')
async def button_send(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(emo_tuple),
        reply_markup=None)