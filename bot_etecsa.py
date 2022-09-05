#from python standar
import os
from re import search
import sys
import random
import subprocess
import urllib.parse
#from requests
import requests
#from aiogram3b
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

dp = Dispatcher()

TOKEN = os.getenv("TOKEN")  


########################## COMMANDS ZONE ###############################


@dp.message(Command(commands=["start"]))
async def command_start_handler(message):   
    await message.answer(f"Hola <b>{message.from_user.full_name}!</b>\nEste Bot esta en desarrollo, El unico comando disponible hasta el momento es /buscar, para utilizarlo escriba /buscar (Nombre o numero de telefono) y se le mostrara los primeros 5 resultados")

@dp.message(Command(commands=["ping"]))
async def command_ping_handler(message):
    the_command = ["ping","api.telegram.org","-c4"]
    ping_telegram = subprocess.check_output(the_command)
    ping_telegram = ping_telegram.decode()   
    await message.answer(ping_telegram)

@dp.message(Command(commands=["buscar"]))
async def command_buscar_handler(message):   
    text = message.text
    text_filter = text.replace("/buscar","")
    search = urllib.parse.quote_plus(text_filter)
    print(search)
    await message.answer(f"Cargando los 5 primeros resultados")
    try:
        data = requests.get(f"https://directorioetecsa.com/api/search?q={search}&offset=0&limit=5", timeout=5).json()
        for result in data["data"]:
            reply_msg = f"Nombre: {result['name']}\n\nNumero: {result['number']}\n\nDireccion: {result['address']}"
            await message.answer(reply_msg)           
    except:
        await message.answer(f"Resultados no encontrados")
        

@dp.message()
async def test(message):
    text = message.text
    search = urllib.parse.quote_plus(text)
    print(search)
    await message.answer(f"Cargando los 5 primeros resultados")
    try:
        data = requests.get(f"https://directorioetecsa.com/api/search?q={search}&offset=0&limit=5", timeout=5).json()
        for result in data["data"]:
            reply_msg = f"Nombre: {result['name']}\n\nNumero: {result['number']}\n\nDireccion: {result['address']}"
            await message.answer(reply_msg)           
    except:
        await message.answer(f"Resultados no encontrados")

########################################################################


def main():   
    bot = Bot(TOKEN, parse_mode="HTML")
    dp.run_polling(bot)

if __name__ == "__main__":
    print("BOT_STARTED")
    main()