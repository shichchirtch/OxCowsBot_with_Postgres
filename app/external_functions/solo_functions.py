from bot_base import session_marker, User
from sqlalchemy import select
from lexicon import language_dict

async def secret_kit_is_0000(user_tg_id:int):
    '''Функция проверяет проверяет, что secret_kit == [0000]'''
    async with session_marker() as session:
        print("\nWork secret_kit_is_0000 Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        if n.secret_kit == ['0000']:
            return True
        return False

async def return_secret_kit(user_tg_id:int):
    async with session_marker() as session:
        print("\n\nWork return_secret_kit Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        return n.secret_kit

async def check_game_list(user_tg_id:int, user_combo:list):
    '''Функция проверяет называл ли юзер настоящую комбинацию раньше'''
    async with session_marker() as session:
        print("\n\nWork check_game_list Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        current_game_list = n.game_list
        if user_combo not in current_game_list:
            return True
        return False

async def user_attempt_guess_secret_combo(user_tg_id:int, user_combo:list):
    '''Функция обновляет таблицу User, и записыает в спиское комбинацию юзера новую комбинацию'''
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        needed_data = query.scalar()
        print('works user_attempt_guess_secret_combo')
        needed_data.schritt += 1
        att_list = needed_data.game_list
        new_list = att_list + [user_combo]
        needed_data.game_list = new_list
        await session.commit()

async def return_schritt_quantity(user_tg_id:int):
    async with session_marker() as session:
        print("\n\nWork return_schritt_quantity Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        return n.schritt

async def return_game_list(user_tg_id:int):
    async with session_marker() as session:
        print("\n\nWork return_game_list Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        return n.game_list

async def reset_user_data_after_finish(user_id:int):
    '''Функция вносит изменения в строку юзера полсе победы'''
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_id))
        needed_data = query.scalar()
        print('works reset_user_data_after_finish')
        needed_data.wins += 1
        needed_data.game_list = []
        needed_data.schritt = 0
        needed_data.total_games+=1
        needed_data.secret_kit = ['0000']
        needed_data.inline_user_kit = ''
        await session.commit()


async def format_f_string(user_combo: str, temp_res: list, language:int, schritt:int) -> str:
    responce = (f"{language_dict['your combo'][language]} <b>{user_combo}</b>\n"
                f"<b>{schritt+1}</b> {language_dict['Xod'][language]}")

    if temp_res.count('Ox') == 0:
        if temp_res.count('Cow') == 0:
            string = (responce + f"  {language_dict['no cows'][language]}   \U0001f937")
            return string
        elif temp_res.count('Cow') == 1:
            string = (responce + f"  <b>1</b>  {language_dict['1 cow'][language]}     \U0001f42e")
            return string
        else:
            cow_str = " "
            for cow in range(temp_res.count('Cow')):
                cow_str += "\U0001f42e" + "  "
            string = (
                        responce + f"  <b>{temp_res.count('Cow')}</b>  {language_dict['more cows'][language]}     {cow_str}")
            return string
    elif temp_res.count("Ox") == 1:
        if temp_res.count('Cow') == 0:
            string = (responce + f"  <b>1</b>  {language_dict['1 bull'][language]}     \U0001f402")
            return string
        elif temp_res.count('Cow') == 1:
            string = (responce + f"  <b>1</b>  {language_dict['1 bull'][language]}  "
                                 f"  <b>1</b>  {language_dict['1 cow'][language]}   \U0001f402    \U0001f42e")
            return string
        else:
            cow_str = " "
            for cow in range(temp_res.count('Cow')):
                cow_str += "\U0001f42e" + "  "
            string = (responce + f"  <b>1</b>  {language_dict['1 bull'][language]}  "
                                 f"  <b>{temp_res.count('Cow')}</b>  {language_dict['more cows'][language]}   \U0001f402  {cow_str}")
            return string
    elif temp_res.count("Ox") > 1:
        ox_str = " "
        for ox in range(temp_res.count('Ox')):
            ox_str += "\U0001f402" + "  "
        if temp_res.count('Cow') == 0:
            string = (
                        responce + f"  <b>{temp_res.count('Ox')}</b>  {language_dict['more bulls'][language]}   {ox_str}")
            return string
        if temp_res.count('Cow') == 1:
            string = (
                        responce + f"  <b>{temp_res.count('Ox')}</b>  {language_dict['more bulls'][language]}  "
                                   f"  <b>1</b>  {language_dict['1 cow'][language]}   {ox_str} \U0001f42e")
            return string
        else:
            cow_str = " "
            for cow in range(temp_res.count('Cow')):
                cow_str += "\U0001f42e" + "  "

            string = (
                        responce + f"  <b>{temp_res.count('Ox')}</b>  {language_dict['more bulls'][language]}"
                                   f"  <b>{temp_res.count('Cow')}</b>  {language_dict['more cows'][language]}  {ox_str} {cow_str}")
            return string



