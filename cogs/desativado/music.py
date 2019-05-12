import re
import discord
import logging
import math
import datetime
import urllib
import asyncio
from urllib.request import Request, urlopen
from utils import checks
from utils import paged
import lavalink
import random
import requests
from utils import arghelp
from discord.ext import commands


url_re = re.compile('https?:\/\/(?:www\.)?.+')

class music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.votes = []
        
        if not hasattr(bot, 'lavalink'):
            lavalink.Client(ws_port=2333, host="localhost", bot=bot, password='youshallnotpass', loop=self.bot.loop, log_level=logging.ERROR)
            self.bot.lavalink.register_hook(self._events)

    async def _events(self, event):
        if isinstance(event, lavalink.Events.TrackStartEvent):
            if event.player.guild_id not in map(lambda x: x["id"], self.votes):
                self.votes.append({"id": event.player.guild_id, "votes": []})
            else:
                list(filter(lambda x: x["id"] == event.player.guild_id, self.votes))[0]["votes"] = []
            channel = event.player.fetch('channel')
            author = self.bot.get_user(event.track.requester)
            guild = self.bot.get_guild(int(event.player.guild_id))
            if channel:
                channel = guild.get_channel(channel)
                if channel:
                    dur = lavalink.Utils.format_time(event.track.duration)
                    req = self.bot.get_user(int(event.track.requester))
                    s=discord.Embed(colour=0x7289DA, title='Tocando agora:', description=f"[{event.track.title}]({event.track.uri})")
                    s.add_field(name="Duração:", value=lavalink.Utils.format_time(event.track.duration) if not event.track.stream else "LIVE")
                    s.set_footer(text=f"Cripton © 2019 | Requisitado por {req.name}.")
                    s.set_thumbnail(url=event.track.thumbnail)
                    await channel.send(embed=s)
        elif isinstance(event, lavalink.Events.QueueEndEvent):
            channel = event.player.fetch('channel')
            guild = self.bot.get_guild(int(event.player.guild_id))
            if channel:
                channel = guild.get_channel(channel)
                if channel:
                    await channel.send('As músicas acabaram ;(')
        
    def __unload(self):
        for guild_id, player in self.bot.lavalink.players:
            self.bot.loop.create_task(player.disconnect())
            player.cleanup()
        self.bot.lavalink.players.clear()
        self.bot.lavalink.unregister_hook(self._event)

    @commands.command()
    async def seek(self, ctx, position: str):
        """Skip forwards or backwards in a song or set the exact time with the format hh:mm:ss"""
        position_re = re.compile("(?:([0-9]+):|)([0-9]+):([0-9]+)")
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if not player.is_playing:
            return await ctx.send(f'**{ctx.author.name}** eu não estou tocando nada no momento!')
        if not player.current.can_seek:
            return await ctx.send("Você não pode usar esse comando enquanto estiver ouvindo uma **LIVE**.")
        if player.fetch('sessionowner') == ctx.author.id or player.fetch("sessionowner") not in map(lambda c: c.id, player.connected_channel.members):
            match = position_re.match(position)
            if match:
                hours = int(match.group(1)) if match.group(1) else 0
                minutes = int(match.group(2))
                seconds = int(match.group(3))
                time = ((hours * 3600) + (minutes * 60) + seconds) * 1000
            elif position.isdigit():
                time = player.position + int(position) * 1000
            elif position.startswith("-"):
                time = player.position + -(int(position[1:]) * 1000)
            else:
                return await ctx.send(f"**{ctx.author.name}** o tempo que você informou é inválido.")
            await player.seek(time)
            await ctx.send("Agora estou reproduzindo á música dêsde: **{}**".format(self.format_time(time)))
        else:
            return await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")
                
    @commands.command(aliases=["summon"])
    async def join(self, ctx):
        """Make the bot join your current voice channel"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if player.is_connected:
            if len(set(filter(lambda m: not m.bot, player.connected_channel.members))) == 0 or ctx.author.id == player.fetch("sessionowner"):
                if not ctx.author.voice or not ctx.author.voice.channel:
                    return await ctx.send(f"**{ctx.author.name}** você não está conectado em nenhum canal de voz.")
                player.store('sessionowner', ctx.author.id)
                player.store('channel', ctx.channel.id)
                await player.connect(ctx.author.voice.channel.id)
                await ctx.send("Me conectei ao canal `{}`.".format(ctx.author.voice.channel.name))
            else:
                return await ctx.send(f"**{ctx.author.name}** eu já estou concectado em um canal de Voz.")
        else:
            if not ctx.author.voice or not ctx.author.voice.channel:
                return await ctx.send(f"**{ctx.author.name}** você não está concectado em nenhum canal de voz.")
            player.store('sessionowner', ctx.author.id)
            player.store('channel', ctx.channel.id)
            await player.connect(ctx.author.voice.channel.id)
            await ctx.send("Me conectei ao canal `{}`.".format(ctx.author.voice.channel.name))

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, query=None):
        """Play something by query or link"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if ctx.message.attachments and not query:
            query = ctx.message.attachments[0].url
        elif not ctx.message.attachments and not query:
            return await arghelp.send(self.bot, ctx)
        else:
            query = query.strip('<>').replace("music.", "")
        if player.is_connected:
            if not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send(f"**{ctx.author.name}** você não está concectado em nenhum canal de voz.")
        else:
            if not ctx.author.voice or not ctx.author.voice.channel:
                return await ctx.send(f"**{ctx.author.name}** você não está concectado em nenhum canal de voz.")
            else:
                player.store('sessionowner', ctx.author.id)
                player.store('channel', ctx.channel.id)
                await player.connect(ctx.author.voice.channel.id)
        if not url_re.match(query):
            query = "ytsearch:{}".format(query)
        results = await self.bot.lavalink.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send(f'**{ctx.author.name}** nenhum resultado encontrado ;(')
        s=discord.Embed(colour=0x7289DA)
        if results["loadType"] == "PLAYLIST_LOADED":
            tracks = results["tracks"]
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            playlist_duration = 0
            for track in results['tracks']:
                playlist_duration += track['info']['length']
            playlist_duration = lavalink.Utils.format_time(playlist_duration)
            s.description = f'Adicionei `{len(tracks)}` músicas da playlist `{results["playlistInfo"]["name"]}`. `({playlist_duration})`'
            await ctx.send(embed=s)
        else:
            track = results["tracks"][0]
            player.add(requester=ctx.author.id, track=track)
            s.add_field(name="Duração:", value=lavalink.Utils.format_time(track["info"]["length"]) if not track["info"]["isStream"] else "LIVE", inline=True)
            s.description = f"Adicionei [{track['info']['title']}]({track['info']['uri']}) na fila."
            s.set_footer(text='Cripton © 2019')
            await ctx.send(embed=s)

        
        if not player.is_playing:
            await player.play()

    @commands.command()
    async def playnow(self, ctx, *, query=None):
        """Play something by query or link"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if ctx.message.attachments and not query:
            query = ctx.message.attachments[0].url
        elif not ctx.message.attachments and not query:
            return await arghelp.send(self.bot, ctx)
        else:
            query = query.strip('<>').replace("music.", "")
        if player.is_connected:
            if not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send(f"**{ctx.author.name}** você não está concectado em nenhum canal de voz.")
        else:
            if not ctx.author.voice or not ctx.author.voice.channel:
                return await ctx.send(f"**{ctx.author.name}** você não está concectado em nenhum canal de voz.")
            else:
                player.store('sessionowner', ctx.author.id)
                player.store('channel', ctx.channel.id)
                await player.connect(ctx.author.voice.channel.id)
        if player.fetch("sessionowner") in map(lambda c: c.id, player.connected_channel.members) and player.fetch("sessionowner") != ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")
        if not url_re.match(query):
            query = "ytsearch:{}".format(query)
        results = await self.bot.lavalink.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send(f'**{ctx.author.name}** nenhum resultado encontrado ;(')
        s=discord.Embed(colour=0x7289DA)
        if results["loadType"] == "PLAYLIST_LOADED":
            queue_length = len(player.queue)
            tracks = results["tracks"]
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
            if queue_length != 0:
                player.queue[:queue_length], player.queue[queue_length:] = player.queue[queue_length:], player.queue[:queue_length]
            playlist_duration = 0
            for track in results['tracks']:
                playlist_duration += track['info']['length']
            playlist_duration = lavalink.Utils.format_time(playlist_duration)
            s.description = f'Adicionei `{len(tracks)}` músicas da playlist `{results["playlistInfo"]["name"]}`. `({playlist_duration})`'
            await ctx.send(embed=s)
        else:
            queue_length = len(player.queue)
            track = results["tracks"][0]
            player.add(requester=ctx.author.id, track=track)
            if queue_length != 0:
                player.queue[:queue_length], player.queue[queue_length+1:] = player.queue[queue_length+1:], player.queue[:queue_length]
            s.add_field(name="Duração:", value=lavalink.Utils.format_time(track["info"]["length"]) if not track["info"]["isStream"] else "LIVE", inline=True)
            s.description = f"Adicionei [{track['info']['title']}]({track['info']['uri']}) na fila."
            s.set_footer(text='Cripton © 2019')
            await ctx.send(embed=s)
        if not player.is_playing:
            await player.play()
        await player.skip()

    @commands.command()
    async def movesong(self, ctx, track_index: int, new_index: int):
        """Moves a song index to another index in the queue"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if player.fetch("sessionowner") in map(lambda c: c.id, player.connected_channel.members) and player.fetch("sessionowner") != ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")
        if (new_index < 1 or new_index > len(player.queue)) or (track_index < 1 or track_index > len(player.queue)):
            return await ctx.send(f"**{ctx.author.name}** posição inválida.")
        new_index -= 1
        track_index -= 1
        track = player.queue[track_index:track_index + 1][0]
        player.queue.pop(track_index)
        player.queue.insert(new_index, track)
        await ctx.send("Movido **{}** para a posição `{}` na queue.".format(track.title, new_index + 1))

    @commands.command(aliases=['find', 'ms'])
    async def msearch(self, ctx, *, query):
        """Search for a track"""
        qu = query
        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send(f'**{ctx.author.name}** nenhum resultado encontrado ;(')

        tracks = results['tracks'][:10]

        data = ''
        for i, t in enumerate(tracks, start=0):
            data += f'**{i + 1}:** [{t["info"]["title"]}]({t["info"]["uri"]})\n'

        embed = discord.Embed(title=f"**Resultados pra busca de {ctx.author.name}:** {qu}", colour=discord.Colour(0x7289DA), description=f"{data}\n\nDigite o número correspondente a música que você deseja ouvir. Para cancelar responda **cancelar**.")
        embed.set_footer(text=f'Requisitado por {ctx.message.author}')
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.message.author

        msg = await self.bot.wait_for('message', check=check, timeout=20)
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        if msg.content == 'cancelar' or msg == 'Cancelar' or msg == 'CANCELAR':
            await ctx.send("Cancelado.")
        elif int(msg.content) <= int(msg.content) + 1:
            query = results['tracks'][int(msg.content) - 1]['info']['uri']

            player = self.bot.lavalink.players.get(ctx.guild.id)

            if not player.is_connected:
                if not ctx.author.voice or not ctx.author.voice.channel:
                    await ctx.send(f'**{ctx.author.name}** você precisa estar conectado em um canal de voz!')

                permissions = ctx.author.voice.channel.permissions_for(ctx.me)

                if not permissions.connect or not permissions.speak:
                    await ctx.send(f"**{ctx.author.name}** 😭Eu não tenho as Permissões de **Conectar** e **Falar**.'")

                player.store('channel', ctx.channel.id)
                await player.connect(ctx.author.voice.channel.id)
            else:
                if not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
                    await ctx.send(f"**{ctx.author.name}** por favor entre no canal de voz #**{ctx.me.voice.channel}**.")

            if not url_re.match(query):
                query = f'ytsearch:{query}'

            results = await self.bot.lavalink.get_tracks(query)

            if not results or not results['tracks']:
                await ctx.send(f'**{ctx.author.name}** nenhum resultado encontrado ;(')

            trl = discord.Embed(colour=discord.Colour(0x7289DA))

            if results['loadType'] == "PLAYLIST_LOADED":
                tracks = results['tracks']

                for track in tracks:
                    player.add(requester=ctx.author.id, track=track)

                playlist_duration = 0
                for track in results['tracks']:
                    playlist_duration += track['info']['length']
                playlist_duration = lavalink.Utils.format_time(playlist_duration)
                trl.description = f'Adicionei `{len(tracks)}` músicas da playlist `{results["playlistInfo"]["name"]}`. `({playlist_duration})`'
                await ctx.send(embed=trl)
            else:
                t = results['tracks'][0]
                trl.description = f"Adicionei [{t['info']['title']}]({t['info']['uri']}) na fila."
                await ctx.send(embed=trl)
                player.add(requester=ctx.author.id, track=t)

            if not player.is_playing:
                await player.play()

        else:
            await ctx.send(f"**{ctx.author.name}** Você digitou um número inválido.Abortando...")

    @commands.command(aliases=["leave", "dc", "stop", "sair"])
    async def disconnect(self, ctx):
        """Make the bot end the queue and leave"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if not ctx.author.voice or (player.is_connected and player.connected_channel.id != ctx.author.voice.channel.id):
            return await ctx.send(f'**{ctx.author.name}** você precisa estár conectado em um canal de voz para ouvir música.')
        if player.fetch("sessionowner") == ctx.author.id or player.fetch("sessionowner") not in map(lambda x: x.id, player.connected_channel.members):
            player.queue.clear()
            await player.disconnect()
            player.cleanup()
            await ctx.send(f"Limpei a fila & desconectei do canal `{ctx.author.voice.channel.name}` a pedido de **{ctx.author.name}.**.")
        else:
            await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")

    @commands.command(aliases=['np', 'now'])
    async def nowplaying(self, ctx):
        player = self.bot.lavalink.players.get(ctx.guild.id)
        song = "None"
        

        if not player.is_playing:
            return await ctx.send(f'**{ctx.author.name}** eu não estou tocando nada no momento.')

        if player.current:
            pos = lavalink.Utils.format_time(player.position)
            if player.current.stream:
                dur = 'LIVE'
            else:
                dur = lavalink.Utils.format_time(player.current.duration)
        #bar = await self.bar(volume=player.volume)

        def rcheck(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['⏹','⏭', '📖']

        req = self.bot.get_user(int(player.current.requester))
        embed = discord.Embed(colour=0x7289DA, title='<a:disco:534447709520789517>Tocando agora:', description=f"[{player.current.title}]({player.current.uri})")
        embed.add_field(name="Duração", value=f"`[{pos} / {dur}]`")
        embed.add_field(name="Autor", value=f"`{player.current.author}`")
        embed.add_field(name="Pular", value=f"`[{len(self.votes)}/3]`")
        embed.add_field(name="Volume", value=f"`[{player.volume}]`")
        embed.add_field(name="Requisitado por:", value=f"`{req.name}`")
        embed.set_thumbnail(url=player.current.thumbnail)
        msg = await ctx.send(embed=embed)
        book = await msg.add_reaction("📖")
        stop = await msg.add_reaction("⏹")
        skip = await msg.add_reaction("⏭")
        await asyncio.sleep(0.5)
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if reaction.emoji == '⏹':


                if player.repeat:
                    player.repeat = not player.repeat
                if player.shuffle:
                    player.shuffle = not player.shuffle
                player.queue.clear()
                self.votes.clear()
                await player.stop()
                await ctx.send("As músicas acabaram :(")

            

        elif reaction.emoji == '⏭':
            author = ctx.message.author
            if not player.is_playing:
                return await ctx.send(f'**{ctx.author.name}** eu não estou tocando nada no momento!')
            elif not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send(f"**{ctx.author.name}** você precisa estar no canal #**{ctx.me.voice.channel}**.")
            elif author.id == int(player.current.requester) or "DJ" in [x.name.upper() for x in ctx.author.roles] or ctx.author.guild_permissions.manage_guild:
                await ctx.send(f"Música Pulada.")
                await player.skip()
            elif author.id not in self.votes:
                self.votes.append(author.id)
                if len(self.votes) >= 3:
                    await ctx.send(f"Meta de votos atendida, **Pulando** a musica...")
                    await player.skip()
                    await asyncio.sleep(1)
                    self.votes.clear()
                else:
                    await ctx.send(f"Você votou em **pular** a faixa, atualmente em `[{len(self.votes)}/3]` votos.")
            else:
                await ctx.send(f"**{ctx.author.name}** Você só pode votar para pular uma vez.")
        elif reaction.emoji == '📖':
            try:
                embed = discord.Embed(description="Procurando letra da música..")
                msg = await ctx.send(embed=embed)
                title = player.current.title
                q = title.replace(" ", "+")
                r = requests.get(f"https://some-random-api.ml/lyrics?title={q}").json()
                s = str(r['lyrics'])
                if len(s) > 2040:
                    lyrics = f"Parece que essas letras são muito longas para serem exibidas! Clique [aqui]({r['links']['genius']}) para ir até a letra.\n"
                else:
                    lyrics = f"{r['lyrics']}\n\n"
                embed = discord.Embed(colour=0x7289DA, title=r['title'], description=lyrics, url=r['links']['genius'])
                embed.set_footer(text="Genius", icon_url="https://trashbox.ru/files/427612_ad428e/yp31wbgn.png")
                await msg.edit(embed=embed)
            except Exception as e:
                embed = discord.Embed(description=f"{self.tfals} Não encontramos a letra dessa música!")
                await msg.edit(embed=embed)
        else:
            pass

    @commands.command()
    async def notificações(self, ctx, channel: discord.TextChannel=None):
        """Rebind the text channel all the music notifications are being sent to"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if not channel:
            channel = ctx.channel
        if player.fetch('sessionowner') == ctx.author.id or player.fetch("sessionowner") not in map(lambda c: c.id, player.connected_channel.members):
            player.store('channel', channel.id)
            await ctx.send("As notificações agora serão enviadas para o canal {}.".format(channel.mention))
        else:
            return await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")

    @commands.command(aliases=["resume", "unpause"])
    async def pause(self, ctx):
        """Pause the music that is currently playing"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if not player.is_playing:
            return await ctx.send(f'**{ctx.author.name}** eu não estou tocando nada no momento!')
        if ctx.author not in player.connected_channel.members:
            return await ctx.send(f"**{ctx.author.name}** Você não está no mesmo canal de voz que o bot.")
        if player.fetch("sessionowner") not in map(lambda c: c.id, player.connected_channel.members): 
            if player.paused:
                await player.set_pause(False)
                await ctx.send(f"**{ctx.author.name}** continuando a reprodução da música.")
            else:
                await player.set_pause(True)
                await ctx.send(f"**{ctx.author.name}** acabo de pausar a música.")
        elif player.fetch("sessionowner") == ctx.author.id:
            if player.paused:
                await player.set_pause(False)
                await ctx.send(f"**{ctx.author.name}** continuando a reprodução da música.")
            else:
                await player.set_pause(True)
                await ctx.send(f"**{ctx.author.name}** acabo de pausar a música.")
        else:
            return await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")

    @commands.command()
    async def rewind(self, ctx):
        """Rewind the current track to the start again"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if not player.is_playing:
            return await ctx.send(f'**{ctx.author.name}** eu não estou tocando nada no momento!')
        if ctx.author not in player.connected_channel.members:
            return await ctx.send(f"**{ctx.author.name}** Você não está no mesmo canal de voz que o bot.")
        if player.current.requester not in map(lambda c: c.id, player.connected_channel.members) and player.fetch("sessionowner") not in map(lambda c: c.id, player.connected_channel.members): 
            await ctx.send(f"**{ctx.author.name}** estou reiniciando a música.")
            await player.seek(0)
        elif player.current.requester == ctx.author.id or player.fetch("sessionowner") == ctx.author.id:
            await ctx.send(f"**{ctx.author.name}** estou reiniciando a música.")
            await player.seek(0)
        else:
            return await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")

    @commands.command(aliases=["pular"])
    async def skip(self, ctx):
        """Skip the current song"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if not player.is_playing:
            return await ctx.send(f'**{ctx.author.name}** eu não estou tocando nada no momento!')
        if ctx.author not in player.connected_channel.members:
            return await ctx.send(f"**{ctx.author.name}** Você não está no mesmo canal de voz que o bot.")
        try:
            guild_data = list(filter(lambda x: x["id"] == str(ctx.guild.id), self.votes))[0]
        except IndexError:
            guild_data = None
        if player.current.requester not in map(lambda c: c.id, player.connected_channel.members) and player.fetch("sessionowner") not in map(lambda c: c.id, player.connected_channel.members):
            await ctx.send(f"Pulei a música a pedido de **{ctx.author.name}**.")
            await player.skip()
        else:
            if player.current.requester == ctx.author.id:
                await ctx.send(f"Pulei a música a pedido de **{ctx.author.name}**.")
                await player.skip()
            else:
                if not guild_data:
                    return await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")
                if ctx.author.id in guild_data["votes"]:
                    return await ctx.send(f"**{ctx.author.name}** Você já votou para pular.")
                guild_data["votes"].append(ctx.author.id)
                if len(guild_data["votes"]) >= math.ceil(len(list(filter(lambda x: not x.bot, player.connected_channel.members)))*0.51):
                    await ctx.send(f"Pulei a música a pedido de **{ctx.author.name}**.")
                    await player.skip() 
                else:
                    await ctx.send("Adicionei seu voto para pular a música,agora temos (`{}`/`{}` votos)".format(len(guild_data["votes"]), math.ceil(len(list(filter(lambda x: not x.bot, player.connected_channel.members)))*0.51)))

    @commands.command(aliases=["vol"])
    async def volume(self, ctx, volume: int=None):
        """Set the volume of the bot"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not volume:
            return await ctx.send("O Volume atual é **{}%**".format(player.volume))
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if player.fetch("sessionowner") not in map(lambda c: c.id, player.connected_channel.members):
            await player.set_volume(volume)
            await ctx.send("Alterei o volume do player para **{}%**".format(player.volume))
        elif player.fetch("sessionowner") == ctx.author.id:
            await player.set_volume(volume)
            await ctx.send("Alterei o volume do player para **{}%**".format(player.volume))
        else:
            return await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")

    @commands.command(aliases=['pa', 'selecionar'])
    @commands.guild_only()
    async def playat(self, ctx, index: int):
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if not player.is_playing:
            return await ctx.send(f'**{ctx.author.name}** eu não estou tocando nada no momento!')
        if ctx.author not in player.connected_channel.members:
            return await ctx.send(f"**{ctx.author.name}** Você não está no mesmo canal de voz que o bot.")

        if index < 1:
            return await ctx.send(f'**{ctx.author.name}** Especifique o número da música.')

        if len(player.queue) < index:
            return await ctx.send(f'**{ctx.author.name}** Este número não contém nenhuma musica.')

        await player.play_at(index-1)
    @commands.command(aliases=["remover"])
    async def remove(self, ctx, index: int):
        """Remove a song from the queue"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if not player.is_playing:
            return await ctx.send(f'**{ctx.author.name}** eu não estou tocando nada no momento!')
        if not player.queue:
            return await ctx.send('Nothing is queued :no_entry:')
        if index > len(player.queue) or index < 1:
            return await ctx.send("Invalid song index :no_entry:")
        if player.queue[index-1].requester not in map(lambda c: c.id, player.connected_channel.members) and player.fetch("sessionowner") not in map(lambda c: c.id, player.connected_channel.members):
            index -= 1
            removed = player.queue.pop(index)
            await ctx.send(f"**{ctx.author.name}** Removi `" + removed.title + "` da lista queue.")
        elif player.queue[index-1].requester == ctx.author.id or player.fetch("sessionowner") == ctx.author.id:
            index -= 1
            removed = player.queue.pop(index)
            await ctx.send(f"**{ctx.author.name}** Removi `" + removed.title + "` da lista queue.")
        else:
            return await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")

    @commands.command(aliases=["loop", "repetir"])
    async def repeat(self, ctx):
        """Repeat the queue"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if not player.is_playing:
            return await ctx.send(f'**{ctx.author.name}** eu não estou tocando nada no momento!')
        player.repeat = not player.repeat
        if player.fetch('sessionowner') == ctx.author.id or player.fetch("sessionowner") not in map(lambda c: c.id, player.connected_channel.members):
            await ctx.send("Modo de repetição : **{}**".format("Ligada" if player.repeat else "Desligada"))
        else:
            await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")

    @commands.command()
    async def shuffle(self, ctx):
        """Shuffle the queue"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(f'**{ctx.author.name}** eu não estou conectado em nenhum canal de voz no momento.')
        if not player.is_playing:
            return await ctx.send(f'**{ctx.author.name}** eu não estou tocando nada no momento!')
        if player.fetch('sessionowner') == ctx.author.id or player.fetch("sessionowner") not in map(lambda c: c.id, player.connected_channel.members):
            random.shuffle(player.queue)
            await ctx.send(f"**{ctx.author.name}** a queue será reproduzida automaticamante.")
        else:
            await ctx.send(f"**{ctx.author.name}** Você não pode usar esse comando pois não é o dono da seção :v")

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int=1):
        """Fetch the queue"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('Não há nada na fila! Por que colocar umas músicas em?')

        shuf = 'Ligado' if player.shuffle else 'Desligado'
        n_dur = lavalink.Utils.format_time(player.current.duration)

        if not player.queue and player.is_playing:
            embed = discord.Embed(title=f"Lista de reprodução:", colour=discord.Colour(0x7289DA), description=f"**Tocando Agora:** [{player.current.title}]({player.current.uri}) -  `{n_dur}`")
            embed.set_footer(text=f"Página 1 de 1 | Aleatório: {shuf}.")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        elif not player.queue:
            return await ctx.send(f"**{ctx.author.name}** minha fila de reprodução se encontra vazia! Adicione algo antes de usar esse comando.")

        else:

            items_per_page = 11
            pages = math.ceil(len(player.queue) / items_per_page)

            start = (page - 1) * items_per_page
            end = start + items_per_page

            emoji = '- :repeat: \n' if player.repeat else '\n'

            qlist = ''

            q = len(player.queue)

            for i, track in enumerate(player.queue[start:end], start=start):
                if player.current.stream:
                    dur = 'LIVE'
                else:
                    dur = lavalink.Utils.format_time(track.duration)
                qlist += f'**{i + 1}:** [{track.title}]({track.uri}) `{dur}` {emoji}'

            embed = discord.Embed(title=f"Lista de reprodução ({q}):", colour=discord.Colour(0x7289DA), description=f"**Tocando Agora:** [{player.current.title}]({player.current.uri}) `{n_dur}` {emoji}{qlist}")
            embed.set_footer(text=f"Página {page} de {pages} | Aleatório: {shuf}.")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def conectados(self, ctx):
        players = self.bot.lavalink.players
        msg = ""
        totallis, totalcon = 0, 0
        for x in players:
            player = x[1]
            if player.is_connected:
                listeners = len(set(filter(lambda x: not x.bot, player.connected_channel.members)))
                totallis += listeners
                totalcon += 1
                msg += "`{}` conectado com `{}` {}\n".format(player.connected_channel.guild, listeners, "ouvinte." if listeners == 1 else "ouvintes")
        if msg:
            await ctx.send(embed=discord.Embed(description=msg, colour=0x7289DA).set_footer(text="Conexões Totais: {} | Ouvintes Totais: {}".format(totalcon, totallis)))
        else:
            await ctx.send("Sem conexões ;(")

    @commands.command(hidden=True)
    @checks.is_owner()
    async def forcedisconnect(self, ctx, *, server):
        server = discord.utils.get(self.bot.guilds, name=server)
        player = self.bot.lavalink.players.get(server.id)
        await player.connect([x.id for x in server.voice_channels][0])
        await player.disconnect()
        await ctx.send(f'**{ctx.author.name}** desconectei do servidor que você mandou.')

    def format_time(self, time):
        h, r = divmod(time / 1000, 3600)
        m, s = divmod(r, 60)
        if h == 0:
            return '%02d:%02d' % (m, s)
        else:
            return '%02d:%02d:%02d' % (h, m, s)       

    @join.after_invoke
    @play.after_invoke
    @playnow.after_invoke
    @msearch.after_invoke
    async def deafen(self, ctx):
        if ctx.me.voice:
            if not ctx.me.voice.deaf:
                await ctx.me.edit(deafen=True)

    async def check_timeout(self):
        while not self.bot.is_closed():
            for x in self.bot.lavalink.players:
                player = x[1]
                channel = self.bot.get_channel(player.fetch("channel"))
                if player.is_connected:
                    if len(set(filter(lambda x: not x.bot, player.connected_channel.members))) == 0:
                        if not player.fetch("nousers"):
                            player.store("nousers", datetime.datetime.utcnow().timestamp())
                        else:
                            if datetime.datetime.now().timestamp() - player.fetch("nousers") >= 10:
                                if channel:
                                    await channel.send("Ninguém esteve no canal de voz por 2 minutos, então estou saindo..")
                                player.queue.clear()
                                await player.disconnect()
                                player.cleanup()
                    else:
                        player.delete("nousers")
            await asyncio.sleep(45)

def setup(bot):
    bot.add_cog(music(bot))
