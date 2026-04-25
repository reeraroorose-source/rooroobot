






import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import os
import logging
from anime_bot import setup_anime_commands
from react_bot import setup_react_commands
from gojo_bot import setup_gojo_commands

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("rooHackBot")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ── Helpers ─────────────────────────────────────────────────────────────────

def progress_bar(p):
    return "█" * (p // 10) + "-" * (10 - p // 10)

def fake_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

# ── Static data ──────────────────────────────────────────────────────────────

ROASTS = [
    "has the personality of a wet paper bag.",
    "is the reason shampoo has instructions.",
    "could start an argument in an empty room.",
    "has a face made for podcasting.",
    "is living proof that evolution can go in reverse.",
    "brings so much nothing to the table, the table left.",
    "is like a cloud — when they disappear, it's a beautiful day.",
    "once stared at a juice box because it said 'concentrate'.",
    "is the human equivalent of a participation trophy.",
    "has never had an original thought and never will.",
]

EXPOSE_FACTS = [
    "still sleeps with a night light. 🌙",
    "googles how to spell 'wednesday' every single time. 🤫",
    "has sent a text to the wrong person and never recovered. 😬",
    "skips the gym but tells people they 'just got back from the gym'. 💪",
    "laughs at their own jokes before finishing them. 😂",
    "has eaten cereal for dinner more than 3 times this week. 🥣",
    "talks to their pets like they're in a business meeting. 🐾",
    "has a folder on their phone called 'do not open'. 👀",
    "rewatches the same show for the 6th time instead of being productive. 📺",
    "mutes their mic on calls and complains about people. 🎙️",
]

BROWSER_HISTORIES = [
    "- 'how to look busy at work'\n- 'do fish have feelings'\n- 'can you eat playdough'\n- minecraft tutorial 2009",
    "- 'is cereal a soup'\n- 'why do I exist'\n- 'free robux'\n- 47 tabs of Wikipedia",
    "- 'how to delete browser history'\n- 'am I a main character'\n- 'chicken dance origin'\n- 3am meme compilations",
    "- 'signs you're a genius'\n- 'why is my cat judging me'\n- 'how to be cool'\n- discount socks",
    "- 'how to fake being sick'\n- 'loudest animal on earth'\n- 'is a hotdog a sandwich'\n- 6 hours of lo-fi beats",
]

IQ_COMMENTS = [
    (range(0, 20),    "Congratulations — you've achieved something previously thought impossible."),
    (range(20, 40),   "Scientists are baffled. This breaks several laws of physics."),
    (range(40, 60),   "You might want to sit down for this one."),
    (range(60, 75),   "Room-temperature IQ. Literally."),
    (range(75, 90),   "Could be worse. Could be better. It's not better."),
    (range(90, 105),  "Perfectly average. Bold of you to be here."),
    (range(105, 120), "Smarter than most, but let's not get cocky."),
    (range(120, 140), "Impressive. You're still not right though."),
    (range(140, 160), "Big brain. Shame about everything else."),
    (range(160, 201), "Off the charts. The charts are embarrassed."),
]

SUS_VERDICTS = [
    "EXTREMELY SUS 🔴 — was standing on the body doing nothing",
    "kinda sus 🟡 — faked a task in electrical",
    "pretty clean 🟢 — has a solid alibi but we're watching them",
    "MEGA SUS 🔴🔴 — vented in front of 3 witnesses and blamed the cat",
    "not sus at all 🟢 — did all tasks, reported the body, and made snacks",
    "sus beyond all reason 🔴 — literally just confessed and still denying it",
    "sus-pending judgement 🟡 — keeps saying 'I was in medbay' but medbay was on fire",
]

BATTLE_STATS   = ["Strength", "Speed", "Big Brain", "Luck", "Chaos Energy", "Audacity"]
BATTLE_ENDINGS = [
    "delivered a devastating roast so powerful the server lagged.",
    "pulled out a sock and won inexplicably.",
    "just started crying and somehow it worked.",
    "tripped, fell, and accidentally won.",
    "did nothing and still came out on top. Respect.",
    "deployed the ancient technique of 'talking too much'.",
    "opened their camera and the other person immediately forfeited.",
]

RPS_BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
RPS_EMOJI = {"rock": "🪨", "scissors": "✂️", "paper": "📄"}

POLL_BUTTON_STYLES = [
    discord.ButtonStyle.primary,
    discord.ButtonStyle.success,
    discord.ButtonStyle.danger,
    discord.ButtonStyle.secondary,
]

TRUTH_QUESTIONS = [
    "What's the most embarrassing thing you've done in public?",
    "What's something you've lied about that nobody knows?",
    "Who was your first crush and do you regret it?",
    "What's the pettiest thing you've ever done?",
    "Have you ever blamed someone else for something you did?",
    "What's the most childish thing you still do?",
    "What's something you pretend to like but actually hate?",
    "What's the longest you've gone without showering?",
    "Have you ever read someone's messages without them knowing?",
    "What's your most embarrassing late-night purchase?",
    "What's something you're irrationally afraid of?",
    "Have you ever walked into a room and completely forgotten why?",
    "What's the most ridiculous thing you've ever googled?",
    "Have you ever pretended to be busy to avoid someone?",
    "What's the weirdest dream you've had about someone in this chat?",
]

DARE_CHALLENGES = [
    "Send the last photo in your camera roll (no deletions).",
    "Type only in ALL CAPS for the next 5 messages.",
    "Change your nickname to 'Big Brain Energy' for 10 minutes.",
    "Send a voice message doing your best villain laugh.",
    "Write a love poem for the person above you — right now.",
    "Confess your most embarrassing Discord moment.",
    "Send the most unhinged GIF you can find in 30 seconds.",
    "Type 'I eat soup with a fork' in the main chat.",
    "Do your best impression of a medieval knight in the next message.",
    "Send a message pretending to be a disappointed parent.",
]

# ── Views ────────────────────────────────────────────────────────────────────

class RPSView(discord.ui.View):
    def __init__(self, challenger: discord.User, opponent: discord.User):
        super().__init__(timeout=60)
        self.challenger = challenger
        self.opponent   = opponent
        self.choices    = {}

    async def resolve(self, interaction: discord.Interaction):
        c1, c2 = self.choices[self.challenger.id], self.choices[self.opponent.id]
        e1, e2 = RPS_EMOJI[c1], RPS_EMOJI[c2]
        if c1 == c2:
            result = f"🤝 **It's a tie!** Both picked {e1} {c1}."
        elif RPS_BEATS[c1] == c2:
            result = f"🏆 **{self.challenger.display_name} wins!** {e1} {c1} beats {e2} {c2}."
        else:
            result = f"🏆 **{self.opponent.display_name} wins!** {e2} {c2} beats {e1} {c1}."
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(
            content=(
                f"⚔️ {self.challenger.mention} vs {self.opponent.mention}\n\n"
                f"{self.challenger.display_name} chose {e1} **{c1}**\n"
                f"{self.opponent.display_name} chose {e2} **{c2}**\n\n"
                f"{result}"
            ),
            view=self,
        )

    async def handle_choice(self, interaction: discord.Interaction, choice: str):
        if interaction.user.id not in (self.challenger.id, self.opponent.id):
            await interaction.response.send_message("❌ This isn't your game!", ephemeral=True)
            return
        if interaction.user.id in self.choices:
            await interaction.response.send_message("✋ You already locked in your choice!", ephemeral=True)
            return
        self.choices[interaction.user.id] = choice
        await interaction.response.send_message(
            f"✅ Locked in: {RPS_EMOJI[choice]} **{choice}** — waiting for the other player...",
            ephemeral=True,
        )
        if len(self.choices) == 2:
            await self.resolve(interaction)

    @discord.ui.button(label="🪨 Rock",     style=discord.ButtonStyle.secondary)
    async def rock    (self, i, b): await self.handle_choice(i, "rock")
    @discord.ui.button(label="📄 Paper",    style=discord.ButtonStyle.secondary)
    async def paper   (self, i, b): await self.handle_choice(i, "paper")
    @discord.ui.button(label="✂️ Scissors", style=discord.ButtonStyle.secondary)
    async def scissors(self, i, b): await self.handle_choice(i, "scissors")


class PollView(discord.ui.View):
    def __init__(self, creator: discord.User, question: str, options: list):
        super().__init__(timeout=None)
        self.creator  = creator
        self.question = question
        self.options  = options
        self.votes: dict[int, int] = {}

        for i, option in enumerate(options):
            btn = discord.ui.Button(
                label=option,
                style=POLL_BUTTON_STYLES[i % len(POLL_BUTTON_STYLES)],
                custom_id=f"poll_option_{i}",
            )
            btn.callback = self.make_callback(i)
            self.add_item(btn)

        end_btn = discord.ui.Button(
            label="🔒 End Poll",
            style=discord.ButtonStyle.secondary,
            custom_id="poll_end",
            row=1,
        )
        end_btn.callback = self.end_poll
        self.add_item(end_btn)

    def make_callback(self, index: int):
        async def callback(interaction: discord.Interaction):
            prev = self.votes.get(interaction.user.id)
            if prev == index:
                await interaction.response.send_message(
                    f"✋ You already voted for **{self.options[index]}**!", ephemeral=True
                )
                return
            self.votes[interaction.user.id] = index
            msg = (
                f"✅ Voted for **{self.options[index]}**!"
                if prev is None else
                f"🔄 Changed vote to **{self.options[index]}**!"
            )
            await interaction.response.send_message(msg, ephemeral=True)
            await interaction.message.edit(content=self.render(), view=self)
        return callback

    async def end_poll(self, interaction: discord.Interaction):
        if interaction.user.id != self.creator.id:
            await interaction.response.send_message("❌ Only the poll creator can end this poll.", ephemeral=True)
            return
        for item in self.children:
            item.disabled = True
        counts = [0] * len(self.options)
        for opt_idx in self.votes.values():
            counts[opt_idx] += 1
        total      = sum(counts)
        winner_idx = counts.index(max(counts)) if total > 0 else None
        lines = []
        for i, (opt, count) in enumerate(zip(self.options, counts)):
            pct   = int((count / total) * 100) if total > 0 else 0
            bar   = "█" * (pct // 10) + "░" * (10 - pct // 10)
            crown = " 👑" if i == winner_idx and total > 0 else ""
            lines.append(f"**{opt}**{crown}\n`{bar}` {count} vote{'s' if count != 1 else ''} ({pct}%)")
        await interaction.response.edit_message(
            content=f"🔒 **POLL CLOSED — {self.question}**\n\n" + "\n\n".join(lines) + f"\n\n_Total votes: {total}_",
            view=self,
        )

    def render(self):
        counts = [0] * len(self.options)
        for opt_idx in self.votes.values():
            counts[opt_idx] += 1
        total = sum(counts)
        lines = []
        for opt, count in zip(self.options, counts):
            pct = int((count / total) * 100) if total > 0 else 0
            bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
            lines.append(f"**{opt}** — {count} vote{'s' if count != 1 else ''} ({pct}%)\n`{bar}`")
        return (
            f"📊 **{self.question}**\n_by {self.creator.display_name}_\n\n"
            + "\n\n".join(lines)
            + f"\n\n_Total votes: {total} — Click to vote! You can change your vote anytime._"
        )


class ConfessionModal(discord.ui.Modal, title="💌 Anonymous Confession"):
    confession = discord.ui.TextInput(
        label="Your confession",
        style=discord.TextStyle.paragraph,
        placeholder="Type your confession here... nobody will know it was you.",
        min_length=1,
        max_length=500,
    )

    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ Confession sent anonymously!", ephemeral=True)
        await self.channel.send(f"💌 **Anonymous Confession:**\n> {self.confession.value}")


class ConfessView(discord.ui.View):
    def __init__(self, channel):
        super().__init__(timeout=None)
        self.channel = channel

    @discord.ui.button(label="💌 Submit a Confession", style=discord.ButtonStyle.primary)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ConfessionModal(self.channel))


class TruthModal(discord.ui.Modal):
    answer = discord.ui.TextInput(
        label="Your honest answer",
        style=discord.TextStyle.paragraph,
        placeholder="Be honest... everyone's watching. 👀",
        min_length=1,
        max_length=500,
    )

    def __init__(self, question: str, asker: discord.User, channel):
        super().__init__(title="🎯 Truth")
        self.question = question
        self.asker    = asker
        self.channel  = channel
        self.answer.placeholder = question[:100]

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ Answer posted!", ephemeral=True)
        await self.channel.send(
            f"🎯 **Truth** — {self.asker.mention} asked {interaction.user.mention}:\n"
            f"> {self.question}\n\n"
            f"💬 **{interaction.user.display_name}'s answer:**\n> {self.answer.value}"
        )


class TruthView(discord.ui.View):
    def __init__(self, target: discord.User, asker: discord.User, question: str, channel):
        super().__init__(timeout=120)
        self.target   = target
        self.asker    = asker
        self.question = question
        self.channel  = channel

    @discord.ui.button(label="🎯 Answer the question", style=discord.ButtonStyle.danger)
    async def answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message(
                f"❌ This question is for {self.target.display_name}, not you!", ephemeral=True
            )
            return
        button.disabled = True
        button.label    = "✅ Answered"
        await interaction.message.edit(view=self)
        await interaction.response.send_modal(TruthModal(self.question, self.asker, self.channel))


class DareView(discord.ui.View):
    def __init__(self, target: discord.User, dare: str):
        super().__init__(timeout=120)
        self.target = target
        self.dare   = dare

    @discord.ui.button(label="✅ Done", style=discord.ButtonStyle.success)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("❌ This dare isn't for you!", ephemeral=True)
            return
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(
            content=f"{interaction.message.content}\n\n✅ **{self.target.display_name} completed the dare!**",
            view=self,
        )
        await interaction.response.send_message("💪 Respect!", ephemeral=True)

    @discord.ui.button(label="🐔 Chicken out", style=discord.ButtonStyle.danger)
    async def chicken(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("❌ This dare isn't for you!", ephemeral=True)
            return
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(
            content=f"{interaction.message.content}\n\n🐔 **{self.target.display_name} chickened out. Classic.**",
            view=self,
        )
        await interaction.response.send_message("😂 As expected.", ephemeral=True)

# ── Error handler ─────────────────────────────────────────────────────────────

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    log.error("Command error in /%s: %s", interaction.command and interaction.command.name, error, exc_info=error)
    msg = "⚠️ Something went wrong. Please try again in a moment."
    try:
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)
    except Exception:
        pass

# ── Startup — only register & sync commands once ──────────────────────────────

@bot.event
async def on_ready():
    log.info("Logged in as %s (ID: %s)", bot.user, bot.user.id)


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if not OWNER_ID or after.id != OWNER_ID:
        return
    if before.nick == after.nick:
        return

    original = before.nick
    changed_to = after.nick
    guild = after.guild

    # Revert the nickname immediately
    try:
        await after.edit(nick=original, reason="Auto-revert: unauthorized nickname change")
        log.info("Reverted nickname change for owner in %s", guild.name)
    except discord.Forbidden:
        log.warning("Missing permission to revert nickname in %s", guild.name)
    except Exception as e:
        log.error("Failed to revert nickname in %s: %s", guild.name, e)

    # Find who changed it via audit log
    culprit = None
    await asyncio.sleep(1)  # brief wait for audit log to update
    try:
        async for entry in guild.audit_logs(action=discord.AuditLogAction.member_update, limit=10):
            if entry.target.id == OWNER_ID:
                culprit = entry.user
                break
    except discord.Forbidden:
        log.warning("No audit log access in %s", guild.name)
    except Exception as e:
        log.error("Audit log error in %s: %s", guild.name, e)

    # DM the owner
    try:
        owner_user = await bot.fetch_user(OWNER_ID)
        culprit_str = f"**{culprit.display_name}** (`{culprit}`)" if culprit else "someone (no audit log access)"
        before_str = f"`{original}`" if original else "_no nickname_"
        after_str  = f"`{changed_to}`" if changed_to else "_no nickname_"
        await owner_user.send(
            f"🛡️ **Nickname Protection — {guild.name}**\n\n"
            f"{culprit_str} changed your nickname\n"
            f"From: {before_str} → To: {after_str}\n\n"
            f"✅ Reverted automatically."
        )
    except Exception as e:
        log.error("Could not DM owner: %s", e)

@bot.event
async def setup_hook_done():
    pass

async def setup_hook():
    setup_anime_commands(bot.tree)
    setup_react_commands(bot.tree)
    setup_gojo_commands(bot.tree)
    await bot.tree.sync()
    log.info("Slash commands synced globally.")

bot.setup_hook = setup_hook

# ── Slash commands ────────────────────────────────────────────────────────────

_EVERYWHERE = dict(
    guilds=True, users=True,
)
_CTX = dict(
    guilds=True, dms=True, private_channels=True,
)

def _decorate(cmd):
    cmd = app_commands.allowed_installs(**_EVERYWHERE)(cmd)
    cmd = app_commands.allowed_contexts(**_CTX)(cmd)
    return cmd


@bot.tree.command(name="hack", description="Fake-hack a user with a dramatic hacking sequence")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def hack(interaction: discord.Interaction, member: discord.User):
    await interaction.response.send_message(f"🕵️ Hacking {member.mention}...")
    await asyncio.sleep(1)
    await interaction.followup.send(f"🌐 IP found: {fake_ip()}")
    for i in range(0, 101, 20):
        await interaction.followup.send(f"[{progress_bar(i)}] {i}%")
        await asyncio.sleep(1)
    await interaction.followup.send("📂 Found: embarrassing photos")
    await asyncio.sleep(1)
    await interaction.followup.send(f"💥 Hack complete!\n{member.mention} eats snacks at midnight 😭")


@bot.tree.command(name="roast", description="Roast a user")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def roast(interaction: discord.Interaction, member: discord.User):
    await interaction.response.send_message("🔥 Warming up the roaster...")
    await asyncio.sleep(1.5)
    await interaction.followup.send(f"🎤 {member.mention} {random.choice(ROASTS)}")


@bot.tree.command(name="expose", description="Expose a user's embarrassing secret")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def expose(interaction: discord.Interaction, member: discord.User):
    await interaction.response.send_message(f"📡 Scanning {member.mention}'s activity logs...")
    await asyncio.sleep(1)
    await interaction.followup.send(f"[{progress_bar(50)}] 50% — cross-referencing sources...")
    await asyncio.sleep(1.5)
    await interaction.followup.send(f"[{progress_bar(100)}] 100% — intel confirmed.")
    await asyncio.sleep(0.5)
    await interaction.followup.send(f"💥 EXPOSED: {member.mention} {random.choice(EXPOSE_FACTS)}")


@bot.tree.command(name="history", description="Leak a user's browser history")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def history(interaction: discord.Interaction, member: discord.User):
    await interaction.response.send_message(f"🌐 Retrieving {member.mention}'s browser history...")
    await asyncio.sleep(1)
    await interaction.followup.send(f"[{progress_bar(60)}] 60% — decrypting incognito mode...")
    await asyncio.sleep(1.5)
    await interaction.followup.send(
        f"📂 **{member.display_name}'s Recent Searches:**\n{random.choice(BROWSER_HISTORIES)}"
    )


@bot.tree.command(name="iq", description="Calculate a user's IQ")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def iq(interaction: discord.Interaction, member: discord.User):
    await interaction.response.send_message(f"🧠 Running cognitive analysis on {member.mention}...")
    score        = random.randint(1, 200)
    comment_text = next(c for r, c in IQ_COMMENTS if score in r)
    await asyncio.sleep(1.5)
    await interaction.followup.send(f"📊 **IQ Result for {member.mention}: {score}**\n_{comment_text}_")


@bot.tree.command(name="sus", description="Investigate how sus a user is")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def sus(interaction: discord.Interaction, member: discord.User):
    await interaction.response.send_message(f"🔍 Investigating {member.mention}...")
    await asyncio.sleep(1)
    await interaction.followup.send(f"📋 **VERDICT:** {member.mention} is {random.choice(SUS_VERDICTS)}")
description="Rate a user across 5 categories")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def rate(interaction: discord.Interaction, member: discord.User):
    categories = {
        "Vibes":           random.randint(0, 10),
        "Intelligence":    random.randint(0, 10),
        "Drip":            random.randint(0, 10),
        "Trustworthiness": random.randint(0, 10),
        "Chaos":           random.randint(0, 10),
    }
    await interaction.response.send_message(f"📊 Rating {member.mention}...")
    await asyncio.sleep(1.5)
    lines   = "\n".join(f"**{k}:** {'⭐' * v}{'☆' * (10 - v)} ({v}/10)" for k, v in categories.items())
    overall = sum(categories.values()) / len(categories)
    await interaction.followup.send(
        f"🎯 **{member.display_name}'s Stats:**\n{lines}\n\n**Overall:** {overall:.1f}/10"
    )


