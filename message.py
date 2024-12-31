import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

CHANNEL_ID = None
MESSAGE = "This is your daily message!"

async def schedule_next_message():
    now = datetime.now()
    tomorrow = now.date() + timedelta(days=1)
    random_hour = random.randint(0, 23)
    next_message_time = datetime.combine(tomorrow, datetime.min.time().replace(hour=random_hour))
    
    seconds_until_message = (next_message_time - now).total_seconds()
    await asyncio.sleep(seconds_until_message)
    if CHANNEL_ID:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(MESSAGE)
            print(f"Message sent at {datetime.now()}")
        else:
            print("Could not find the specified channel")
    
    await schedule_next_message()

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')
    await schedule_next_message()

@bot.command()
async def set_channel(ctx):
    global CHANNEL_ID
    CHANNEL_ID = ctx.channel.id
    await ctx.send(f"Channel set! Messages will be sent here daily at a random hour.")

@bot.command()
async def set_message(ctx, *, new_message):
    global MESSAGE
    MESSAGE = new_message
    await ctx.send(f"Message updated! New message is: {MESSAGE}")

bot.run('YOUR_DISCORD_BOT_TOKEN')