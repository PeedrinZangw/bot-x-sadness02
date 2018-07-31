import discord
import youtube_dl
from discord.ext import commands
import asyncio
from itertools import cycle

TOKEN = 'NDcyNTc5NzAyNDI3NzQ2MzA2.Dj1b7g.ImrLfBRHRq2z56YZO5CFWr0dBrU'
client = commands.Bot(command_prefix = 'rw!')
status = ['discord.gg/nzbG5eR', 'amor para nossos membros', 'created by ! Ｈａｚａｒｄ 竹エッ#0459']

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print('Ratazanas bot - Online')

@client.command(pass_context=True)
async def entrar(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    await client.say(':musical_note: | Estou entrando no canal...')

@client.command(pass_context=True)
async def sair(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    await client.say(':musical_note: | Estou saindo do canal...')

@client.command(pass_context=True)
async def tocar(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()
    await client.say(':musical_note: | Irei começar a tocar a música...')

@client.command(pass_context=True)
async def pausar(ctx):
    id = ctx.message.server.id
    players[id].pause()
    await client.say(':musical_note: | Música pausada...')

@client.command(pass_context=True)
async def parar(ctx):
    id = ctx.message.server.id
    players[id].stop()
    await client.say(':musical_note: | Música parada.')

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    await client.say(':musical_note: | Música resumida.')

@client.command(pass_context=True)
async def adicionar(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].appened(player)
    else:
        queues[server.id] = [player]
    await client.say(':musical_note: | Música Adicionada à lista.')

@client.event
async def on_member_join(member):
  canal = client.get_channel("467101617762730016")
  regras = client.get_channel("467103656219508736")
  msg = "Bem-vindo {} ao Ratazana's World\nAntes de tudo leia as regras no canal {}\n\nAgora você está seguro com a tropa Ratazana.\nhttps://i.imgur.com/4yB6I4V.jpg".format(member.mention, regras.mention)
  await client.send_message(member, msg)

@client.command()
async def logout():
    await client.logout()

client.loop.create_task(change_status())
client.run(TOKEN)
