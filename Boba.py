import sqlite3
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'ТВОЙ_ТОКЕН_ОТ_BOTFATHER'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Создание базы
conn = sqlite3.connect('balances.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance REAL DEFAULT 0.00
)''')
conn.commit()

# Старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    await message.answer("👋 Добро пожаловать! Ваш баланс: 0.00$")

# Обработка эмодзи "777"
@dp.message_handler(lambda message: '🎰' in message.text)
async def slot_win(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("UPDATE users SET balance = balance + 7.77 WHERE user_id = ?", (user_id,))
    conn.commit()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]
    await message.answer(f"💰 Вы получили 7.77$! Новый баланс: {balance:.2f}$")

# Пополнение через "тестнет"
@dp.message_handler(commands=['deposit'])
async def deposit(message: types.Message):
    user_id = message.from_user.id
    # Здесь можешь вставить свою интеграцию с CryptoBot API
    # Для теста просто эмулируем пополнение
    cursor.execute("UPDATE users SET balance = balance + 100.0 WHERE user_id = ?", (user_id,))
    conn.commit()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]
    await message.answer(f"🚀 Баланс пополнен на 100$. Новый баланс: {balance:.2f}$")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
