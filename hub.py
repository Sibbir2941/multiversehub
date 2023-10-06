import discord
from discord import app_commands
from discord.ext import commands
import psutil
import datetime
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import time
from io import BytesIO
import base64
from discord.ui import view
from discord.interactions import Interaction
import requests
import random



players = {}

API_KEY = "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"
API_KEYS ="de306122167d419f85381454230704"


intents = discord.Intents.all()
intents.typing = True
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print("Bot Running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)

@bot.tree.command(name="help", description="Display a list of available commands.")
async def help_command(interaction: discord.Interaction):
    # Create a dictionary of available commands and their descriptions
    commands_dict = {
        "/about": "Displays information about the bot.",
        "/invite": "Creates an invite link for the current channel and displays it in a button.",
        "/avatar": "Displays the avatar of a member..",
        "/aclear": "Deletes all messages in the channel.",
        "/serverinfo": "Displays information about the current server.",
        "/ask": "Get a response from OpenAI's GPT-3.",
        "/help": "Display a list of available commands.",

        # Add more commands and descriptions here
    }
    
    # Create an embedded message to display the list of commands and descriptions
    embed = discord.Embed(title="Available Commands", color=0x00ff00)
    for command, description in commands_dict.items():
        embed.add_field(name=command, value=description, inline=False)
    
    # Send the embedded message as a response to the /help command
    await interaction.response.send_message(embed=embed)




WELCOME_CHANNEL_ID = 1057730489663885382 # Replace with the ID of your welcome channel

@bot.event
async def on_member_join(member):
    # Get the welcome channel
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)

    # Create the welcome message embed
    embed = discord.Embed(title=f"Welcome {member.display_name} to the server!", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url)

    # Add a description to the embed
    embed.add_field(name="Introduction", value="Thanks for joining our server. We hope you have a great time here!", inline=False)

    # Send the embed to the welcome channel
    await welcome_channel.send(embed=embed)

    # Send a direct message to the new member
    # Create the message embed
    embed = discord.Embed(title="Welcome to our server!", description="Before you start chatting, please make sure to follow the rules and guidelines below:", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url)

    # Add the rules and guidelines to the embed
    embed.add_field(name="Rule 1: Be respectful to others in the server.", value="Treat others with kindness and respect at all times.")
    embed.add_field(name="Rule 2: No spamming or flooding the chat with messages.", value="Please refrain from posting repetitive or unnecessary messages.")
    embed.add_field(name="Rule 3: No adult content or NSFW content allowed.", value="Any content that is not suitable for all ages is strictly prohibited.")
    embed.add_field(name="Rule 4: No advertising or self-promotion without permission from the server staff.", value="Please do not promote your own content or products without permission.")
    embed.add_field(name="Rule 5: No hate speech, discrimination, or harassment of any kind.", value="We do not tolerate any form of hate speech, discrimination, or harassment.")
    embed.add_field(name="Rule 6: Do not share personal information or sensitive data.", value="Please keep your personal information and sensitive data private and do not share it with others.")
    embed.add_field(name="Rule 7: Follow the instructions of the server staff.", value="Please follow the instructions of the server staff at all times.")
    embed.add_field(name="Rule 8: Do not use bots or scripts to automate actions in the server.", value="The use of bots or scripts to automate actions in the server is strictly prohibited.")
    embed.add_field(name="Rule 9: No trolling or intentionally causing disruption in the server.", value="Please do not engage in trolling or disruptive behavior.")
    embed.add_field(name="Rule 10: Do not use offensive language or slurs.", value="Please be mindful of the language you use and avoid using offensive slurs.")

    # Send the embed to the new member
    await member.send(embed=embed)


@bot.event
async def on_message(message):
    if not message.author.bot:
        if message.content.startswith('!weather') or message.content.startswith('!generate'):
            await message.channel.send(f"Please use the slash command '/{message.content[1:]}' instead of the regular command '{message.content}'")
        else:
            await bot.process_commands(message)