@bot.tree.command(name="battle", description="Pit two users against each other in a stat battle")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def battle(interaction: discord.Interaction, member1: discord.User, member2: discord.User):
    await interaction.response.send_message(
        f"⚔️ **BATTLE INITIATED**\n{member1.mention} vs {member2.mention}\n\nScanning combatants..."
    )
    await asyncio.sleep(1.5)
    stats1  = {s: random.randint(1, 100) for s in BATTLE_STATS}
    stats2  = {s: random.randint(1, 100) for s in BATTLE_STATS}
    score1  = sum(stats1.values())
    score2  = sum(stats2.values())
    lines1  = "\n".join(f"  {k}: `{v}`" for k, v in stats1.items())
    lines2  = "\n".join(f"  {k}: `{v}`" for k, v in stats2.items())
    await interaction.followup.send(
        f"📊 **{member1.display_name}**\n{lines1}\n**Total: {score1}**\n\n"
        f"📊 **{member2.display_name}**\n{lines2}\n**Total: {score2}**"
    )
    await asyncio.sleep(2)
    await interaction.followup.send("🥊 Calculating outcome...")
    await asyncio.sleep(1.5)
    if score1 == score2:
        await interaction.followup.send("🤝 It's a **TIE**. Both of you go home disappointed.")
    else:
        winner = member1 if score1 > score2 else member2
        loser  = member2 if score1 > score2 else member1
        await interaction.followup.send(
            f"🏆 **{winner.mention} WINS!**\n"
            f"{winner.mention} {random.choice(BATTLE_ENDINGS)}\n\n"
            f"💀 {loser.mention} has been eliminated from existence."
        )


