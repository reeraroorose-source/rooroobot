
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

# ── EMOTION API MAPPING ──
EMOTION_ENDPOINTS = {
    "happy": "smile",
    "sad": "cry",
    "angry": "kick",
    "surprised": "baka",
    "shy": "blush",
    "wave": "wave",
    "hug": "hug",
    "dance": "dance",
    "laugh": "laugh",
    "pat": "pat",
}

# ── BACKUP GIFS (IMPORTANT FIX) ──
FALLBACK_GIFS = [
    "https://media.tenor.com/0AVbKGY_MxMAAAAC/anime-smile.gif",
    "https://media.tenor.com/W6Yc8M4z2q8AAAAC/anime-hug.gif",
    "https://media.tenor.com/2roX3uxz_68AAAAC/anime-laugh.gif",
    "https://media.tenor.com/Qr6d7X9EwSMAAAAC/anime-wave.gif",
]

# ── GOJO GIFS ──
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
]

# ── READY ──
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

# ── REACT COMMAND (FIXED) ──
@bot.tree.command(name="react", description="Anime reaction GIF")
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

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception("API failed")

                data = await resp.json()
                gif_url = data["results"][0]["url"]

    except:
        # 🔥 FALLBACK FIX
        gif_url = random.choice(FALLBACK_GIFS)

    embed = discord.Embed(
        title=f"{emotion.capitalize()} reaction",
        color=discord.Color.blurple()
    )
    embed.set_image(url=gif_url)

    await interaction.followup.send(embed=embed)

# ── GOJO COMMAND ──
@bot.tree.command(name="gojo", description="Gojo reaction GIF")
async def gojo(interaction: discord.Interaction):
    gif_url = random.choice(GOJO_GIFS)

    embed = discord.Embed(
        title="Gojo Satoru 🔥",
        color=discord.Color.blue()
    )
    embed.set_image(url=gif_url)

    await interaction.response.send_message(embed=embed)

# ── RUN ──
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN missing")
