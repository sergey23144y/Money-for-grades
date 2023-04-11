from aiogram import types
from aiogram.dispatcher import FSMContext
import requests

from handlers.users.instruction import instruction
from handlers.users.mechanic import check_email, user_reg, _connect

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


