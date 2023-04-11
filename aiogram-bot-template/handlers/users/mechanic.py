from aiogram import types
from aiogram.dispatcher import FSMContext
import requests

from handlers.users.instruction import instruction

from loader import dp, bot
from states.ClassUser import User

new_user = False
email = ''
phon = ''
score_user = ''
user_token = ''


@dp.callback_query_handler(text="connect_program")
async def connect(call: types.CallbackQuery, state: FSMContext):
    await _connect(call.message)


@dp.message_handler(state=User.user_email)
async def registr_1(message: types.Message, state: FSMContext):
    global new_user, email
    email = message.text
    await state.update_data(user_email=email)

    if await check_email(email):
        await message.answer("Ваш профиль найден!\nВведите ваш пароль")
        new_user = False
    else:
        await message.answer("Ваш профиль не найден.\nПройдите регестрацию пожалуйста\nВведите пароль")
        new_user = True
    await User.user_password.set()


@dp.message_handler(state=User.user_password)
async def password(message: types.Message, state: FSMContext):
    global new_user
    if(new_user):
        await message.answer("Введите пароль потворно")
        password = message.text
        await state.update_data(user_password=password)
        await User.user_password_sweaty.set()
    else:
        await Authorization(message, state)


@dp.message_handler(state=User.user_password_sweaty)
async def Registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    email = data.get('user_email')
    password = data.get('user_password')
    await state.finish()
    await user_reg(email, password, message, state)


async def Authorization(message: types.Message, state: FSMContext):
    password = message.text
    await state.update_data(user_password=password)
    global email
    await autor_user(email, password, message,state)


async def autor_user(mail,password, message: types.Message,state: FSMContext ):
    url = "https://admin.sokratapp.ru/api/api-token-auth/"

    data_auto = {
        "username": f"{mail}",
        "password": f"{password}"
    }
    try:
        global email, phon, score_user, user_token
        r_admin = requests.post(url, data=data_auto)
        r_admin_json = r_admin.json()

        url_user = f"https://admin.sokratapp.ru/api/user_me"

        headers = {'Authorization': f'Token {r_admin_json["token"]}'}

        user_token = r_admin_json["token"]

        r_user = requests.get(url=url_user, headers=headers)

        r_user_json = r_user.json()

        email = r_user_json['email']
        score_user = r_user_json['money_for_grades']
        phon = r_user_json['phone']

        await instruction(message)
        await state.finish()
    except:
        await message.answer("Неверный пароль или логин")
        await message.answer("Введите пароль потворно")
        await User.user_password.set()


async def check_email(email):
    url = 'https://admin.sokratapp.ru/api/users/check_email/'

    data = {
        "email": email
    }

    r = requests.get(url=url, data=data)

    try:
        r.raise_for_status()
        return True
    except:
        return False


async def menu(message: types.Message):

    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text="Обменять оценку через онлайн дневник", callback_data="online_diary")
    button2 = types.InlineKeyboardButton(text="Онлайн поступление", callback_data="entrance")
    button3 = types.InlineKeyboardButton(text="Обменять оценку по фото", callback_data="exchange")
    button4 = types.InlineKeyboardButton(text="Школьный магазин", callback_data="online_diary")
    button5 = types.InlineKeyboardButton(text="Подбери репититора", url="https://sokratapp.ru/courses/category/repetitori/")
    button6 = types.InlineKeyboardButton(text="Настройки", callback_data="setting")

    keyboard.row(button1)
    keyboard.row(button2)
    keyboard.row(button3)
    keyboard.row(button4)
    keyboard.row(button5)
    keyboard.row(button6)

    await bot.send_photo(chat_id=message.chat.id,
        photo="https://downloader.disk.yandex.ru/preview/269dea1c26fd03511dc15c8f882192d1cb426565d3ebab81ca395fe36ad19a34/64349bd6/Eb7aDNN3SyZbfZoHBZKdVEr9N2DqxgbnVTwuaGpxRfavoL5Ma0_a80ZJBMrut8AitqUo7oGWHMZa1xwj9fou9Q%3D%3D?uid=0&filename=Картинка%205.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=714x943",
        caption=  f"👤 Ваш профиль:\nВаша почта: {email}  \nВаш телефон:  {phon}\n"
        f"Город: \nНомер школы: \nКласс: \nКуда планируете поступать:\n"
        f"\nВаши монеты Сократа: 🟡{score_user}"
        f"\n\n↪️ Пригласи друга: https://t.me/Kalinenocbot",
                         reply_markup=keyboard)




async def user_reg(email, password,message: types.Message,state: FSMContext):

    if message.text == password:

        url = 'https://admin.sokratapp.ru/api/users/signup/'

        body = {
            "email": f"{email}",
            "first_name": "",
            "last_name": "",
            "password": f"{password}"
        }

        r = requests.post(url=url, data=body)

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Выполнить авторизацию", callback_data="connect_program"))

        await message.answer("Успешно",reply_markup=keyboard)

    else:
        await message.answer("Введены не соответствующие пароли")


async def _connect(message: types.Message):
    await message.answer("Введите вашу почту, для начала авторизации.")
    await User.user_email.set()


async def money_for_grades(count):
    url_user = f"https://admin.sokratapp.ru/api/user_me"
    global score_user
    headers = {'Authorization': f'Token {user_token}'}

    r_user = requests.get(url=url_user, headers=headers)
    r_user_json = r_user.json()

    score_user = r_user_json['money_for_grades'] + count

    grades = {'money_for_grades': f'{score_user}'}
    r = requests.patch(url=url_user, headers=headers, data=grades)

