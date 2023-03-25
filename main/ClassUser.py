from aiogram.dispatcher.filters.state import State, StatesGroup

class User(StatesGroup):
    user_name = State()
    user_email = State()
    user_phon = State()
    user_password = State()
    user_score = State()
