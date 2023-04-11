from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = "6281107032:AAF5kZPJCDXCu4UjoLS5quYtiI8LM5jw56Y" # Забираем значение типа str
ADMINS = 1073170752  # Тут у нас будет список из админов
IP = "localhost" # Тоже str, но для айпи адреса хоста

