from aiogram import Dispatcher

from bot.hendlers.director import director_router
from bot.hendlers.employees import employees_router
from bot.hendlers.start import start_router

dp = Dispatcher()
dp.include_routers(
    start_router,
    director_router,
    employees_router
)