@bot.tree.command(name="rps", description="Challenge someone to Rock, Paper, Scissors")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def rps(interaction: discord.Interaction, opponent: discord.User):
    if opponent.bot:
        await interaction.response.send_message(
            "❌ You can't challenge a bot... unless you're scared of humans?", ephemeral=True
        )
        return
    if opponent.id == interaction.user.id:
        await interaction.response.send_message("❌ You can't challenge yourself. Touch grass.", ephemeral=True)
        return
    view = RPSView(interaction.user, opponent)
    await interaction.response.send_message(
        f"⚔️ **Rock, Paper, Scissors!**\n"
        f"{interaction.user.mention} has challenged {opponent.mention}!\n\n"
        f"Both players — pick your move below. Choices are hidden until both have chosen. 👇",
        view=view,
    )


@bot.tree.command(name="poll", description="Create a poll with custom options")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def poll(
    interaction: discord.Interaction,
    question: str,
    option1: str,
    option2: str,
    option3: str = None,
    option4: str = None,
):
    options = [o for o in [option1, option2, option3, option4] if o]
    view    = PollView(interaction.user, question, options)
    await interaction.response.send_message(view.render(), view=view)


@bot.tree.command(name="confess", description="Open an anonymous confession box")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def confess(interaction: discord.Interaction):
    channel = interaction.channel
    if channel is None:
        await interaction.response.send_message(
            "❌ Confessions can only be used in a server channel.", ephemeral=True
        )
        return
    view = ConfessView(channel)
    await interaction.response.send_message(
        "💌 **Anonymous Confessions**\n"
        "Click below to submit a confession. Nobody will know it was you — not even the bot owner. 🤫",
        view=view,
    )


