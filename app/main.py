import asyncio
from aiogram import Bot, Dispatcher
from handlers import command_handlers, game_handlers, solo_gaming, digit_buttons
from bot_base import init_models
from aiogram.enums import ParseMode
from states import redis_storage
from config import settings
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties

# Функция конфигурирования и запуска бота
async def main():
    await init_models()
    # Инициализируем бот и диспетчер
    bot = Bot(token=settings.BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=redis_storage)
    # Регистрируем роутеры в диспетчере
    dp.include_router(command_handlers.command_router)
    dp.include_router(game_handlers.game_router)
    dp.include_router(digit_buttons.digit_router)
    dp.include_router(solo_gaming.solo_router)

    async def set_main_menu(bot: Bot):
        # Создаем список с командами и их описанием для кнопки menu
        main_menu_commands = [
            BotCommand(command='/help',
                       description='Справка по работе бота'),
            BotCommand(command='/set',
                       description='Выбрать вариант игры'),
            BotCommand(command='/schet',
                       description='Узнать счёт'),
            BotCommand(command='/cancel',
                       description='Закончить игру')]

        await bot.set_my_commands(main_menu_commands)
    # Регистрируем асинхронную функцию в диспетчере,
    # которая будет выполняться на старте бота,
    dp.startup.register(set_main_menu)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())