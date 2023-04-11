import requests

from aiogram import types

from handlers.users.mechanic import menu
from loader import dp




@dp.callback_query_handler(text="menu")
async def menu_button(call: types.CallbackQuery):
    await menu(message=call.message)

