import discord
from discord.ext import commands
import random
import asyncio 
from collections import deque
import os
import json
import datetime 
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ----------------------------
# LOAD / SAVE WELCOME DATA
# ----------------------------

def load_data():
    try:
        with open("welcome.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_data():
    with open("welcome.json", "w") as f:
        json.dump(welcome_channels, f)

welcome_channels = load_data()

# ----------------------------
# INTENTS
# ----------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# READY EVENT
# ----------------------------

@bot.event
async def on_ready():
    if not hasattr(bot, "already_ready"):
        bot.already_ready = True
        print(f"[{datetime.datetime.now()}] Bot online: {bot.user}")

#test command 
@bot.command()
async def test(ctx):
    await ctx.send(f"Instance ID: {id(bot)}")

# ----------------------------
# WHEEL COMMAND
# ----------------------------

@bot.command()
async def wheel(ctx, *, options):
    choices = [c.strip() for c in options.split(",")]

    if len(choices) < 2:
        await ctx.send("Give me at least 2 options 😭")
        return

    embed = discord.Embed(
        title="🎡 Decision Wheel",
        description="Spinning...",
        color=discord.Color.blurple()
    )

    msg = await ctx.send(embed=embed)

    wheel = deque(choices)

    for _ in range(10):
        await asyncio.sleep(0.1)

        wheel.rotate(1)
        preview = list(wheel)[:5]

        lines = []
        for idx, item in enumerate(preview):
            if idx == 2:
                lines.append(f"🟢 **{item}**")
            else:
                lines.append(f"🔴 {item}")

        embed.description = "🎰\n" + "\n".join(lines)
        await msg.edit(embed=embed)

    await asyncio.sleep(0.5)

    result = random.choice(choices)

    embed.title = "🎯 Result"
    embed.description = f"**{result}**"
    embed.color = discord.Color.green()

    await msg.edit(embed=embed)

# ----------------------------
# FUN SPEED GIF TRIGGER
# ----------------------------

speed_gifs = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnUzdGZwdGExczZwanpzZnA4cnh6YWhzamJzaTVubTBjMHQxOHB3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/D63HGAzG15LQrjBPRE/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnUzdGZwdGExczZwanpzZnA4cnh6YWhzamJzaTVubTBjMHQxOHB3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/MOYUOOoIHOj9PKN1rE/giphy.gif",
]

# ----------------------------
# WELCOME / GOODBYE EVENTS
# ----------------------------

@bot.event
async def on_member_join(member):
    channel_id = welcome_channels.get(str(member.guild.id))

    if channel_id:
        channel = member.guild.get_channel(channel_id)
        if channel:
            await channel.send(f"👁️ Welcome to heaven, {member.mention}!")

@bot.event
async def on_member_remove(member):
    channel_id = welcome_channels.get(str(member.guild.id))

    if channel_id:
        channel = member.guild.get_channel(channel_id)
        if channel:
            await channel.send(f"👁️ {member.name} left.")

# ----------------------------
# MESSAGE LISTENER
# ----------------------------

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "speed" in message.content.lower():
        await message.channel.send(random.choice(speed_gifs))

    await bot.process_commands(message)

# ----------------------------
# COMMANDS
# ----------------------------

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, channel: discord.TextChannel):
    welcome_channels[str(ctx.guild.id)] = channel.id
    save_data()
    await ctx.send(f"✅ Welcome channel set to {channel.mention}")

@bot.command()
async def hello(ctx):
    await ctx.send("hi :3")

@bot.command()
async def whoami(ctx):
    await ctx.send(f"You are {ctx.author}")

@bot.command()
async def roll(ctx):
    await ctx.send(str(random.randint(1, 100)))

# ----------------------------
# RUN BOT
# ----------------------------

keep_alive()
bot.run(os.getenv("TOKEN"))
