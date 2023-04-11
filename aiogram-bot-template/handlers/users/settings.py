
from aiogram import types

from loader import dp, bot


@dp.callback_query_handler(text="setting")
async def settings(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    button2 = types.InlineKeyboardButton(text="Изменить имя", callback_data="menu")
    button3 = types.InlineKeyboardButton(text="Добавить город (+🟡1000)", callback_data="menu")
    button4 = types.InlineKeyboardButton(text="Добавить номер школы (+🟡1000)", callback_data="menu")
    button5 = types.InlineKeyboardButton(text="Добавить класс (+🟡2000)", callback_data="menu")
    button6 = types.InlineKeyboardButton(text="Добавить номер телефона (+🟡2000)", callback_data="menu")
    button1 = types.InlineKeyboardButton(text="Вернуться в кабинет", callback_data="menu")

    keyboard.row(button2)
    keyboard.row(button3)
    keyboard.row(button4)
    keyboard.row(button5)
    keyboard.row(button6)
    keyboard.row(button1)
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/be8c6828c1e6e75e96a8e49a43cf77659ca674e43184fc052444abf34d61d53a/642c66a8/ZA5nVuIWol8rtRW1_HfPdkr9N2DqxgbnVTwuaGpxRfbqKB8X4Rv4XveNYgEnFi37mZoWyINjeUnDjXMa-zJdHw%3D%3D?uid=0&filename=Картинка%205%20–%202.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption='Здесь ты можешь настроить свой профиль', reply_markup=keyboard)