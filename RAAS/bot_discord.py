import discord
import os
from dotenv import load_dotenv
from ratio import phrase_to_ratio

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def handleSpecialMessages(message):
    if message.content == "!ping":
        await message.channel.send("pong uwu")
        return True
    if "cr7" in message.content:
        # send gif
        await message.channel.send("https://tenor.com/fr/view/siuu-gif-23749474")
        return True
    if "messi" in message.content:
        await message.channel.send("cr7 > messi")
        return True
    return False

        
@client.event
async def on_message(message):
    if message.author == client.user:
        # add reaction to own message bar chart
        await message.add_reaction("📊")
        # add reaction to own message repeat
        await message.add_reaction("🔁")
        # add reaction to own message heart
        await message.add_reaction("❤️")
        return
    
    print("Received message: ", message.content)
    if await handleSpecialMessages(message):
        return

    ratio_phrase = phrase_to_ratio(message.content)
    if ratio_phrase != "":
        await message.channel.send(ratio_phrase)
    #else:
    #    # post the looser reaction
    #    await message.add_reaction("👎")

@client.event
async def on_message_edit(before,after):
    if after.author == client.user:
        return
    ratio_phrase = phrase_to_ratio(after.content)
    if ratio_phrase != "":
        await after.channel.send(ratio_phrase)


client.run(os.getenv("TOKEN"))

