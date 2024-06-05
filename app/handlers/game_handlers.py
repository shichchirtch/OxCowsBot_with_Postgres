from aiogram import Router, F, html
import asyncio
from filters import (DATA_IS_DIGIT,
                     DATA_IS_NOT_DIGIT,
                     BOT_COMBO,
                     NOT_USER_COMBO,
                     INLINE_FILTER)
from bot_base import tallys_str_bot, four_bools
from loggers import std_out_logger, std_err_logger
from lexicon import *
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from external_functions.external_functions import (get_user_language,
                                                   insert_bot_comboline_in_bot_list_without_first_combo,
                                                   insert_secret_kit,
                                                   insert_in_versus_table,
                                                   check_secret_kit,
                                                   insert_user_combo_in_versus_table,
                                                   get_bot_first_attempt,
                                                   insert_first_bot_combo_in_versus_table,
                                                   seek_bools,
                                                   append_kit,
                                                   verify_when_two_cows,
                                                   verify_bools_position,
                                                   insert_bot_comboline_in_bot_list,
                                                   return_bot_list,
                                                   return_user_combo_for_bot,
                                                   format_bot_response,
                                                   reset_versusbot_table_over_bot_pobeda,
                                                   reset_user_table_over_bot_pobeda,
                                                   get_start_time,
                                                   insert_time_again
                                                   )
from external_functions.digit_functions import (return_data_from_inline_user_kit,
                                                reset_inline_user_kit)
from external_functions.solo_functions import (check_game_list,
                                               user_attempt_guess_secret_combo,
                                               return_secret_kit,
                                               format_f_string,
                                               return_schritt_quantity,
                                               reset_user_data_after_finish,
                                               return_game_list,
                                               secret_kit_is_0000)
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states import FSM_IN_GAME, ingame_states
from keyboards import *

game_router = Router()

digit_keyboards_tuple = (keyboard_digits_Rus, keyboard_digits, keyboard_digits_De)
lang_set = (keyboard_after_saying_NO, keyboard_after_saying_NO_eng, keyboard_after_saying_NO_de)
yes_no_kb = (keyboard_yes_no, keyboard_yes_no_eng, keyboard_yes_no_de)
keyafter_finish = (keyboard_after_finish, keyboard_after_finish_eng, keyboard_after_finish_de)
k_after_fin_with_NO = (keyboard_game_level_with_NO_rus, keyboard_game_level_with_NO_en,
                       keyboard_game_level_with_NO_de)


@game_router.message(F.content_type != ContentType.TEXT)
async def process_notTEXT_answers(message: Message, state: FSMContext):
    print('Wrong content type')
    user_tg_id = message.from_user.id
    user_name = message.from_user.first_name
    status = await state.get_state()
    language = await get_user_language(user_tg_id)
    if status in ingame_states:
        await message.answer(language_dict['wrong sent data'][language])
    else:
        await message.answer(text=f"<b>{user_name}</b>{language_dict['wrong content type'][language]}",
                             reply_markup=keyboard_yes_no)


