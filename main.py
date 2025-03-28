import discord
from discord.ext import commands

import tokens
from dependencies import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)


async def send_message(ctx, response, is_private):
    try:
        if isinstance(response, dict) and 'file' in response:
            await ctx.send(file=discord.File(response['file']))
        else:
            await ctx.author.send(response) if is_private else await ctx.send(response)
    except Exception as e:
        print(e)


@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")



@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    await bot.tree.sync()
    await bot.change_presence(status=discord.Status.idle)

    channel_id = 1176920698640408576
    startup_channel = bot.get_channel(channel_id)

    if startup_channel:
        await startup_channel.purge(limit=None)
        await startup_channel.send("@everyone"
                                   "https://tenor.com/view/getting-online-getting-online-gif-27546602")
    else:
        print("Could not find the specified channel for startup message.")

def run_discord_bot():
    bot.run(tokens.token)