@bot.tree.command(name="aclear", description="Deletes all messages in the channel.")
@commands.has_permissions(manage_messages=True)
async def aclear(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_messages:
        emoji = "❌"
        await interaction.response.react(emoji)
        await interaction.response.send_message("You do not have permission to use this command.")
        return

    channel = interaction.channel

    await channel.purge()

    confirm_embed = discord.Embed(title="Clear Command Executed", description=f"All messages in {channel.mention} have been deleted by {interaction.user.mention}", color=discord.Color.red())
    confirm_embed.set_author(name="MultiVerse Hub Bot")
    await interaction.response.send_message(embed=confirm_embed)

    await interaction.response.send_message("Messages have been deleted successfully.")



@bot.tree.command(name="avatar", description="Displays the avatar of a member.")
async def avatar(interaction: discord.Interaction, member: discord.Member):
    avatar_url: str = member.avatar.url
    embed: discord.Embed = discord.Embed(title=f"Avatar of {member.name}", color=member.color)
    embed.set_image(url=avatar_url)
    await interaction.response.send_message(embed=embed)



@bot.tree.command()
async def about(interaction):
    """Displays information about the bot."""
    cpu_usage = psutil.cpu_percent()
    uptime = str(datetime.timedelta(seconds=int(psutil.boot_time() - psutil.Process().create_time())))
    embed = discord.Embed(title="About Bot", color=0x00ff00)
    embed.add_field(name="Bot Ping", value=f"{round(bot.latency * 1000)}ms")
    embed.add_field(name="Bot Code", value="This bot was written in Python using the Discord.py library.")
    embed.add_field(name="Bot Author", value="This bot was fully written by **Mohammad Sibbir**")
    embed.add_field(name="Servers Watching", value=len(bot.guilds))
    embed.add_field(name="CPU Usage", value=f"{cpu_usage}%")
    embed.add_field(name="Uptime", value=uptime)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serverinfo", description="Displays information about the current server.")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"{guild.name} ({guild.id})", color=0x00ff00)
    embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Owner", value=guild.owner.mention)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%b %d, %Y"))
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.add_field(name="Text Channels", value=len(guild.text_channels))
    embed.add_field(name="Voice Channels", value=len(guild.voice_channels))
    await interaction.response.send_message(embed=embed)


@bot.tree.command(description="Get a response from OpenAI's GPT-3")
async def ask(interaction: discord.Interaction, *, prompt: str):
    async with aiohttp.ClientSession() as session:
        payload = {
            "model": "text-davinci-003",
            "prompt": prompt,
            "temperature": 0.5,
            "max_tokens": 50,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "best_of": 1,
        }
        headers = {"Authorization": f"Bearer {API_KEY}"}
        async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
            response = await resp.json()
            embed = discord.Embed(title="MultiVerse Hub Response:", description=response["choices"][0]["text"])
            await interaction.response.send_message(embed=embed)

@bot.tree.command()
async def weather(interaction: discord.Interaction, *, city: str):
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEYS,
        "q": city
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as res:
            data = await res.json()
            location = data["location"]["name"]
            temp_c = data["current"]["temp_c"]
            temp_f = data["current"]["temp_f"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]
            wind_mph = data["current"]["wind_mph"]
            condition = data["current"]["condition"]["text"]
            condition_icon = data["current"]["condition"]["icon"]
            image_url = "https:" + condition_icon
            embed = discord.Embed(title=f"Weather For {location}", description=f"The condition in `{location}` is ` {condition}`")
            embed.add_field(name="Temperature", value=f"c:{temp_c} | f: {temp_f}")
            embed.add_field(name="Humidity", value=f"{humidity}")
            embed.add_field(name="Wind Speeds", value=f"KPH: {wind_kph} | MPH: {wind_mph}")
            embed.set_thumbnail(url=image_url)
            await interaction.response.send_message(embed=embed)