@game_router.message(StateFilter(FSM_IN_GAME.choose_level), ~F.text.lower().in_(negative_answer))
async def update_user_game_level(message: Message, state: FSMContext):  # Здесь юзер устанавливает уровень игры
    user_tg_id = message.from_user.id
    language = await get_user_language(user_tg_id)
    if message.text == "SOLO":
        await state.set_state(FSM_IN_GAME.solo)
        await message.answer(text=f"{language_dict['choosing level is'][language]}"
                                  f"<b>SOLO</b>   \n"
                                  f"{language_dict['game start ?'][language]}",
                             reply_markup=yes_no_kb[language])
    elif message.text == "WITH SILLY BOT":
        await state.set_state(FSM_IN_GAME.with_silly_bot)
        await message.answer(text=f"{language_dict['choosing level is'][language]}"
                                  f"<b>WITH SILLY BOT</b>   \n"
                                  f"{language_dict['game start ?'][language]}",
                             reply_markup=yes_no_kb[language])
    elif message.text == "WITH SMART BOT":
        await state.set_state(FSM_IN_GAME.with_smart_bot)
        await message.answer(text=f"{language_dict['choosing level is'][language]}"
                                  f"<b>WITH SMART BOT</b>   \n"
                                  f"{language_dict['game start ?'][language]}",
                             reply_markup=yes_no_kb[language])
    else:
        await state.set_state(FSM_IN_GAME.solo)
        await message.answer(text=f"{language_dict['choosing level is'][language]}"
                                  f"<b>SOLO - DEFAULT</b>   \n"
                                  f"{language_dict['game start ?'][language]}",
                             reply_markup=yes_no_kb[language])
    print("UPDATE FINISHED")


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@game_router.message(DATA_IS_NOT_DIGIT(), BOT_COMBO(), F.text.lower().in_(positiv_answer))
async def process_positive_answer(message: Message, state: FSMContext):
    await message.answer_sticker(sticker_dict['rocket bull'],
                                 reply_markup=usual_clava)
    user_tg_id = message.from_user.id
    us_name = message.from_user.first_name
    language = await get_user_language(user_tg_id)
    status = await state.get_state()
    await insert_secret_kit(user_tg_id)  # Записываем секретную комбинацию для юзера
    std_out_logger.info('insert have done')

    us_time = await get_start_time(user_tg_id)
    if not us_time:  # Если юзер нажимал cancel, то его время равно 0
        await insert_time_again(user_tg_id)
    if status not in ingame_states:
        await state.set_state(FSM_IN_GAME.solo)
        status = await state.get_state()
    if status == ingame_states[0]:
        print("\nSOLO states in positive answer ")
        await message.answer(language_dict['solo_bot_guessed'][language],
                             reply_markup=digit_keyboards_tuple[language])
    else:
        await insert_in_versus_table(user_tg_id, us_name)
        await message.answer(language_dict['bot_ask_user_combo'][language],
                             reply_markup=usual_clava)


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@game_router.message(F.text.lower().in_(negative_answer))
async def process_negative_answer(message: Message, state: FSMContext):
    print("NEGATIVE WORKS")
    user_tg_id = message.from_user.id
    language = await get_user_language(user_tg_id)
    if await secret_kit_is_0000(user_tg_id):
        await message.answer(text=language_dict['pity'][language],
                             reply_markup=ReplyKeyboardRemove())
        await message.answer_sticker(sticker_dict['negative answer'],
                                     reply_markup=lang_set[language])
        await state.set_state(
            FSM_IN_GAME.not_in_game)  # Эта натсройка не позволит продолжить игру просто вводом комбинаций
    else:
        std_out_logger.info(f'\nЮзер {user_tg_id} ответил нет !')
        await message.answer(language_dict['wrong sent data'][language])


@game_router.message(DATA_IS_DIGIT(), StateFilter(FSM_IN_GAME.with_smart_bot, FSM_IN_GAME.with_silly_bot),
                     NOT_USER_COMBO(), INLINE_FILTER())
