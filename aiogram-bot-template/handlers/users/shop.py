from aiogram import types

from loader import dp, bot


def webAppKeyboard(): #создание клавиатуры с webapp кнопкой
   keyboard = types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
   webAppTest = types.WebAppInfo(url="https://telegram.mihailgok.ru") #создаем webappinfo - формат хранения url
   one_butt = types.KeyboardButton(text="Тестовая страница", web_app=webAppTest) #создаем кнопку типа webapp
   keyboard.add(one_butt) #добавляем кнопки в клавиатуру

   return keyboard #возвращаем клавиатуру


@dp.callback_query_handler(text="shop")
async def settings(call: types.CallbackQuery):
   await bot.send_message(call.message.chat.id, 'Привет, я бот для проверки телеграмм webapps!)', reply_markup=webAppKeyboard())
