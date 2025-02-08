import discord
from discord.ext import commands
from langdetect import detect
import re  # For checking English letters
import json
import os

# Enable intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for command processing
intents.guilds = True
intents.members = True  # Needed for managing members

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)

# File Paths
WELCOME_FILE = "welcome_config.json"
DATA_FILE = "test-data.json"
CONFIG_FILE = "config.json"

# ✅ Priority 1 Role Authority (Manually Set)
PRIORITY_ROLE_ID = None  # Replace with the actual role ID before using

# ========== HELPER FUNCTIONS ========== #

# Load JSON Data
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

# Save JSON Data
def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Load stored data
welcome_data = load_json(WELCOME_FILE)
test_data = load_json(DATA_FILE)
config = load_json(CONFIG_FILE)

# ✅ Check If User Has Priority 1 Authority
def has_priority_role(ctx):
    return PRIORITY_ROLE_ID and any(role.id == PRIORITY_ROLE_ID for role in ctx.author.roles)

# ✅ Overriding Tester Role Check to Include Priority 1
def has_tester_role(ctx):
    if has_priority_role(ctx):  
        return True  # Priority 1 users can bypass restrictions
    tester_role_id = config.get("tester_role")
    return tester_role_id and any(role.id == tester_role_id for role in ctx.author.roles)

# ========== WELCOME SYSTEM ========== #

@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, channel: discord.TextChannel):
    """Set the welcome message channel"""
    welcome_data[str(ctx.guild.id)] = channel.id
    save_json(WELCOME_FILE, welcome_data)
    await ctx.send(f"✅ Welcome channel set to {channel.mention}!")

@bot.command()
async def welcometest(ctx):
    """Test the welcome message"""
    guild_id = str(ctx.guild.id)
    if guild_id in welcome_data:
        channel = bot.get_channel(welcome_data[guild_id])
        if channel:
            await channel.send(f"👋 Welcome {ctx.author.mention} to **{ctx.guild.name}**! Enjoy your stay! 🎉")
        else:
            await ctx.send("❌ Welcome channel not set! Use `!setwelcome #channel` first.")
    else:
        await ctx.send("❌ Welcome channel not set! Use `!setwelcome #channel` first.")

@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id in welcome_data:
        channel = bot.get_channel(welcome_data[guild_id])
        if channel:
            await channel.send(f"👋 Welcome {member.mention} to **{member.guild.name}**! Enjoy your stay! 🎉")

# ========== TESTER SYSTEM ========== #

@bot.command()
@commands.has_permissions(administrator=True)
async def settesterrole(ctx, role: discord.Role):
    """Set the Alpha Tester/Management role"""
    config["tester_role"] = role.id
    save_json(CONFIG_FILE, config)
    await ctx.send(f"✅ Tester role set to {role.mention}!")

@bot.command()
async def adddata(ctx, key: str, *, value: str):
    """Adds or updates test data"""
    if not has_tester_role(ctx):
        return await ctx.send("❌ You don't have permission to use this command!")
    
    test_data[key] = value
    save_json(DATA_FILE, test_data)
    await ctx.send(f"✅ Data added: `{key}` → `{value}`")

@bot.command()
async def getdata(ctx, key: str):
    """Retrieve specific test data"""
    if not has_tester_role(ctx):
        return await ctx.send("❌ You don't have permission to use this command!")

    if key in test_data:
        await ctx.send(f"📌 `{key}` → `{test_data[key]}`")
    else:
        await ctx.send("❌ No data found for this key!")

@bot.command()
async def alldata(ctx):
    """Displays all stored test data"""
    if not has_tester_role(ctx):
        return await ctx.send("❌ You don't have permission to use this command!")

    if test_data:
        data_str = "\n".join([f"📌 `{k}` → `{v}`" for k, v in test_data.items()])
        await ctx.send(f"**📂 Stored Test Data:**\n{data_str}")
    else:
        await ctx.send("📂 No data stored yet!")

@bot.command()
async def deletedata(ctx, key: str):
    """Deletes a specific test entry"""
    if not has_tester_role(ctx):
        return await ctx.send("❌ You don't have permission to use this command!")

    if key in test_data:
        del test_data[key]
        save_json(DATA_FILE, test_data)
        await ctx.send(f"🗑️ Deleted `{key}` from test data.")
    else:
        await ctx.send("❌ No such key found!")

# ========== MODERATION SYSTEM ========== #

@bot.command()
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    """Mute a member (Requires 'Muted' Role)"""
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")

    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False, speak=False))
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False, speak=False)

    await member.add_roles(mute_role)
    await ctx.send(f"🔇 {member.mention} has been muted. Reason: {reason}")

@bot.command()
async def unmute(ctx, member: discord.Member):
    """Unmute a member"""
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if mute_role in member.roles:
        await member.remove_roles(mute_role)
        await ctx.send(f"🔊 {member.mention} has been unmuted.")
    else:
        await ctx.send(f"⚠️ {member.mention} is not muted.")

# ========== UTILITY COMMANDS ========== #

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! 👋")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! 🏓 {round(bot.latency * 1000)}ms")

@bot.command()
async def info(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! If you need assistance, contact an admin.")

# ========== BOT STATUS & MESSAGE FILTER ========== #

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Aki"))
    print(f'✅ Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if re.search(r'[a-zA-Z]', message.content):
        await bot.process_commands(message)
        return  

    try:
        lang = detect(message.content)
        if lang != "en":
            await message.delete()
            await message.channel.send(f"{message.author.mention}, please use English only!")
    except:
        pass

# Run bot (DO NOT put your token here in public!)
bot.run("YOUR_BOT_TOKEN")