from bot_base import session_marker, User, VersusBot
from random import sample
from sqlalchemy import select
import time
from lexicon import language_dict


async def insert_new_user_in_table(user_tg_id: int, name: str):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        print('query =', query)
        needed_data = query.scalar()
        print('needed_data = ', needed_data)
        if not needed_data:
            start_time = int(time.monotonic())
            print('Now we are into first function')
            new_us = User(tg_us_id=user_tg_id, user_name=name, start_time=start_time)
            session.add(new_us)
            await session.commit()


async def check_user_in_table(user_tg_id:int):
    """Функция проверяет есть ли юзер в БД"""
    async with session_marker() as session:
        print("Work check_user Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        print('query = ', query)
        data = query.one_or_none()
        print('data = ', data)
        return data


async def get_user_language(user_tg_id:int):
    '''Функуия возвращает числовой индекс языка на котром ведётся игра'''
    async with session_marker() as session:
        print("\nWork   get_user_language Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        return n.language

async def get_start_time(user_tg_id:int):
    '''Функуия возвращает start_time'''
    async with session_marker() as session:
        print("\nWork   get_start_time Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        return n.start_time

async def insert_time_again(user_tg_id:int):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        needed_data = query.scalar()
        print('\nworks insert_time_again')
        needed_data.start_time = int(time.monotonic())
        await session.commit()

async def insert_secret_kit(user_tg_id:int):
    _tallys_str_bot = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    secret_kit = sample(_tallys_str_bot, k=4)
    async with session_marker() as session:
        print("\n\nWork insert_secret_kit Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        print('secret kit is = ', secret_kit)
        n.secret_kit = secret_kit
        print('n.secret_kit = ', n.secret_kit)
        await session.commit()


async def check_user_in_versus_table(user_tg_id:int):
    """Функция проверяет есть ли юзер в БД Versus"""
    async with session_marker() as session:
        print("\n\nWork check_user_in_Versus Function")
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
        return query.one_or_none()


async def check_user_combo_in_versus_table(user_tg_id:int)->bool:
    """Функция удостоверяется, что юзер ещё не загадал свою комбинацию Боту"""
    async with session_marker() as session:
        print("\nWork check_user_combo_in_versus_table Function")
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
        n = query.one_or_none()
        if n:
            query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
            needed_data = query.scalar()
            if needed_data.user_combo == ['setting_data']:
                return True
            return False
        else:
            print('*9* 90 sting ext func works')
            return False

async def insert_in_versus_table(user_tg_id: int, name: str):
    async with session_marker() as session:
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
        needed_data = query.scalar()
        print('insert_in_versus_table works')
        if not needed_data:
            new_us = VersusBot(tg_us_id=user_tg_id, user_name=name)
            session.add(new_us)
            await session.commit()
        else:
            needed_data.user_combo = ['setting_data']
            needed_data.bot_list = []
            await session.commit()


async def check_secret_kit(user_tg_id:int) -> bool:
    """ Функция проверяет секретную комбинацию """
    async with session_marker() as session:
        print("\nWorks check_secret_kit Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        if n.secret_kit == ['0000']:
            print('n.secret_kit = ', n.secret_kit)
            return True
        return False

async def insert_user_combo_in_versus_table(user_tg_id:int, us_combo: list):
    async with session_marker() as session:
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
        needed_data = query.scalar()
        print('works insert_user_combo_in_versus_table')
        needed_data.user_combo = us_combo
        await session.commit()

async def change_language(user_tg_id:int, language):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        needed_data = query.scalar()
        print('works change_language')
        if language in ('rus', 'кгы'):
            needed_data.language = 0
        elif language in ('eng', 'утп'):
            needed_data.language = 1
        else:
            needed_data.language = 2
        await session.commit()

async def get_bot_first_attempt(tallys_str_bot):
    bot_first_att = sample(tallys_str_bot, k=4)
    return bot_first_att


async def insert_first_bot_combo_in_versus_table(user_tg_id:int, first_bot_combo: list):
    async with session_marker() as session:
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
        needed_data = query.scalar()
        print('insert_first_bot_combo_in_versus_table')
        needed_data.bot_list = [first_bot_combo]
        await session.commit()


async def seek_bools(secret, att):  # Сначала то, что угадывается, потом то, что вводится в попытке угадать
    """Функция возвращает список из строк ['Ox', 'Cow']"""
    temp_game_arr = []
    for k, num in enumerate(att):
        if num not in secret:
            pass
        elif num in secret and num == secret[k]:
            temp_game_arr.append('Ox')
        else:
            temp_game_arr.append('Cow')
    return temp_game_arr


async def append_kit(bot_kit: list, bot_test_combinations: list[list]):
    if bot_kit not in bot_test_combinations:
        bot_test_combinations.append(bot_kit)
        return bot_test_combinations
    return bot_test_combinations


async def verify_when_two_cows(bot_data, secret_kit):
    new_arr = []
    for x in bot_data:
        if x in secret_kit:
            new_arr.append(x)
    for y in secret_kit:
        if y not in new_arr:
            new_arr.append(y)
    return new_arr


async def verify_bools_position(bot_kit: list, secret_kit: list, bot_test_combination: list):
    a, b, c, d = bot_kit
    super_tup = ([a, b, c, d], [a, d, b, c], [a, c, d, b], [a, c, b, d], [a, d, c, b], [a, b, d, c],
                 [b, c, d, a], [b, a, c, d], [b, d, a, c], [b, a, d, c], [b, c, a, d], [b, d, c, a],
                 [c, d, a, b], [c, a, d, b], [c, b, d, a], [c, b, a, d], [c, d, b, a], [c, a, b, d],
                 [d, b, a, c], [d, c, b, a], [d, a, b, c], [d, c, a, b], [d, b, c, a], [d, a, c, b])
    for spisok in super_tup:
        if spisok not in bot_test_combination:
            bot_test_combination.append(spisok)  # Ну и аппендим сразу это в список комбинаций, если его там ещё нет
        if spisok == secret_kit:
            # print('bot_test_combination = ', bot_test_combination)
            return bot_test_combination

    return "something goes wrong"


async def insert_bot_comboline_in_bot_list(user_tg_id: int, comboline: list[list]):
    '''Функция добавляет к первой  комбе бота список попыток отгадать комбо юзера'''
    async with session_marker() as session:
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
        needed_data = query.scalar()
        print('works insert_bot_comboline_in_bot_list')
        first_bot_combo = needed_data.bot_list
        total_comboline = comboline + first_bot_combo #wecheln
        needed_data.bot_list = total_comboline
        await session.commit()

async def insert_bot_comboline_in_bot_list_without_first_combo(user_tg_id: int, comboline: list[list]):
    '''Функция добавляет к первой  комбе бота список попыток отгадать комбо юзера'''
    async with session_marker() as session:
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
        needed_data = query.scalar()
        print('insert_bot_comboline_in_bot_list_without_first_combo')
        needed_data.bot_list = comboline
        await session.commit()


async def return_bot_list(user_tg_id:int):
    async with session_marker() as session:
        print("\nWork return_bot_list Function")
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
        n = query.scalar()
        return n.bot_list

async def return_user_combo_for_bot(user_tg_id:int):
    async with session_marker() as session:
        print("\n\nWork return_user_combo_for_bot Function")
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
        n = query.scalar()
        return n.user_combo

async def return_user_wins(user_tg_id:int):
    async with session_marker() as session:
        print("\n\nWork return_user_wins Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        return n.wins

async def return_total_games(user_tg_id:int):
    async with session_marker() as session:
        print("\n\nWork return_total_games Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        return n.total_games

async def return_bot_wins(user_tg_id:int):
    async with session_marker() as session:
        print("\n\nWork return_bot_wins Function")
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_tg_id))
        n = query.scalar()
        return n.bot_pobeda


async def reset_user_table_over_bot_pobeda(user_id:int):
    '''Функция вносит изменения в строку юзера после победы бота'''
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_id))
        needed_data = query.scalar()
        print('works reset_user_table_over_bot_pobeda')
        needed_data.game_list = []
        needed_data.schritt = 0
        needed_data.total_games += 1
        needed_data.secret_kit = ['0000']
        needed_data.inline_user_kit = ''
        await session.commit()

async def cancel_reset_user_table(user_id:int):
    '''Функция вносит изменения в строку юзера после победы бота'''
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_id))
        needed_data = query.scalar()
        print('works reset_user_table_over_bot_pobeda')
        needed_data.game_list = []
        needed_data.schritt = 0
        needed_data.total_games = 0
        needed_data.secret_kit = ['0000']
        needed_data.inline_user_kit = ''
        needed_data.start_time = 0
        needed_data.wins = 0
        await session.commit()

async def reset_versusbot_table_over_bot_pobeda(user_id:int):
    '''Функция вносит изменения в строку юзера VERSUS_BOT после победы бота'''
    async with session_marker() as session:
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_id))
        needed_data = query.scalar()
        print('works reset_versusbot_table_over_bot_pobeda')
        needed_data.bot_list = []
        needed_data.bot_pobeda += 1
        needed_data.user_combo = ['setting_data']
        await session.commit()


