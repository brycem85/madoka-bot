import discord
from discord.ext import commands
import random
import asyncio 
from collections import deque
import math 

# Intents are required now
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

#Wheel command
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

    for i in range(10):
        await asyncio.sleep(0.1)

        wheel.rotate(1)
        preview = list(wheel)[:5]

        lines = []

        for idx, item in enumerate(preview):
            if idx == 2:
                lines.append(f"🟢 **{item}**")
            else:
                lines.append(f"🔴 {item}")

        display = "\n".join(lines)

        embed.description = f"🎰\n{display}"

        await msg.edit(embed=embed)

    await asyncio.sleep(0.5)

    result = random.choice(choices)

    embed.title = "🎯 Result"
    embed.description = f"**{result}**"
    embed.color = discord.Color.green()

    await msg.edit(embed=embed)
#Speed gifs (replace with your own GIF URLs)
speed_gifs = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnUzdGZwdGExczZwanpzZnA4cnh6YWhzamJzaTVubTBjMHQxOHB3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/D63HGAzG15LQrjBPRE/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnUzdGZwdGExczZwanpzZnA4cnh6YWhzamJzaTVubTBjMHQxOHB3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/MOYUOOoIHOj9PKN1rE/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnUzdGZwdGExczZwanpzZnA4cnh6YWhzamJzaTVubTBjMHQxOHB3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/s5wFafpHxqKbIEERl9/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnUzdGZwdGExczZwanpzZnA4cnh6YWhzamJzaTVubTBjMHQxOHB3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/68L3bCQleHM3lIl58J/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnUzdGZwdGExczZwanpzZnA4cnh6YWhzamJzaTVubTBjMHQxOHB3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/lxxOGaDRk4f7R5TkBd/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnUzdGZwdGExczZwanpzZnA4cnh6YWhzamJzaTVubTBjMHQxOHB3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GCO5WNzFmlc0vjK8cA/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnUzdGZwdGExczZwanpzZnA4cnh6YWhzamJzaTVubTBjMHQxOHB3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/O0iwtaQGSuppWRZXnk/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnUzdGZwdGExczZwanpzZnA4cnh6YWhzamJzaTVubTBjMHQxOHB3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/nKxhhe2UlnnFoPbBnE/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eDhhM2tjNmRhNTBrbTJmcXpjczVhdzRpZnlic3h1cXBiYTk3NnRnMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/yFnd80hiHQyEvNcmGd/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3ZwZWd0MTh1OXhwM2pkZ28wZHl3OHIxN3dtamlzeGVrMm1hM3IwdyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/12bGJjBwzS7oNCzKqC/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDN6dGI4dXQ1Yng1eWp5azk5M3NsYjM5YTkxczdpOW9mZzc3MXh6ayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/hLVv5qog6L2EWaGQkd/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDN6dGI4dXQ1Yng1eWp5azk5M3NsYjM5YTkxczdpOW9mZzc3MXh6ayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/dcKWFKCzjdozxwZASo/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3a3BsZTc1bjBtNTFnNHMyNXRnZnl4ejl4dXNhdmNxcmV6aDN0NDBzMCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/NuxHYnFFiNFpTswXUU/giphy.gif",
]
#Welcome message 
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")

    if channel:
        await channel.send(f"👋 Welcome to the server, {member.mention}!")

#Goodbye message 
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")

    if channel:
        await channel.send(f"👋 {member.name} just left the server.")

#Speed command
@bot.event
async def on_message(message):
    # ignore bot messages (important or it will loop)
    if message.author.bot:
        return

    # check if "speed" is in the message
    if "speed" in message.content.lower():
        await message.channel.send(random.choice(speed_gifs))

    # THIS is required so commands like !ping still work
    await bot.process_commands(message)

# Ping test
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Hello command
@bot.command()
async def hello(ctx):
    await ctx.send("hi :3")

# Who am I command
@bot.command()
async def whoami(ctx):
    await ctx.send(f"You are {ctx.author}")

# Roll command (1–100)
@bot.command()
async def roll(ctx):
    await ctx.send(str(random.randint(1, 100)))

# Run the bot (PASTE YOUR TOKEN HERE)
bot.run(os.getenv("TOKEN"))