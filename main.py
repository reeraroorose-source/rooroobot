



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
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Storage
PROTECTED_NICKS: dict[tuple[int, int], str | None] = {}
ROLE_WATCHERS: set[tuple[int, int]] = set()

def giphy(gif_id: str) -> str:
    return f"https://media.giphy.com/media/{gif_id}/giphy.gif"

async def get_changer(guild, target_id, action):
    try:
        async for entry in guild.audit_logs(limit=5, action=action):
            if entry.target.id == target_id:
                return f"{entry.user.mention} (`{entry.user}`)"
    except discord.Forbidden:
        pass
    return "Someone (unknown — missing Audit Log permission)"

EMOTION_ENDPOINTS = {
    "happy": "smile", "sad": "cry", "angry": "kick",
    "surprised": "baka", "shy": "blush", "wave": "wave",
    "hug": "hug", "dance": "dance", "laugh": "laugh", "pat": "pat",
}

GOJO_MOOD_GIFS = {
    "hollow_purple": [giphy("P2olhkZ061vEACZcSG"), giphy("5HJ10dynt13qqF2dnS"),
                      giphy("9Xx1OMQIiA9feabm70"), giphy("8TUMXruYkQ31IVOKKF"),
                      giphy("4sReZVgNmJLaVXp1mW"), giphy("6FMCMhZ1pGMKbPjYB8")],
    "blue":          [giphy("gOnyRejxIPvPUE65HN"), giphy("5AL08VXMfOD48mzqfO"),
                      giphy("iNPNqI81MvDQ4D4n6D"), giphy("TWmkxZCIIP0XdfH92G"),
                      giphy("QSwBid1bso4h5ePFnN")],
    "smirk":         [giphy("nMtKecpxYBRLH5ggYp"), giphy("2FLA1N2ESsT3L03FvK"),
                      giphy("aYQSXVlQXF7hgWvfri"), giphy("YsHVkhLdi9af5JTR93"),
                      giphy("Y9FaRDuM1r55YGRiPg"), giphy("Tl8hfjRo21CXNhSqAQ")],
    "playful":       [giphy("5EYhwZQV9cEvPulZkh"), giphy("N58glDmlxrlqZc99jj"),
                      giphy("xBsGMBcnlRYantuffk"), giphy("MxfS5KAoviW8SbUhV9"),
                      giphy("2R60TLJxKjDiMbyEfq")],
    "honored_one":   [giphy("x16KAEmQ1gTfN8UBZW"), giphy("AgmdBhjPbCBjn6Vuo1"),
                      giphy("p6jg7cOIQ7dUnOSH35"), giphy("orvJf7kwgc2iakssc4"),
                      giphy("WldPA6tzPPSgZDxiJc"), giphy("puSELgYhEXpHLnsblt")],
    "limitless":     [giphy("HARTNiFs9XM7DqfUtc"), giphy("DGsDLr9nyz2LkVgKFs"),
                      giphy("Pt9cmfZNAsBvSPxzNr"), giphy("x16KAEmQ1gTfN8UBZW")],
}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("✅ Slash commands synced")

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    key = (after.guild.id, after.id)

    # Nickname protection
    if key in PROTECTED_NICKS and before.nick != after.nick:
        saved_nick = PROTECTED_NICKS[key]
        try:
            await after.edit(nick=saved_nick, reason="Nickname protection: auto-reverted")
        except discord.Forbidden:
            pass
        changer_name = await get_changer(after.guild, after.id, discord.AuditLogAction.member_update)
        reverted_to = f"`{saved_nick}`" if saved_nick else f"`{after.name}` (your username)"
        changed_to  = f"`{after.nick}`" if after.nick else "`[removed]`"
        embed = discord.Embed(title="🛡️ Nickname Change Detected & Reverted", color=discord.Color.red())
        embed.add_field(name="🖊️ Changed by",   value=changer_name, inline=False)
        embed.add_field(name="❌ Changed to",    value=changed_to,   inline=True)
        embed.add_field(name="✅ Reverted back", value=reverted_to,  inline=True)
        embed.add_field(name="🏠 Server",        value=after.guild.name, inline=False)
        embed.set_footer(text="Your nickname protection is still active.")
        try:
            await after.send(embed=embed)
        except discord.Forbidden:
            pass

    # Role watcher
    if key in ROLE_WATCHERS and set(before.roles) != set(after.roles):
        added   = [r for r in after.roles  if r not in before.roles]
        removed = [r for r in before.roles if r not in after.roles]
        if added or removed:
            changer_name = await get_changer(after.guild, after.id, discord.AuditLogAction.member_role_update)
            embed = discord.Embed(title="👀 Role Change Detected on Your Account", color=discord.Color.orange())
            embed.add_field(name="🖊️ Changed by", value=changer_name, inline=False)
            if added:
                embed.add_field(name="➕ Roles Added",   value=" ".join(r.mention for r in added),   inline=False)
            if removed:
                embed.add_field(name="➖ Roles Removed", value=" ".join(r.mention for r in removed), inline=False)
            embed.add_field(name="🏠 Server", value=after.guild.name, inline=False)
            embed.set_footer(text="Role Watch is active on your account.")
            try:
                await after.send(embed=embed)
            except discord.Forbidden:
                pass

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
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://nekos.best/api/v2/{endpoint}") as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Could not fetch a GIF right now. Try again!")
                return
            data = await resp.json()
    gif_url = data["results"][0]["url"]
    artist_name = data["results"][0].get("artist_name", "Unknown")
    anime_name  = data["results"][0].get("anime_name", "")
    labels = {
        "happy": "😊 Feeling happy!", "sad": "😢 Feeling sad...", "angry": "😠 Feeling angry!",
        "surprised": "😲 Surprised!", "shy": "😳 Feeling shy~", "wave": "👋 Waving!",
        "hug": "🤗 Sending hugs!", "dance": "💃 Let's dance!", "laugh": "😂 Laughing!", "pat": "🫶 Pat pat!",
    }
    embed = discord.Embed(title=labels.get(emotion, emotion.capitalize()), color=discord.Color.blurple())
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
    embed = discord.Embed(color=discord.Color.from_rgb(135, 206, 250))
    embed.set_image(url=random.choice(GOJO_MOOD_GIFS[mood]))
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="protect", description="Lock your nickname so no mod can change it")
async def protect(interaction: discord.Interaction):
    key = (interaction.guild.id, interaction.user.id)
    if key in PROTECTED_NICKS:
        await interaction.response.send_message("🛡️ Already protected. Use `/unprotect` to remove it.", ephemeral=True)
        return
    member = interaction.guild.get_member(interaction.user.id)
    PROTECTED_NICKS[key] = member.nick
    display = f"`{member.nick}`" if member.nick else f"`{member.name}` (your username)"
    await interaction.response.send_message(
        f"🛡️ **Nickname protection ON!** Locked to: {display}\nAny mod change will be reverted & you'll be DM'd.",
        ephemeral=True
    )

