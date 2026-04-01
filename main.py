import discord
from discord.ext import commands
from datetime import timedelta
import os

# KEEP ALIVE (Flask)
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot activo"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


TOKEN = os.getenv("TOKEN")
CANAL_ID = 1488724851429478450 # ID del canal donde quieres aplicar esto

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
PALABRAS_PROHIBIDAS = ["nigger", "nigga", "niggeeer", "niggeer"]

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    # Ignorar bots
    if message.author.bot:
        return

    # Solo actuar en el canal específico
    if message.channel.id == CANAL_ID:

        mensaje = message.content.lower()

        tiene_link = "http://" in message.content or "https://" in message.content
        tiene_archivo = len(message.attachments) > 0
        tiene_sticker = len(message.stickers) > 0
        tiene_palabra = any(p in mensaje for p in PALABRAS_PROHIBIDAS)

        if tiene_link or tiene_archivo or tiene_sticker or tiene_palabra:
            try:
                await message.delete()

                # Timeout de 15 minutos
                await message.author.timeout(
                    timedelta(minutes=15),
                    reason="Bromita"
                )

                await message.channel.send(
                    f"{message.author.mention} CAISTE AWEONAO WUAJAJA ",
                    delete_after=1
                )

            except Exception as e:
                print(e)

    await bot.process_commands(message)

# INICIAR KEEP ALIVE
keep_alive()

# INICIAR BOT
bot.run(TOKEN)