async def set_user_combo(message: Message, state: FSMContext):
    """Этот хэндлер срабатывает, только тогда, когда бот   Т О Ж Е     будет отгадывать комбо юзера
        Этот хэндлер должен срабатывать только один раз за игру с ботом !"""
    user_tg_id = message.from_user.id
    language = await get_user_language(user_tg_id)
    status = await state.get_state()
    print('SET_US_COMBO_HANDLER works')
    if await check_secret_kit(user_tg_id):
        await insert_secret_kit(user_tg_id)
        await message.answer(language_dict['bot_ask_user_combo'][language],
                             reply_markup=usual_clava)

    us_combo = list(message.text)
    await insert_user_combo_in_versus_table(user_tg_id, us_combo)
    print('insert_user_combo_in_versus_table done')
    await message.answer(text=language_dict['after_user_zagadal_combo'][language],
                         reply_markup=digit_keyboards_tuple[language])

    #  Что мы имеем на старте
    start_kit = us_combo  # Уже введена и отловлена хэндлером ! ! !

    first_bot_data = await get_bot_first_attempt(
        tallys_str_bot)  # Так бот получает комбинацию, с которой начинает угадывать комбо юзера

    await insert_first_bot_combo_in_versus_table(user_tg_id, first_bot_data)  # Аппендим первую попытку

    std_out_logger.info(
        f'\n ********  FIRST BOT attempt {first_bot_data}  for  {user_tg_id}  ********')

    rest_bot_chisla_arr = list(set(tallys_str_bot).symmetric_difference(set(first_bot_data)))  # Это набор оставшихся
    # неиспользованными при построении первой комбинации ботом чисел

    temp_game_arr = await seek_bools(start_kit, first_bot_data)

    final_res = [[first_bot_data]]
    if not temp_game_arr:  # То есть  ни коров ни быков не попало к боту
        std_err_logger.info('NOT temp_game_arr works')  # Раскомментируовать логгер, при необходимости !
        bot_data = rest_bot_chisla_arr[:4]  # Новый набор для бота
        final_res = await append_kit(bot_data,
                                     final_res)  # Ну и аппендим сразу вторую попытку бота угадать в список комбинаций
        first_bot_data = bot_data
        temp_game_arr = await seek_bools(start_kit, bot_data)

    ########################################################  len(temp_game_arr) == 1 ########################################
    if len(temp_game_arr) == 1:  # Только одна корова или бык
        std_err_logger.info('temp_game_arr 1 works')  # Раскомментируовать логгер, при необходимости !

        bot_data = rest_bot_chisla_arr[:4]  # Здесь мы перезаписываем значение bot_data на 4 из 6 оставшихся в наборе
        final_res.append(bot_data)  # Ну и аппендим сразу это в список комбинаций
        e, f = rest_bot_chisla_arr[4], rest_bot_chisla_arr[5]
        temp_game_arr = await seek_bools(start_kit, bot_data)
        first_bot_data = bot_data
        if len(temp_game_arr) == 1:
            new_bot_data = [bot_data[0], bot_data[1], e, f]
            first_bot_data = new_bot_data
            temp_game_arr = await seek_bools(start_kit, new_bot_data)

    if len(temp_game_arr) == 2:
        std_err_logger.info('temp_game_arr 2 works')  # Раскомментируовать логгер, при необходимости !
        temp_arr = await verify_when_two_cows(first_bot_data, start_kit)
        final_res = await append_kit(temp_arr, final_res)  # Ну и аппендим сразу это в список комбинаций
        # Дальше Вызовем функцию расставления коров по местам
        final_res = await verify_bools_position(temp_arr, start_kit, final_res)

    if len(temp_game_arr) == 3:
        # std_err_logger.info('temp_game_arr 3 works, first bot data = ', first_bot_data)  # Раскомментируовать логгер, при необходимости !
        # Находим последнюю корову в остаtке набора цифр
        last_tally = set(start_kit).difference(set(first_bot_data)).pop()
        right_num = list(set(start_kit).intersection(set(first_bot_data)))
        verifying_arr = right_num + [last_tally]

        final_res = await append_kit(verifying_arr, final_res)  # Ну и аппендим сразу это в список комбинаций
        # Дальше Вызовем функцию расставления коров по местам
        final_res = await verify_bools_position(verifying_arr, start_kit, final_res)

    if len(temp_game_arr) == 4:
        # std_err_logger.info('temp_game_arr 4 works')  # Раскомментируовать логгер, при необходимости !
        final_res = await verify_bools_position(first_bot_data, start_kit, final_res)

    del final_res[0]  # удаляю первый эдемент, потому что он уже есть в таблицы VersusBot
    final_res = final_res[::-1]  # Делаю реверс списка, чтобы можно было удалять элементы с конца методом рор()

    if status == ingame_states[2]:
        if len(final_res) > 8:
            final_res = final_res[:-1:2]
            final_res = final_res[:7]
            await insert_bot_comboline_in_bot_list(user_tg_id, final_res)
        else:
            await insert_bot_comboline_in_bot_list(user_tg_id, final_res)
    else:
        final_res = final_res[:-1]
        await insert_bot_comboline_in_bot_list(user_tg_id, final_res)

    std_err_logger.info(f'Список Бота - {final_res}')


@game_router.message(DATA_IS_DIGIT(),
                     StateFilter(FSM_IN_GAME.with_smart_bot, FSM_IN_GAME.with_silly_bot))