@bot.tree.command(name="truth", description="Send someone a truth question they have to answer publicly")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def truth(interaction: discord.Interaction, member: discord.User):
    if member.bot:
        await interaction.response.send_message("❌ Bots don't answer truth questions.", ephemeral=True)
        return
    if member.id == interaction.user.id:
        await interaction.response.send_message("❌ Ask someone else, coward.", ephemeral=True)
        return
    channel = interaction.channel
    if channel is None:
        await interaction.response.send_message(
            "❌ Truth can only be used in a server channel.", ephemeral=True
        )
        return
    question = random.choice(TRUTH_QUESTIONS)
    view     = TruthView(member, interaction.user, question, channel)
    await interaction.response.send_message(
        f"🎯 **Truth or Dare — Truth!**\n\n"
        f"{interaction.user.mention} is asking {member.mention}:\n"
        f"**❓ {question}**\n\n"
        f"{member.mention}, click below to answer publicly. No backing out! 👇",
        view=view,
    )


@bot.tree.command(name="dare", description="Dare someone to do something")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def dare(interaction: discord.Interaction, member: discord.User):
    if member.bot:
        await interaction.response.send_message("❌ Bots don't do dares.", ephemeral=True)
        return
    if member.id == interaction.user.id:
        await interaction.response.send_message("❌ Dare someone else, not yourself.", ephemeral=True)
        return
    challenge = random.choice(DARE_CHALLENGES)
    view      = DareView(member, challenge)
    await interaction.response.send_message(
        f"🎲 **Truth or Dare — Dare!**\n\n"
        f"{interaction.user.mention} dares {member.mention}:\n"
        f"**🔥 {challenge}**\n\n"
        f"{member.mention} — complete it or chicken out. Your reputation is on the line. 👇",
        view=view,
    )


