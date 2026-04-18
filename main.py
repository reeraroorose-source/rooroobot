import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import os
import random
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

EMOTION_ENDPOINTS = {
    "happy":     "smile",
    "sad":       "cry",
    "angry":     "kick",
    "surprised": "baka",
    "shy":       "blush",
    "wave":      "wave",
    "hug":       "hug",
    "dance":     "dance",
    "laugh":     "laugh",
    "pat":       "pat",
}

GOJO_GIFS = [
    "https://media.tenor.com/W4MzVuCBnXkAAAAC/gojo-satoru-jujutsu-kaisen.gif",
    "https://media.tenor.com/1_E4Nby1z5QAAAAC/gojo-satoru.gif",
    "https://media.tenor.com/xPmgTtcqJsoAAAAC/gojo-satoru-jujutsu-kaisen.gif",
    "https://media.tenor.com/d3d8GOwNfFQAAAAC/gojo-satoru-jujutsu-kaisen.gif",
    "https://media.tenor.com/9j9X2Q7P1NAAAAAC/gojo.gif",
    "https://media.tenor.com/Gz9F5bHanSkAAAAC/gojo-satoru.gif",
    "https://media.tenor.com/Y5LKA-A6ZwAAAAAC/gojo-satoru.gif",
    "https://media.tenor.com/HtqOX-BpFEQAAAAC/gojo-satoru-gojo.gif",
    "https://media.tenor.com/oCJCGLqEMKsAAAAC/jujutsu-kaisen-gojo-satoru.gif",
    "https://media.tenor.com/oKTq3hBPRCsAAAAC/gojo-satoru.gif",
    "https://media.tenor.com/Mk77c62_cSAAAAAC/gojo-satoru-jujutsu.gif",
    "https://media.tenor.com/1v5kySGTkbAAAAAC/gojo-satoru-unlimited-void.gif",
    "https://media.tenor.com/5QqP0pXKajUAAAAC/gojo-satoru-anime.gif",
    "https://media.tenor.com/JK9XtGQcTpYAAAAC/gojo-satoru-jujutsu-kaisen.gif",
    "https://media.tenor.com/FbcCimSx9KYAAAAC/gojo-satoru-jjk.gif",
]

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("✅ Slash commands synced")

@bot.tree.command(name="react", description="Send an anime reaction GIF based on your emotion")
@app_commands.describe(emotion="Choose the emotion you want to express")
@app_commands.choices(emotion=[
    app_commands.Choice(name="Happy 😊", value="happy"),
    app_commands.Choice(name="Sad 😢", value="sad"),
    app_commands.Choice(name="Angry 😠", value="angry"),
    app_commands.Choice(name="Surprised 😲", value="surprised"),
    app_commands.Choice(name="Shy 😳", value="shy"),
    app_commands.Choice(name="Wave 👋", value="wave"),
    app_commands.Choice(name="Hug 🤗", value="hug"),
    app_commands.Choice(name="Dance 💃", value="dance"),
    app_commands.Choice(name="Laugh 😂", value="laugh"),
    app_commands.Choice(name="Pat 🫶", value="pat"),
])
async def react(interaction: discord.Interaction, emotion: str):
    await interaction.response.defer()

    endpoint = EMOTION_ENDPOINTS.get(emotion, "smile")
    url = f"https://nekos.best/api/v2/{endpoint}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Could not fetch a GIF right now. Try again!")
                return
            data = await resp.json()

    gif_url = data["results"][0]["url"]
    embed = discord.Embed(title=emotion.capitalize(), color=discord.Color.blurple())
    embed.set_image(url=gif_url)

    await interaction.followup.send(embed=embed)

@bot.tree.command(name="gojo", description="Send a random Gojo Satoru reaction GIF")
async def gojo(interaction: discord.Interaction):
    gif_url = random.choice(GOJO_GIFS)
    embed = discord.Embed(title="Gojo Satoru", color=discord.Color.blue())
    embed.set_image(url=gif_url)
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    if not TOKEN:
        print("❌ DISCORD_TOKEN missing!")
    else:
        bot.run(TOKEN)