async def cancel_reset_versusbot_table(user_id: int):
    '''Функция вносит изменения в строку юзера VERSUS_BOT после победы бота'''
    async with session_marker() as session:
        query = await session.execute(select(VersusBot).filter(VersusBot.tg_us_id == user_id))
        needed_data = query.scalar()
        print('works reset_versusbot_table_over_bot_pobeda')
        needed_data.bot_list = []
        needed_data.bot_pobeda = 0
        needed_data.user_combo = ['setting_data']
        await session.commit()


async def reset_time(user_id:int):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_id))
        needed_data = query.scalar()
        print('works reset_time')
        needed_data.start_time = 0
        await session.commit()

async def time_counter(start_time)-> str:
    current_time = int(time.monotonic())
    if current_time - start_time < 3600:
        secund = (current_time - start_time) % 60
        minut = (current_time - start_time) // 60
        time_data = f'<b><i>GameTiming : {int(minut)} min, {int(secund)} sec.</i></b>'
        return time_data
    if 3600 < current_time - start_time < 3600*24:
        time_data = '<b><i>More then 1 hour</i></b>'
        return time_data
    else:
        time_data = '<b><i>More then 1 day</i></b>'
        return time_data


async def format_bot_response(bot_test_combo: str, temp_game_arr: list, language: int):
    bot_responce = f"{language_dict['bot says'][language]} <b>{bot_test_combo}</b>\n"

    if temp_game_arr.count('Ox') == 0:
        if temp_game_arr.count('Cow') == 0:
            string = (bot_responce + f"  {language_dict['no cows'][language]}   \U0001f937")
            return string
        elif temp_game_arr.count('Cow') == 1:
            string = (
                    bot_responce + f"  <b>1</b>  {language_dict['1 cow'][language]}     \U0001f42e")
            return string
        else:
            cow_str = " "
            for cow in range(temp_game_arr.count('Cow')):
                cow_str += "\U0001f42e" + "  "
            string = (
                    bot_responce + f"  <b>{temp_game_arr.count('Cow')}</b>  {language_dict['more cows'][language]}     {cow_str}")
            return string
    elif temp_game_arr.count("Ox") == 1:
        if temp_game_arr.count('Cow') == 0:
            string = (
                    bot_responce + f"  <b>1</b>  {language_dict['1 bull'][language]}     \U0001f402")
            return string
        elif temp_game_arr.count('Cow') == 1:
            string = (bot_responce + f"  <b>1</b>  {language_dict['1 bull'][language]}  "
                                     f"  <b>1</b>  {language_dict['1 cow'][language]}   \U0001f402    \U0001f42e")
            return string
        else:
            cow_str = " "
            for cow in range(temp_game_arr.count('Cow')):
                cow_str += "\U0001f42e" + "  "
            string = (bot_responce + f"  <b>1</b>  {language_dict['1 bull'][language]}  "
                                     f"  <b>{temp_game_arr.count('Cow')}</b>  {language_dict['more cows'][language]}   \U0001f402  {cow_str}")
            return string
    elif temp_game_arr.count("Ox") > 1:
        ox_str = " "
        for ox in range(temp_game_arr.count('Ox')):
            ox_str += "\U0001f402" + "  "
        if temp_game_arr.count('Cow') == 0:
            string = (bot_responce + f"  <b>{temp_game_arr.count('Ox')}</b>  {language_dict['more bulls'][language]}   {ox_str}")
            return string
        if temp_game_arr.count('Cow') == 1:
            string = (bot_responce + f"  <b>{temp_game_arr.count('Ox')}</b>  {language_dict['more bulls'][language]}  "
                                   f"  <b>1</b>  {language_dict['1 cow'][language]}   {ox_str} \U0001f42e")
            return string
        else:
            cow_str = " "
            for cow in range(temp_game_arr.count('Cow')):
                cow_str += "\U0001f42e" + "  "
            string = (bot_responce + f"  <b>{temp_game_arr.count('Ox')}</b>  {language_dict['more bulls'][language]}"
                                   f"  <b>{temp_game_arr.count('Cow')}</b>  {language_dict['more cows'][language]}  {ox_str} {cow_str}")
            return string


