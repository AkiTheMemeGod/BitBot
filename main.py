import discord
from discord.ext import commands
from dependencies import *
import random
import bot_responses as br
import requests
from bs4 import BeautifulSoup
from AnarchKeyClient import AnarchKeyClient

AnarchKey = AnarchKeyClient(api_key='OcXevh4XAMxPQsOlDfqMjsK0x13RcjCaH-5D2HlC6zKnec5bXvr2tkaOEs9AIcKp', username='AkiTheMemeGod')

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

#FUN PARTS
@bot.command(name='roast')
async def roast(ctx, person: discord.User = ""):
    if person != "":
        response = f"{person.mention} {random.choice(br.roasts)}"
        await ctx.send(response)

    else:
        response = f"{ctx.author.mention} {random.choice(br.roasts_for_missing_argument)}"
        await ctx.send(response)

@bot.command()
async def meme(ctx):
    url = "https://www.reddit.com/r/memes/hot.json?limit=50"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            memes = response.json()["data"]["children"]
            meme = random.choice(memes)["data"]
            embed = discord.Embed(title=meme["title"], url=f"https://reddit.com{meme['permalink']}")
            embed.set_image(url=meme["url"])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch memes, try again later!")
    except Exception as e:
        await ctx.send("Error fetching memes!")
        print(f"Error: {e}")

@bot.command()
async def rolldice(ctx):
    roll = random.randint(1,6)
    await ctx.send(roll)

@bot.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)
    event = f'{username} said: "{user_message}" ({channel})'
    with open("log.log", "a") as log_file:
        log_file.write(event + "\n")
    print(event)


    if message.author == bot.user:
        return

    if contains_prohibited_content(message.content):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, 🚫 please follow the server rules!")

    if f"{get("prefix.txt")}change prefix to" in user_message:
        put(user_message[18:19], "prefix.txt")
        response = f"{message.author.mention} the prefix has been changed to `{get('prefix.txt')}`"
        await message.channel.send(response)

    if "prefix?" == user_message:
        response = f"`{get("prefix.txt")}` is the current prefix for the bot-->{bot.user}"
        await message.channel.send(response)

    await bot.process_commands(message)


@bot.command(name='whitelist')
async def whitelist(ctx, person: discord.User = ""):
    if str(ctx.author)+"\n" in get("Moderators.txt", True):
        print("in command")
        put(person.name, "Moderators.txt",True)
        await ctx.send(f"Added {person.mention} as a Moderator")



def run_discord_bot():
    bot.run(token=AnarchKey.get_api_key("BitBot - Discord")['api_key'])
