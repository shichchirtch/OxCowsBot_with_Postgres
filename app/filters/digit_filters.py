from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from bot_base import session_marker, User
from sqlalchemy import select




class VERIFY_LEN_INLINE_COMBO(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        async with session_marker() as session:
            user_tg_id = callback.from_user.id
            print("\n\nWork check_secret_combo_in_table Function")
            query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
            n = query.scalar()
            if len(n.inline_user_kit) < 4:
                return True
            return False