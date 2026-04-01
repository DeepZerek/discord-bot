import discord
from discord.ext import commands
from datetime import timedelta
import os

TOKEN = os.getenv("TOKEN")
CANAL_ID = 1236226637490688034  # ID del canal donde quieres aplicar esto

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    # Ignorar bots
    if message.author.bot:
        return

    # Solo actuar en el canal específico
    if message.channel.id == CANAL_ID:
        tiene_link = "http://" in message.content or "https://" in message.content
        tiene_archivo = len(message.attachments) > 0

        if tiene_link or tiene_archivo:
            try:
                await message.delete()

                # Timeout de 10 minutos
                await message.author.timeout(
                    timedelta(minutes=1),
                    reason="Enviar links o multimedia no permitido"
                )

                await message.channel.send(
                    f"{message.author.mention} recibió timeout por enviar contenido no permitido.",
                    delete_after=5
                )

            except Exception as e:
                print(e)

    await bot.process_commands(message)

bot.run(TOKEN)