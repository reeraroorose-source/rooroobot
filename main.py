

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


def giphy(gif_id: str) -> str:
    return f"https://media.giphy.com/media/{gif_id}/giphy.gif"


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
    "hollow_purple": [
        giphy("P2olhkZ061vEACZcSG"),
        giphy("5HJ10dynt13qqF2dnS"),
        giphy("9Xx1OMQIiA9feabm70"),
        giphy("8TUMXruYkQ31IVOKKF"),
        giphy("4sReZVgNmJLaVXp1mW"),
        giphy("6FMCMhZ1pGMKbPjYB8"),
    ],
    "blue": [
        giphy("gOnyRejxIPvPUE65HN"),
        giphy("5AL08VXMfOD48mzqfO"),
        giphy("iNPNqI81MvDQ4D4n6D"),
        giphy("TWmkxZCIIP0XdfH92G"),
        giphy("QSwBid1bso4h5ePFnN"),
    ],
    "smirk": [
        giphy("nMtKecpxYBRLH5ggYp"),
        giphy("2FLA1N2ESsT3L03FvK"),
        giphy("aYQSXVlQXF7hgWvfri"),
        giphy("YsHVkhLdi9af5JTR93"),
        giphy("Y9FaRDuM1r55YGRiPg"),
        giphy("Tl8hfjRo21CXNhSqAQ"),
    ],
    "playful": [
        giphy("5EYhwZQV9cEvPulZkh"),
        giphy("N58glDmlxrlqZc99jj"),
        giphy("xBsGMBcnlRYantuffk"),
        giphy("MxfS5KAoviW8SbUhV9"),
        giphy("2R60TLJxKjDiMbyEfq"),
    ],
    "honored_one": [
        giphy("x16KAEmQ1gTfN8UBZW"),
        giphy("AgmdBhjPbCBjn6Vuo1"),
        giphy("p6jg7cOIQ7dUnOSH35"),
        giphy("orvJf7kwgc2iakssc4"),
        giphy("WldPA6tzPPSgZDxiJc"),
        giphy("puSELgYhEXpHLnsblt"),
    ],
    "limitless": [
        giphy("HARTNiFs9XM7DqfUtc"),
        giphy("DGsDLr9nyz2LkVgKFs"),
        giphy("Pt9cmfZNAsBvSPxzNr"),
        giphy("HARTNiFs9XM7DqfUtc"),
        giphy("x16KAEmQ1gTfN8UBZW"),
    ],
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

    embed = discord.Embed(
        title=emotion_labels.get(emotion, emotion.capitalize()),
        color=discord.Color.blurple()
    )
    embed.set_image(url=gif_url)
    embed.set_footer(text=f"🎨 {artist_name}" + (f"  •  🎬 {anime_name}" if anime_name else ""))
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="gojo", description="Send a Gojo Satoru GIF 🥷")
@app_commands.describe(mood="Choose Gojo's mood")
@app_commands.choices(mood=[
    app_commands.Choice(name="Hollow Purple 💜", value="hollow_purple"),
    app_commands.Choice(name="Blue ⚡",          value="blue"),
    app_commands.Choice(name="Smirk 😏",         value="smirk"),
    app_commands.Choice(name="Playful 😄",        value="playful"),
    app_commands.Choice(name="Honored One 👑",    value="honored_one"),
    app_commands.Choice(name="Limitless ∞",       value="limitless"),
])
async def gojo(interaction: discord.Interaction, mood: str):
    gif_url = random.choice(GOJO_MOOD_GIFS[mood])
    embed = discord.Embed(color=discord.Color.from_rgb(135, 206, 250))
    embed.set_image(url=gif_url)
    await interaction.response.send_message(embed=embed)


if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: DISCORD_TOKEN not found in .env file!")
        print("👉 Copy .env.example to .env and add your bot token.")
    else:
        bot.run(TOKEN)
