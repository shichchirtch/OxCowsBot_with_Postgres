from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config import settings

using_redis = Redis(host=settings.REDIS_HOST)
redis_storage = RedisStorage(redis=using_redis)

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSM_IN_GAME(StatesGroup):
    not_in_game = State()
    choose_level = State()  # Состояние выбора уровня игры, наступает в set_game_level,
                            # срабатывает только в update_user_game_level
    solo = State()        # Состояние в игре SOLO
    with_silly_bot = State()  # Игра с ботом
    with_smart_bot =State()

ingame_states = ('FSM_IN_GAME:solo', 'FSM_IN_GAME:with_silly_bot', 'FSM_IN_GAME:with_smart_bot')
# all_states = ()