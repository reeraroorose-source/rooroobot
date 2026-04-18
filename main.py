
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

# ───────── GOJO SYSTEM ─────────

GOJO_ACTIONS = {
    "happy": "gojo satoru happy",
    "sad": "gojo satoru sad",
    "angry": "gojo satoru angry",
    "laugh": "gojo satoru laughing",
    "fight": "gojo satoru fight",
    "cool": "gojo satoru cool",
    "blindfold": "gojo satoru blindfold",
    "domain": "gojo domain expansion",
    "blue": "gojo blue technique",
    "red": "gojo red technique",
    "purple": "gojo hollow purple"
}

# ───────── READY EVENT ─────────

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")
    print("✅ Slash commands synced")

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

    embed = discord.Embed(
        title=f"{emotion.capitalize()}",
        color=discord.Color.blurple()
    )
    embed.set_image(url=gif_url)

    await interaction.followup.send(embed=embed)

# ───────── /GOJO COMMAND ─────────

@bot.tree.command(name="gojo", description="Gojo reactions & abilities")
@app_commands.describe(action="Choose Gojo action")
@app_commands.choices(action=[
    app_commands.Choice(name="Happy 😊", value="happy"),
    app_commands.Choice(name="Sad 😢", value="sad"),
    app_commands.Choice(name="Angry 😠", value="angry"),
    app_commands.Choice(name="Laugh 😂", value="laugh"),
    app_commands.Choice(name="Fight 🥊", value="fight"),
    app_commands.Choice(name="Cool 😎", value="cool"),
    app_commands.Choice(name="Blindfold 😎", value="blindfold"),
    app_commands.Choice(name="Domain Expansion 🌀", value="domain"),
    app_commands.Choice(name="Blue 💙", value="blue"),
    app_commands.Choice(name="Red 🔴", value="red"),
    app_commands.Choice(name="Hollow Purple 🟣", value="purple"),
])
async def gojo(interaction: discord.Interaction, action: str):
    await interaction.response.defer()

    query = GOJO_ACTIONS.get(action, "gojo satoru")
    url = f"https://tenor.googleapis.com/v2/search?q={query}&key=LIVDSRZULELA&limit=10"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Couldn't fetch Gojo GIF!")
                return
            data = await resp.json()

    results = data.get("results", [])
    if not results:
        await interaction.followup.send("❌ No GIF found!")
        return

    gif = random.choice(results)["media_formats"]["gif"]["url"]

    embed = discord.Embed(
        title=f"Gojo — {action.capitalize()}",
        color=discord.Color.from_rgb(135, 206, 250)
    )
    embed.set_image(url=gif)

    await interaction.followup.send(embed=embed)

# ───────── RUN BOT ─────────

if __name__ == "__main__":
    if not TOKEN:
        print("❌ DISCORD_TOKEN missing!")
    else:
        bot.run(TOKEN)
