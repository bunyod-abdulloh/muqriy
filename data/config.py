from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot Token
ADMIN_ID = env.str("ADMINS")  # adminlar ro'yxati
BASE_URL = env.str("BASE_URL")
WEBHOOK_PATH = f'/{BOT_TOKEN}'
HOST = env.str("HOST")
PORT = env.int("PORT")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
