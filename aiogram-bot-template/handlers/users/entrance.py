from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from handlers.users.start import user_username, id_user
from loader import dp, bot

@dp.callback_query_handler(text="entrance")
async def entrance(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Выбрать ВУЗ", callback_data="UNIVERSITY")
    button2 = types.InlineKeyboardButton(text="Назад", callback_data="menu")
    keyboard.add(button1,button2)
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/2c9d6195fe98b386fd8540c15d602b1317bca79f8a3a59b5762170f211982e7c/642d780e/Kh-Qn5DFYEbHzwNGp49Ky0r9N2DqxgbnVTwuaGpxRfbQL9_zVXCWPArtRDZ4DQq2P1Lj_grgMww07gcjAV4_PA%3D%3D?uid=0&filename=Картинка%206.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption="Serega_4, поступите в один из университетов со скидкой от Sokrat.\n\n"
                              "Sokrat - это:\n- Бесплатная консультация\n- Подача документов онлайн\n"
                              "- Подбор ВУЗа бесплатно\n- Выгодные условия поступления\n- Поступление без ЕГЭ*\n\n"
                              "*Действует не на все учебные заведения - партнеры Sokrat",
                         reply_markup=keyboard)


@dp.callback_query_handler(text="UNIVERSITY")
async def UNIVERSITY(call: types.CallbackQuery):

    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Уневер 1", callback_data="Уневер 1")
    button2 = types.InlineKeyboardButton(text="Уневер 2", callback_data="Уневер 2")
    button3 = types.InlineKeyboardButton(text="Назад", callback_data="entrance")
    keyboard.row(button1)
    keyboard.row(button2)
    keyboard.row(button3)

    await call.message.answer("Выберете один из учебных заведений:", reply_markup=keyboard)


@dp.callback_query_handler(text="Уневер 1")
async def UNIVERSITY_1(call: types.CallbackQuery):


    keyboard = types.InlineKeyboardMarkup()
    button3 = types.InlineKeyboardButton(text="В личный кабинет", callback_data="menu")
    keyboard.row(button3)
    await call.message.answer("Ваша заявка отправлена.\nНаш специалист свяжется с вами в ближайшее время", reply_markup=keyboard)
    await bot.send_message(ADMINS,f'Пользователь {user_username},отпраил запрос на поступление в 1 Уневер')


@dp.callback_query_handler(text="Уневер 2")
async def UNIVERSITY_1(call: types.CallbackQuery):


        keyboard = types.InlineKeyboardMarkup()
        button3 = types.InlineKeyboardButton(text="В личный кабинет", callback_data="menu")
        keyboard.row(button3)
        await call.message.answer("Ваша заявка отправлена.\nНаш специалист свяжется с вами в ближайшее время",
                                  reply_markup=keyboard)
        await bot.send_message(ADMINS,
                               f'Пользователь {user_username},отпраил запрос на поступление в 2 Уневер')
