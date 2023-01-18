import discord
import os
from dotenv import load_dotenv
from ratio import phrase_to_ratio

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    ratio_phrase = phrase_to_ratio(message.content)
    if ratio_phrase != "":
        await message.channel.send(ratio_phrase)


client.run(os.getenv("TOKEN"))