@bot.tree.command(name="unprotect", description="Remove nickname protection")
async def unprotect(interaction: discord.Interaction):
    key = (interaction.guild.id, interaction.user.id)
    if key not in PROTECTED_NICKS:
        await interaction.response.send_message("❌ Not protected. Use `/protect` to enable it.", ephemeral=True)
        return
    del PROTECTED_NICKS[key]
    await interaction.response.send_message("🔓 **Nickname protection removed.**", ephemeral=True)

@bot.tree.command(name="watchroles", description="Get a DM alert whenever a mod adds or removes a role from you")
async def watchroles(interaction: discord.Interaction):
    key = (interaction.guild.id, interaction.user.id)
    if key in ROLE_WATCHERS:
        await interaction.response.send_message("👀 Role Watch already active. Use `/unwatchroles` to disable.", ephemeral=True)
        return
    ROLE_WATCHERS.add(key)
    current = ", ".join(f"`{r.name}`" for r in interaction.user.roles if r.name != "@everyone") or "none"
    await interaction.response.send_message(
        f"👀 **Role Watch ON!**\nCurrent roles: {current}\nI'll DM you if any mod touches your roles.",
        ephemeral=True
    )

@bot.tree.command(name="unwatchroles", description="Stop role change alerts")
async def unwatchroles(interaction: discord.Interaction):
    key = (interaction.guild.id, interaction.user.id)
    if key not in ROLE_WATCHERS:
        await interaction.response.send_message("❌ Role Watch is not active. Use `/watchroles` to enable.", ephemeral=True)
        return
    ROLE_WATCHERS.discard(key)
    await interaction.response.send_message("🔕 **Role Watch disabled.**", ephemeral=True)

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: DISCORD_TOKEN not found in .env file!")
        print("👉 Copy .env.example to .env and add your bot token.")
    else:
        bot.run(TOKEN)