class Dropdown(discord.ui.Select):
    def __init__(self, message, images, user):
        self.message = message
        self.images = images
        self.user = user

        options = [
            discord.SelectOption(label="1"),
            discord.SelectOption(label="2"),
            discord.SelectOption(label="3"),
            discord.SelectOption(label="4"),
            discord.SelectOption(label="5"),
            discord.SelectOption(label="6"),
            discord.SelectOption(label="7"),
            discord.SelectOption(label="8"),
            discord.SelectOption(label="9"),
        ]

        super().__init__(
            placeholder="Choose the image you want to see!",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if not int(self.user) == int(interaction.user.id):
            await interaction.response.send_message("You are not the author of this message!", ephemeral=True)
            return

        selection = int(self.values[0]) - 1
        image = BytesIO(base64.decodebytes(self.images[selection].encode("utf-8")))
        embed = discord.Embed(title="Content Generated By Multiverse Hub")
        await self.message.edit(content=None, embed=embed, file=discord.File(image, "generatedImage.png"), view=DropdownView(self.message, self.images, self.user))


class DropdownView(discord.ui.View):
    def __init__(self, message, images, user):
        super().__init__()
        self.message = message
        self.images = images
        self.user = user
        self.add_item(Dropdown(self.message, self.images, self.user))



@bot.tree.command()
async def generate(interaction: Interaction, prompt: str):
    ETA = int(time.time() + 60)
    msg = await interaction.response.send_message(f"Go grab a coffee, this may take some time.. ETA: <t:{ETA}:R>")
    async with aiohttp.request("POST", "https://backend.craiyon.com/generate", json={"Any Image Name": prompt}) as resp:
        r = await resp.json()
        images = r['images']
        image = BytesIO(base64.decodebytes(images[0].encode("utf-8")))
        embed = discord.Embed(title="Content Generated By Multiverse Hub")
        await msg.delete()

        await interaction.response.send_message(content=None, embed=embed, file=discord.File(image, "generatedImage.png"), view=view.DropdownView(interaction, images, interaction.user.id))

class InviteButtons(discord.ui.View):
    def __init__(self, inv: str):
        super().__init__()
        self.inv = inv
        self.add_item(discord.ui.Button(label="Invite Link", url=self.inv))

    @discord.ui.button(label="Invite Btn", style=discord.ButtonStyle.blurple)
    async def inviteBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.inv, ephemeral=True)

@bot.tree.command(description="Creates an invite link for the current channel and displays it in a button.")
async def invite(interaction: discord.Interaction):
    try:
        inv = await interaction.channel.create_invite()
        await interaction.response.send_message("Click the button below to invite someone!", view=InviteButtons(str(inv)))
    except discord.errors.Forbidden:
        await interaction.response.send_message("I don't have permission to create an invite link. Please give me the necessary permissions.")

@bot.tree.command()
async def meme(interaction):
    response = requests.get('https://www.reddit.com/r/memes/random.json', headers={'User-agent': 'Mozilla/5.0'})
    data = response.json()[0]['data']['children'][0]['data']
    
    if not data['url'].endswith(('.jpg', '.jpeg', '.png')):
        await interaction.response.send_message("Sorry, I couldn't find any memes right now :(")
        return
    
    embed = discord.Embed(title=data['title'], url=f"https://www.reddit.com{data['permalink']}")
    embed.set_image(url=data['url'])
    await interaction.response.send_message(embed=embed)



@bot.tree.command()
async def generate(interaction: Interaction, prompt: str):
    ETA = int(time.time() + 60)
    msg = await interaction.response.send_message(f"Go grab a coffee, this may take some time.. ETA: <t:{ETA}:R>")
    async with aiohttp.request("POST", "https://backend.craiyon.com/generate", json={"Any Image Name": prompt}) as resp:
        r = await resp.json()
        images = r['images']
        image = BytesIO()

bot.run("BOT_TOKEN")