@bot.tree.command(name="help", description="Show all available commands")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="rooHackBot — Commands",
        description="All commands work in any server, DMs, and group chats.",
        color=0x5865F2,
    )
    embed.add_field(name="\u200b", value="**💀 Pranks**", inline=False)
    embed.add_field(name="🕵️ /hack @user",      value="Fake-hack someone with a dramatic sequence.",                                   inline=False)
    embed.add_field(name="🔥 /roast @user",     value="Hit someone with a brutal roast.",                                              inline=False)
    embed.add_field(name="💥 /expose @user",    value="Expose someone's most embarrassing secret.",                                    inline=False)
    embed.add_field(name="🌐 /history @user",   value="Leak someone's browser history.",                                               inline=False)
    embed.add_field(name="🧠 /iq @user",        value="Calculate someone's IQ (results may vary).",                                   inline=False)
    embed.add_field(name="🔴 /sus @user",       value="Investigate how sus someone is.",                                               inline=False)
    embed.add_field(name="⭐ /rate @user",      value="Rate someone across 5 categories.",                                             inline=False)
    embed.add_field(name="\u200b", value="**🎮 Games**", inline=False)
    embed.add_field(name="⚔️ /battle @u1 @u2", value="Pit two users in a random stat battle.",                                        inline=False)
    embed.add_field(name="🪨 /rps @user",       value="Rock, Paper, Scissors — both picks are hidden until revealed.",                 inline=False)
    embed.add_field(name="📊 /poll",            value="Create a live vote poll with up to 4 options.",                                 inline=False)
    embed.add_field(name="\u200b", value="**🎭 Social**", inline=False)
    embed.add_field(name="💌 /confess",         value="Open an anonymous confession box in the channel.",                              inline=False)
    embed.add_field(name="🎯 /truth @user",     value="Send someone a truth question they must answer publicly.",                      inline=False)
    embed.add_field(name="🎲 /dare @user",      value="Dare someone — they click ✅ Done or 🐔 Chicken out.",                         inline=False)
    embed.add_field(name="\u200b", value="**🃏 Anime Cards**", inline=False)
    embed.add_field(name="🃏 /card",            value="Roll a random anime character card — Common to Legendary rarity.",              inline=False)
    embed.add_field(name="👑 /getcard [name]",  value="*(Owner only)* Pull the exact character you want.",                             inline=False)
    embed.add_field(name="📂 /collection",      value="Browse all your rolled cards with ◀ ▶ buttons.",                               inline=False)
    embed.add_field(name="\u200b", value="**🎭 Reactions**", inline=False)
    embed.add_field(name="🎭 /react [mood]",    value="Get a random anime reaction GIF. 16 moods: happy, sad, dance, quirky and more.", inline=False)
    embed.add_field(name="\u200b", value="**👁️ Gojo Satoru**", inline=False)
    embed.add_field(name="👁️ /gojo [action]",  value="Gojo-specific reaction GIFs — Hollow Purple, Infinity, Six Eyes, Domain Expansion, Giggling and more.", inline=False)
    embed.set_footer(text="Works in any server, DMs, and group chats.")
    await interaction.response.send_message(embed=embed, ephemeral=True)


TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN secret is not set.")

bot.run(TOKEN, log_handler=None)

@bot.tree.command(name="rate", 
