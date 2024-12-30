import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# Konfigurasi bot
API_TOKEN = "7795659708:AAGG5Kiz6AlNzY2iwvFdu2T8z1mx73U7Wqk"

# ID pengguna yang memiliki akses awal
AUTHORIZED_USERS = {6641413945}

# Payload tetap
DEFAULT_PAYLOAD = {
    "domain": "milwaa.cute",
    "password": "MilwaLog",
    "partner": "6282120420422",
}

URL = "https://api.viupremium.us.kg/create-account"

# Inisialisasi bot dan dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def generate_account_handler(message: Message):
    user_id = message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        await message.reply("You are not authorized to use this command.")
        return

    try:
        await message.reply("Processing your request, please wait...")

        headers = {
            "Content-Type": "application/json"
        }

        payload = DEFAULT_PAYLOAD.copy()
        payload["amount"] = 1  # Tetap

        async with aiohttp.ClientSession() as session:
            async with session.post(URL, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('success'):
                        accounts = result.get('accounts', [])
                        accounts_text = '\n'.join(accounts)
                        await message.reply(f"Account created successfully:\n{accounts_text}")
                    else:
                        await message.reply("Account creation failed. Response:")
                        await message.reply(str(result))
                else:
                    await message.reply(f"Failed to create account. HTTP Status Code: {response.status}")
                    await message.reply(await response.text())

    except Exception as error:
        await message.reply(f"An error occurred: {str(error)}")

async def generate_multiple_accounts_handler(message: Message):
    user_id = message.from_user.id
    if user_id != 6641413945:  # Akses mutlak hanya untuk 6641413945
        await message.reply("You are not authorized to use this command.")
        return

    try:
        command_parts = message.text.split()
        if len(command_parts) != 2:
            await message.reply("Usage: /gens <amount> (max: 20)")
            return

        amount = int(command_parts[1])
        if amount < 1 or amount > 20:
            await message.reply("Amount must be between 1 and 20.")
            return

        await message.reply(f"Processing {amount} accounts, please wait...")

        headers = {
            "Content-Type": "application/json"
        }

        payload = DEFAULT_PAYLOAD.copy()
        payload["amount"] = amount

        async with aiohttp.ClientSession() as session:
            async with session.post(URL, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('success'):
                        accounts = result.get('accounts', [])
                        accounts_text = '\n'.join(accounts)
                        await message.reply(f"{amount} accounts created successfully:\n{accounts_text}")
                    else:
                        await message.reply("Account creation failed. Response:")
                        await message.reply(str(result))
                else:
                    await message.reply(f"Failed to create accounts. HTTP Status Code: {response.status}")
                    await message.reply(await response.text())

    except ValueError:
        await message.reply("Invalid amount. Please provide a numeric value.")
    except Exception as error:
        await message.reply(f"An error occurred: {str(error)}")

async def start_handler(message: Message):
    user_id = message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        await message.reply("You are not authorized to use this bot.")
    else:
        await message.reply("Welcome! You are authorized to use this bot.")

async def main():
    # Daftarkan handler
    dp.message.register(start_handler, Command(commands=["start"]))
    dp.message.register(generate_account_handler, Command(commands=["gen"]))
    dp.message.register(generate_multiple_accounts_handler, Command(commands=["gens"]))

    # Mulai polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())