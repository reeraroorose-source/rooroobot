
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

# ───────── REACT SYSTEM ─────────

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

# ───────── GOJO GIFS (NO API NEEDED) ─────────

GOJO_GIFS = {
    "happy": [
        "https://media.tenor.com/W4MzVuCBnXkAAAAC/gojo-satoru.gif",
        "https://media.tenor.com/Gz9F5bHanSkAAAAC/gojo-satoru.gif"
    ],
    "sad": [
        "https://media.tenor.com/oKTq3hBPRCsAAAAC/gojo-satoru.gif"
    ],
    "angry": [
        "https://media.tenor.com/Mk77c62_cSAAAAAC/gojo-satoru-jujutsu.gif"
    ],
    "laugh": [
        "https://media.tenor.com/Y5LKA-A6ZwAAAAAC/gojo-satoru.gif"
    ],
    "fight": [
        "https://media.tenor.com/xPmgTtcqJsoAAAAC/gojo-satoru-jujutsu-kaisen.gif"
    ],
    "cool": [
        "https://media.tenor.com/1_E4Nby1z5QAAAAC/gojo-satoru.gif"
    ],
    "blindfold": [
        "https://media.tenor.com/HtqOX-BpFEQAAAAC/gojo-satoru-gojo.gif"
    ],
    "domain": [
        "https://media.tenor.com/1v5kySGTkbAAAAAC/gojo-satoru-unlimited-void.gif"
    ],
    "blue": [
        "https://media.tenor.com/5QqP0pXKajUAAAAC/gojo-satoru-anime.gif"
    ],
    "red": [
        "https://media.tenor.com/FbcCimSx9KYAAAAC/gojo-satoru-jjk.gif"
    ],
    "purple": [
        "https://media.tenor.com/d3d8GOwNfFQAAAAC/gojo-satoru-jujutsu-kaisen.gif"
    ]
}

# ───────── READY EVENT ─────────

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

# ───────── /REACT COMMAND ─────────

@bot.tree.command(name="react", description="Send an anime reaction GIF")
@app_commands.describe(emotion="Choose your emotion")
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
                await interaction.followup.send("❌ Couldn't fetch GIF!")
                return
            data = await resp.json()

    gif_url = data["results"][0]["url"]

    embed = discord.Embed(title=emotion.capitalize(), color=discord.Color.blurple())
    embed.set_image(url=gif_url)

    await interaction.followup.send(embed=embed)

# ───────── /GOJO COMMAND (NO API) ─────────

@bot.tree.command(name="gojo", description="Gojo reactions")
@app_commands.describe(action="Choose Gojo emotion/action")
@app_commands.choices(action=[
    app_commands.Choice(name="Happy 😊", value="happy"),
    app_commands.Choice(name="Sad 😢", value="sad"),
    app_commands.Choice(name="Angry 😠", value="angry"),
    app_commands.Choice(name="Laugh 😂", value="laugh"),
    app_commands.Choice(name="Fight 🥊", value="fight"),
    app_commands.Choice(name="Cool 😎", value="cool"),
    app_commands.Choice(name="Blindfold 😎", value="blindfold"),
    app_commands.Choice(name="Domain 🌀", value="domain"),
    app_commands.Choice(name="Blue 💙", value="blue"),
    app_commands.Choice(name="Red 🔴", value="red"),
    app_commands.Choice(name="Purple 🟣", value="purple"),
])
async def gojo(interaction: discord.Interaction, action: str):
    gif_list = GOJO_GIFS.get(action)

    if not gif_list:
        await interaction.response.send_message("❌ No GIF found!")
        return

    gif_url = random.choice(gif_list)

    embed = discord.Embed(
        title=f"Gojo — {action.capitalize()}",
        color=discord.Color.from_rgb(135, 206, 250)
    )
    embed.set_image(url=gif_url)

    await interaction.response.send_message(embed=embed)

# ───────── RUN ─────────

if __name__ == "__main__":
    if not TOKEN:
        print("❌ DISCORD_TOKEN missing!")
    else:
        bot.run(TOKEN)
