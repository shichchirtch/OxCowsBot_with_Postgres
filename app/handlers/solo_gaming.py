from aiogram import Router, html
import asyncio
from loggers import std_out_logger
from lexicon import *
from filters import DATA_IS_DIGIT
from external_functions import *
from keyboards import *
from bot_base import four_bools
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import StateFilter
from states import FSM_IN_GAME, ingame_states
from external_functions.digit_functions import (return_data_from_inline_user_kit,
                                                    reset_inline_user_kit)

from external_functions.solo_functions import (secret_kit_is_0000,
                                                   return_secret_kit,
                                                   user_attempt_guess_secret_combo,
                                                   return_schritt_quantity,
                                                   reset_user_data_after_finish,
                                                   return_game_list,
                                                   check_game_list
                                                   )
from external_functions.external_functions import (insert_secret_kit,
                                    seek_bools,
                                    check_user_in_table,
                                    check_user_combo_in_versus_table,
                                    )
yes_no_kb = (keyboard_yes_no, keyboard_yes_no_eng, keyboard_yes_no_de)

solo_router = Router()

k_af = (keyboard_game_level_with_NO_rus, keyboard_game_level_with_NO_en,
                       keyboard_game_level_with_NO_de)
digit_keyboards_tuple = (keyboard_digits_Rus, keyboard_digits, keyboard_digits_De)
multi_start_clava = (start_clava, start_clava_eng, start_clava_de)


@solo_router.message(DATA_IS_DIGIT(), StateFilter(FSM_IN_GAME.solo))
async def solo_gaming(message: Message, state: FSMContext):
    """В хэндлер попадают комбинации юзера в режиме SOLO"""
    print('SOLO !')
    user_tg_id = message.from_user.id
    language = await get_user_language(user_tg_id)
    if await secret_kit_is_0000(user_tg_id):
        await insert_secret_kit(user_tg_id)
    returned_secret_kit = await return_secret_kit(user_tg_id)  # Комбинация, которую угадывает Юзер
    if message.text == button_emoji:
        _inline_entered_user_kit = await return_data_from_inline_user_kit(user_tg_id)
        sending_user_combo = list(_inline_entered_user_kit)  # Если Юзер ввел комбинацию инлайн клавиатурой
    else:
        sending_user_combo = list(message.text)  # Если юзер ввел комбо обычной клавой

    temp_res = await seek_bools(returned_secret_kit, sending_user_combo)
    schritt = await return_schritt_quantity(user_tg_id)
    if await check_game_list(user_tg_id, sending_user_combo):  # Если такой комбы ещё нет в списке юзера
        await user_attempt_guess_secret_combo(user_tg_id, sending_user_combo)  # Вписываю новую комбинацию в список game_list

        std_out_logger.info(
            f"SOLO {user_tg_id} ход {schritt}, "
            f"AttemtCOMBO  =  {sending_user_combo}   совпадения = {temp_res}")

        if temp_res != four_bools:
            if message.text == button_emoji:
                _inline_entered_user_kit = await return_data_from_inline_user_kit(user_tg_id)
                current_data = " ".join(list(_inline_entered_user_kit))
                stroka = await format_f_string(current_data, temp_res, language, schritt)
                await message.reply(stroka, reply_markup=usual_clava)
            else:
                current_data = " ".join(sending_user_combo)
                stroka = await format_f_string(current_data, temp_res, language, schritt)
                await message.answer(stroka, reply_markup=usual_clava)

            await asyncio.sleep(1)
            await message.answer(language_dict["next combo do"][language],
                                 reply_markup=digit_keyboards_tuple[language])

            await reset_inline_user_kit(user_tg_id)  # Стираю инлайн комбо
        else:
            stroka = (f"{schritt}  Ход  <b>{temp_res.count('Ox')}</b> "
                      f"<b>{language_dict['more bulls'][language]} "
                      f' \U0001f402  \U0001f402  \U0001f402  \U0001f402   !!!</b> \n')
            pip_print = " ".join(returned_secret_kit)
            await asyncio.sleep(1)
            await message.answer(stroka)
            await message.answer_sticker(sticker_dict['win 4 bools'])
            await message.answer(f"{language_dict['wow'][language]}"
                                 f"{html.bold(html.quote(message.chat.first_name))}"
                                 f"{language_dict['user guessed'][language]}"
                                 f"<b>{pip_print}</b>",
                                 parse_mode=ParseMode.HTML)
            std_out_logger.info(
                f"SOLO ******************* {user_tg_id} "
                f"ход {schritt}  WINS\n")
            await asyncio.sleep(1)

            await reset_user_data_after_finish(user_tg_id)   # Здесь происходит перезапись значений в словаре юзера
            await state.set_state(FSM_IN_GAME.choose_level)
            await message.answer(text=language_dict['play new game after user wins'][language],
                                 reply_markup=k_af[language])
    else:  # Если юзер повторно ввел то, что уже вводил ранее

        game_list = await return_game_list(user_tg_id)
        repeated_att = game_list.index(sending_user_combo) + 1
        repeated_data = " ".join(sending_user_combo)
        stroka = await format_f_string(repeated_data, temp_res, language, schritt)
        new_stroka = stroka[:40]
        rest_stroka = stroka[54:]
        await message.answer(
            text=f"{language_dict['repeat combo 1'][language]}  <b>{repeated_att}</b> "
                 f"{language_dict['repeat combo 2'][language]}\n"
                 f"{new_stroka + rest_stroka}",
            reply_markup=usual_clava)


@solo_router.message()
async def process_other_answers(message: Message, state: FSMContext):
    print("WORKS OTHER HANDLER !")
    user_id = message.from_user.id
    language = await get_user_language(user_id)
    status = await state.get_state()
    us_combo = await check_user_combo_in_versus_table(user_id)
    if not await check_user_in_table(user_id):
        await message.answer(language_dict['start chat'][language])
    if status in ingame_states[0]:
        await message.answer(text=language_dict['in bot combo'][language])
    elif status in ingame_states[1:]:
        if us_combo: # Если еще не записана комбинация юзера
            await message.answer(text=language_dict['not repeat'][language])
        else:
            await reset_inline_user_kit(user_id)
            await message.answer(text=language_dict['wrong sent data'][language],
                                 reply_markup=digit_keyboards_tuple[language])
            await message.answer(text=language_dict['next combo do'][language],
                                 reply_markup=usual_clava)
    elif status == 'FSM_IN_GAME:not_in_game':
        await message.answer(text=language_dict['noch ein mal'][language],
                             reply_markup=yes_no_kb[language])
    else:
        if message.text == ('/start'):
            await message.answer(language_dict['restart'][language])
        else:
            await message.reply(language_dict['silly bot'][language])
            await message.answer_sticker(sticker_dict['silly bot'],
                                         reply_markup=multi_start_clava[language])