async def gaming_with_bot(message: Message, state: FSMContext):
    """Сюда попадают комбинации, которые вводит юзер"""
    print('game handler works !'.upper())
    user_tg_id = message.from_user.id
    language = await get_user_language(user_tg_id)
    user_combo_for_bot = await return_user_combo_for_bot(user_tg_id)
    # bot_list = await return_bot_list(user_tg_id)
    secret_kit = await return_secret_kit(user_tg_id)
    schritt = await  return_schritt_quantity(user_tg_id)
    if message.text == button_emoji:
        _inline_entered_user_kit = await return_data_from_inline_user_kit(user_tg_id)
        user_combo = list(_inline_entered_user_kit)  # Если Юзер ввел комбинацию инлайн клавиатурой
    else:
        user_combo = list(message.text)  # Если юзер ввел комбо обычной клавой

    if await check_game_list(user_tg_id, user_combo):  # Если такой комбинации юзер ещё не вводил
        final_res = await return_bot_list(user_tg_id)  # Получаю в распоряжение спискок комбинаций бота
        processing_combo = final_res.pop()  # Последний элемент из списка алгоритма бота
        await insert_bot_comboline_in_bot_list_without_first_combo(user_tg_id, final_res)
        temp_game_arr = await seek_bools(user_combo_for_bot,
                                         processing_combo)  # Получаю подобную структуру ['Ox', 'Cow'], для бота
        #  Тут получает сначала подается str,  потом list
        std_err_logger.info(
            f'for {user_tg_id}   AttemtCOMBO  =  {user_combo} , '
            f'список комбининаций бота : att = {len(final_res)},  '
            f'{final_res}')

        if temp_game_arr != four_bools:  # Бот не отгадал этой комбинацией
            # USER PART
            await user_attempt_guess_secret_combo(user_tg_id,
                                                  user_combo)  # Делаем необходимые преoбразования с записью в БД юзера

            temp_res = await seek_bools(secret_kit, user_combo)  # Переводим tem_res в состояние ["Ox", "Cow" ]

            if temp_res != four_bools:  # Юзер не отгадал этой комбинацией
                if message.text == button_emoji:
                    current_data = " ".join(user_combo)
                    stroka = await format_f_string(current_data, temp_res, language, schritt)
                    await message.reply(stroka, reply_markup=usual_clava)
                else:
                    current_data = " ".join(temp_res)
                    stroka = await format_f_string(current_data, temp_res, language, schritt)  # 'setting_data'
                    await message.answer(stroka, reply_markup=usual_clava)
                await asyncio.sleep(1)

                bot_test_combo = ' '.join(processing_combo)
                stroka_bot_attempt_combo = await format_bot_response(bot_test_combo, temp_game_arr, language)

                await message.answer(stroka_bot_attempt_combo)
                await asyncio.sleep(1)
                await message.answer(language_dict["next combo do"][language],
                                     reply_markup=digit_keyboards_tuple[language])

                await reset_inline_user_kit(user_tg_id)

            else:  # Юзер отгадал
                std_out_logger.info(f"{user_tg_id}  - Выигрыш\n")
                stroka = (f"{schritt}  Ход  <b>{temp_res.count('Ox')} "
                          f"{language_dict['more bulls'][language]} "
                          f"  \U0001f402  \U0001f402  \U0001f402  \U0001f402   !!!</b>!!! \n")
                pip_print = " ".join(secret_kit)
                await asyncio.sleep(1)
                await message.answer(stroka)
                await message.answer_sticker(sticker_dict['win 4 bools'])
                await message.answer(f"{language_dict['wow'][language]}"
                                     f"{html.bold(html.quote(message.chat.first_name))}"
                                     f"{language_dict['user guessed'][language]}"
                                     f"<b>{pip_print}</b>")
                await asyncio.sleep(1)
                await reset_user_data_after_finish(user_tg_id)  # Здесь происходит перезапись значений в словаре юзера
                await state.set_state(FSM_IN_GAME.choose_level)  # Вывожу юзера из игры
                await message.answer(text=language_dict['play new game after user wins'][language],
                                     reply_markup=k_after_fin_with_NO[language])

        else:  # Бот отгадал
            bot_win_stroka = (language_dict['bot ugadal'][language] + f"<b>{' '.join(processing_combo)}</b>\n"
                              + language_dict['bots COMBO was'][language] +
                              f"<b>{' '.join(secret_kit)}</b>\n")

            await message.answer(text=bot_win_stroka)
            await message.answer_sticker(sticker_dict['BOT WINS'])
            await asyncio.sleep(1)
            await reset_user_table_over_bot_pobeda(user_tg_id)
            await reset_versusbot_table_over_bot_pobeda(user_tg_id)
            await state.set_state(FSM_IN_GAME.choose_level)  # Вывожу юзера из игры
            await message.answer(text=f"Сыграем ещё ?",
                                 reply_markup=k_after_fin_with_NO[language])

    else:  # Если юзер ввлел одинаковое комбо повторно
        game_list = await return_game_list(user_tg_id)
        print(' game_handlers  game list =', game_list)
        temp_res = await seek_bools(secret_kit, user_combo)
        repeated_att = game_list.index(user_combo) + 1
        repeated_data = " ".join(user_combo)
        stroka = await format_f_string(repeated_data, temp_res, language, schritt)
        new_stroka = stroka[:40]
        rest_stroka = stroka[54:]
        await message.answer(text=f"{language_dict['repeat combo 1'][language]}  <b>{repeated_att}</b> "
                                  f"{language_dict['repeat combo 2'][language]}\n"
                                  f"{new_stroka + rest_stroka}",
                             reply_markup=usual_clava)
