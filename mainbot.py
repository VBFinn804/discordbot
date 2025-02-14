import discord
from discord.ext import commands
import os

# Setze deine Bot-Token hier (auf Replit als Umgebungsvariable speichern!)
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Erstelle einen Bot mit Präfix "."
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} ist online!')
    await bot.change_presence(activity=discord.Game(name="Systemüberwachung"))

# Begrüßungsnachricht für neue Mitglieder
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(f"Willkommen {member.mention} auf dem Server!")

# Join to Create System
@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    category = discord.utils.get(guild.categories, name="Voice Channels")

    if after.channel and after.channel.name == "Join to Create":
        new_channel = await guild.create_voice_channel(name=f"🔊 {member.name}'s Channel", category=category)
        await member.move_to(new_channel)

        def check(a, b, c):
            return len(new_channel.members) == 0

        await bot.wait_for("voice_state_update", check=check)
        await new_channel.delete()

# Einfache Befehle
@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def info(ctx):
    await ctx.send("Ich bin ein System-Bot, der auf Replit gehostet wird!")

# Moderationsbefehl: Benutzer kicken
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.name} wurde gekickt. Grund: {reason}")

# Moderationsbefehl: Benutzer bannen
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.name} wurde gebannt. Grund: {reason}")

# Starte den Bot
bot.run(TOKEN)
