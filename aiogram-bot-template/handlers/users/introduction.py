from aiogram import types

from loader import dp, bot



@dp.callback_query_handler(text="acquaintance1")
async def acquaintance1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 1 из 4", callback_data="acquaintance2"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/708da2a1ba2954484472febd4d67d676fff3265c67cc33b7763359a40c54d7b7/641b2f71/aav889LViY80SFUJZROaEjgDvA_RgSmArNa4MWmSMaCDjBzheks2RgabpYMt1IWnDWFHGuiykGvN0iSzLZcCaQ%3D%3D?uid=0&filename=Картинка%201.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         reply_markup=keyboard)


@dp.callback_query_handler(text="acquaintance2")
async def acquaintance2(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 2 из 4", callback_data="acquaintance3"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/675beca8b0c73621c8bb93ad309a2bc392fce936bf2269202c0cbaa638992921/641b2f71/bnKFXL36r_9d3cmMsF811DgDvA_RgSmArNa4MWmSMaBqXNsSKkLemGiXltOTt2XxrP3QnBfkefLtrVZrGDsYSA%3D%3D?uid=0&filename=Картинка%202.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         reply_markup=keyboard)


@dp.callback_query_handler(text="acquaintance3")
async def acquaintance3(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 3 из 4", callback_data="acquaintance4"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/e0ccd104f293af9bb09f7244077d63dcca5d13b16bc6423c57b340b2569a0873/641b2f71/Gvr4pk1H6sUpkuCxyJBbSxQTsnBTv7czpn4fvlwOl86aUylQQgWBrMFcFBnGDFBOl68-D4SgN0TZqx5DlAWBTQ%3D%3D?uid=0&filename=Картинка%203.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         reply_markup=keyboard)


@dp.callback_query_handler(text="acquaintance4")
async def acquaintance3(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Участвовать в программе", callback_data="connect_program"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/e9599f3bb92d46099f03878960e455d8f839b24b3201b7e08faaa04aab2247e0/641b2f71/UHyX3SC38i03tcHZeugg2zgDvA_RgSmArNa4MWmSMaAju5NW2rzj6hCzx5XNaPzYjzPrupLrYk3rMo_85KYgkQ%3D%3D?uid=0&filename=Картинка%204.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         reply_markup=keyboard)
