from bot_base import session_marker, User
from sqlalchemy import select



async def check_digit_in_inline_user_kit(user_tg_id:int):
    '''Функция роверяет строку inline_user_kit'''
    async with session_marker() as session:
        print("\n\nWork check_secret_combo_in_table Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        if len(n.inline_user_kit) <= 3:
            return True
        return False

async def format_string(inline: str) -> str:
    empty_space = 4
    dlina_inline = len(inline)
    empty_space = empty_space - dlina_inline
    returned_stroka = inline + "*" * empty_space
    return returned_stroka

async def return_data_from_inline_user_kit(user_id:int):
    async with session_marker() as session:
        print("\n\nWork return_data_from_inline_user_kit Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_id))
        n = query.scalar()
        return n.inline_user_kit

async def check_len_inline_combo(data:str)->bool:
    if len(data)<=4:
        return True
    return False

async def insert_digit_combo_in_inline_user_kit(user_tg_id:int, user_combo:str):
    async with session_marker() as session:
        print("\n\nWork insert_digit_combo_in_inline_user_kit Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        n.inline_user_kit = user_combo
        await session.commit()

async def reset_inline_user_kit(user_tg_id:int):
    async with session_marker() as session:
        print("\n\nWork reset_inline_user_kit Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        n = query.scalar()
        n.inline_user_kit = ''
        await session.commit()

