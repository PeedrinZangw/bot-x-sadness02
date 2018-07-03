import discord
import youtube_dl
from discord.ext import commands

TOKEN = 'NDUyNjEzMTcwMzUyMDk1MjMy.DhyhHg.JGsxbcLzRCVOfjNHNAJhfdWiVLo'
client = commands.Bot(command_prefix = 's2!')

players = {}

@client.event
async def on_ready():
    print('sadness 02 - Online!')
    await client.change_presence(game=discord.Game(name='Lofi Hip-Hop 24/7 [BOT SADNESS 02]'))

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconect()

@client.command(pass_context=True)
async def play (ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

client.run(TOKEN)
