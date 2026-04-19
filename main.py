


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
GOJO_MOOD_GIFS = {
    "cool": [
        "https://media.tenor.com/W4MzVuCBnXkAAAAC/gojo-satoru-jujutsu-kaisen.gif",
        "https://media.tenor.com/Y5LKA-A6ZwAAAAAC/gojo-satoru.gif",
        "https://media.tenor.com/HtqOX-BpFEQAAAAC/gojo-satoru-gojo.gif",
        "https://media.tenor.com/FbcCimSx9KYAAAAC/gojo-satoru-jjk.gif",
    ],
    "smug": [
        "https://media.tenor.com/1_E4Nby1z5QAAAAC/gojo-satoru.gif",
        "https://media.tenor.com/Gz9F5bHanSkAAAAC/gojo-satoru.gif",
        "https://media.tenor.com/oKTq3hBPRCsAAAAC/gojo-satoru.gif",
        "https://media.tenor.com/5QqP0pXKajUAAAAC/gojo-satoru-anime.gif",
    ],
    "serious": [
        "https://media.tenor.com/xPmgTtcqJsoAAAAC/gojo-satoru-jujutsu-kaisen.gif",
        "https://media.tenor.com/d3d8GOwNfFQAAAAC/gojo-satoru-jujutsu-kaisen.gif",
        "https://media.tenor.com/JK9XtGQcTpYAAAAC/gojo-satoru-jujutsu-kaisen.gif",
        "https://media.tenor.com/Mk77c62_cSAAAAAC/gojo-satoru-jujutsu.gif",
    ],
    "power": [
        "https://media.tenor.com/1v5kySGTkbAAAAAC/gojo-satoru-unlimited-void.gif",
        "https://media.tenor.com/9j9X2Q7P1NAAAAAC/gojo.gif",
        "https://media.tenor.com/oCJCGLqEMKsAAAAC/jujutsu-kaisen-gojo-satoru.gif",
        "https://media.tenor.com/HtqOX-BpFEQAAAAC/gojo-satoru-gojo.gif",
    ],
    "happy": [
        "https://media.tenor.com/Gz9F5bHanSkAAAAC/gojo-satoru.gif",
        "https://media.tenor.com/5QqP0pXKajUAAAAC/gojo-satoru-anime.gif",
        "https://media.tenor.com/1_E4Nby1z5QAAAAC/gojo-satoru.gif",
        "https://media.tenor.com/oKTq3hBPRCsAAAAC/gojo-satoru.gif",
    ],
    "angry": [
        "https://media.tenor.com/xPmgTtcqJsoAAAAC/gojo-satoru-jujutsu-kaisen.gif",
        "https://media.tenor.com/9j9X2Q7P1NAAAAAC/gojo.gif",
        "https://media.tenor.com/Mk77c62_cSAAAAAC/gojo-satoru-jujutsu.gif",
        "https://media.tenor.com/d3d8GOwNfFQAAAAC/gojo-satoru-jujutsu-kaisen.gif",
    ],
}
GOJO_MOOD_LABELS = {
    "cool":    ("😎 Too cool for you.", "Gojo Satoru 😎"),
    "smug":    ("😏 You can't even touch me.", "Gojo Satoru 😏"),
    "serious": ("🥷 Don't make me get serious.", "Gojo Satoru 🥷"),
    "power":   ("⚡ Infinity — you can't hit me.", "Gojo Satoru ⚡"),
    "happy":   ("😊 Even the strongest can smile.", "Gojo Satoru 😊"),
    "angry":   ("😤 You just woke up the wrong guy.", "Gojo Satoru 😤"),
}
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("✅ Slash commands synced")
@bot.tree.command(name="react", description="Send an anime reaction GIF based on your emotion")
@app_commands.describe(emotion="Choose the emotion you want to express")
@app_commands.choices(emotion=[
    app_commands.Choice(name="Happy 😊",      value="happy"),
    app_commands.Choice(name="Sad 😢",        value="sad"),
    app_commands.Choice(name="Angry 😠",      value="angry"),
    app_commands.Choice(name="Surprised 😲",  value="surprised"),
    app_commands.Choice(name="Shy 😳",        value="shy"),
    app_commands.Choice(name="Wave 👋",       value="wave"),
    app_commands.Choice(name="Hug 🤗",        value="hug"),
    app_commands.Choice(name="Dance 💃",      value="dance"),
    app_commands.Choice(name="Laugh 😂",      value="laugh"),
    app_commands.Choice(name="Pat 🫶",        value="pat"),
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
    artist_name = data["results"][0].get("artist_name", "Unknown")
    anime_name  = data["results"][0].get("anime_name", "")
    emotion_labels = {
        "happy": "😊 Feeling happy!", "sad": "😢 Feeling sad...",
        "angry": "😠 Feeling angry!", "surprised": "😲 Surprised!",
        "shy": "😳 Feeling shy~", "wave": "👋 Waving!",
        "hug": "🤗 Sending hugs!", "dance": "💃 Let's dance!",
        "laugh": "😂 Laughing!", "pat": "🫶 Pat pat!",
    }
    embed = discord.Embed(title=emotion_labels.get(emotion, emotion.capitalize()), color=discord.Color.blurple())
    embed.set_image(url=gif_url)
    embed.set_footer(text=f"🎨 {artist_name}" + (f"  •  🎬 {anime_name}" if anime_name else ""))
    await interaction.followup.send(embed=embed)
@bot.tree.command(name="gojo", description="Send a Gojo Satoru GIF based on his mood 🥷")
@app_commands.describe(mood="Choose Gojo's mood")
@app_commands.choices(mood=[
    app_commands.Choice(name="Cool 😎",    value="cool"),
    app_commands.Choice(name="Smug 😏",    value="smug"),
    app_commands.Choice(name="Serious 🥷", value="serious"),
    app_commands.Choice(name="Power ⚡",   value="power"),
    app_commands.Choice(name="Happy 😊",   value="happy"),
    app_commands.Choice(name="Angry 😤",   value="angry"),
])
async def gojo(interaction: discord.Interaction, mood: str):
    gif_url = random.choice(GOJO_MOOD_GIFS[mood])
    quote, title = GOJO_MOOD_LABELS[mood]
    embed = discord.Embed(title=title, description=f"*\"{quote}\"*", color=discord.Color.from_rgb(135, 206, 250))
    embed.set_image(url=gif_url)
    embed.set_footer(text="Jujutsu Kaisen  •  Gojo Satoru")
    await interaction.response.send_message(embed=embed)
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: DISCORD_TOKEN not found in .env file!")
        print("👉 Copy .env.example to .env and add your bot token.")
    else:
        bot.run(TOKEN)
