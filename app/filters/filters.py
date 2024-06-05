from aiogram.filters import BaseFilter
from aiogram.types import Message
from external_functions import (check_user_in_table,
                                    check_secret_kit,
                                    check_user_combo_in_versus_table,
                                    return_data_from_inline_user_kit)
from keyboards import button_emoji

class DATA_IS_DIGIT(BaseFilter):
    async def __call__(self, message: Message):
        user_id = message.from_user.id
        if message.text == button_emoji:
            _entered_user_kit = await return_data_from_inline_user_kit(user_id)
            temp_combo_set = set(_entered_user_kit)
            if (_entered_user_kit.isdigit()
                    and len(temp_combo_set) == 4
                    and len(_entered_user_kit) == 4):
                return True
            return False
        else:
            if len(message.text) == len(set(message.text)) and len(message.text) == 4 and message.text.isdigit():
                return True
            return False

class DATA_IS_NOT_DIGIT(BaseFilter):
    async  def __call__(self, message:Message):
        print('DATA_IS_NOT_DIGIT works')
        if not message.text.isdigit():
            return True
        return False


class START_ONCE_ONLY(BaseFilter):
    async def __call__(self, message: Message):
        print("START_ONCE_ONLY Filter works")
        user_tg_id = message.from_user.id
        if await check_user_in_table(user_tg_id):
            return False
        return True

class BOT_COMBO(BaseFilter):
    async def __call__(self, message: Message):
        print("BOT_COMBO_FILTR works")
        user_tg_id = message.from_user.id
        if await check_secret_kit(user_tg_id): # line 108 ext func
            return True
        return False # changed true/false

class NOT_USER_COMBO(BaseFilter):
    async def __call__(self, message: Message):
        user_tg_id = message.from_user.id
        if await check_user_combo_in_versus_table(user_tg_id):
            return True
        return False

class INLINE_FILTER(BaseFilter):
    async def __call__(self, massage: Message):
        if massage.text == button_emoji:
            return False
        return True