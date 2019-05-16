import discord
from discord.ext import commands
from utils import botstatus
import sys
from datetime import datetime, timedelta
import discord
import requests


class informacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="🏓 Pong!",
                              description=f' No Momento estou com: **{round(self.bot.latency * 1000)}ms**.',
                              color=0x36393f)
        embed.set_footer(text="Cripton © 2019", icon_url=self.bot.user.avatar_url)
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=90)

    @commands.guild_only()
    @commands.command()
    async def emojis(self, ctx):
        server = ctx.message.guild
        emojis = [str(x) for x in server.emojis]
        await ctx.message.delete()
        embed = discord.Embed(title=f'<:cseta:550209450506452992> Aqui todos os emojis do servidor {ctx.guild.name}:',
                              description=f"  ".join(emojis), color=0x36393f)
        embed.set_footer(text="Cripton © 2019", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed, delete_after=70)

    @commands.command()
    async def pic(self, ctx, *, user: discord.Member = None):
        if user is None:
            usuario = ctx.author.avatar_url
            texto = f"Olá {ctx.author.name}, está é sua imagem de perfil."
        else:
            usuario = user.avatar_url
            texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name}"

        embed = discord.Embed(title=texto, color=0xF4CBD1)
        embed.set_image(url=usuario)
        embed.set_footer(text=self.bot.user.name + " direitos resevados.")
        await ctx.send(embed=embed)

    @commands.command()
    async def clima(self, ctx, *, buscar=None):

        if buscar is None:
            await ctx.send(f"Olá {ctx.author.mention}, você precisa digitar uma cidade ou país.")
            return

        busca = str(buscar).replace(" ", "%20")
        r = requests.get(f'http://api.apixu.com/v1/current.json?key=6a0d3673a1ec4ceb8f5152802182112&q={busca}')
        if r.status_code == 200:
            js = r.json()

        embed = discord.Embed(title="Apixu Climate", color=0xffff00)
        embed.add_field(name="Nome", value=str(js['location']['name']), inline=False)
        embed.add_field(name="Região", value=str(js['location']['region']), inline=True)
        embed.add_field(name="País", value=str(js['location']['country']), inline=True)
        local = str(js['location']['lat']) + "/" + str(js['location']['lon'])
        embed.add_field(name="Lat & Lon", value=str(local), inline=True)
        temp = str(js['current']['temp_c']) + "/" + str(js['current']['temp_f'])
        embed.add_field(name="c° & f°", value=str(temp), inline=True)
        url = "https:" + str(js['current']['condition']["icon"])
        embed.set_thumbnail(url=url)
        embed.set_footer(text="Climatempo 2018")
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def botinfo(self,ctx):
          mem = botstatus.get_memory()
          embed = discord.Embed(description="Olá {}, este e o perfil do {} e nele contém algumas informações.".format(ctx.author.name, self.bot.user.name),colour=0x00d200)
          embed.set_author(name="Informações do {}".format(self.bot.user.name), icon_url=ctx.author.avatar_url_as())
          embed.add_field(name="<:dono:565969060228104194> Criador", value = '``Henrique__#0841``', inline=True)
          embed.add_field(name="<:tag:565975875749675039> Tag", value = '``'+str(self.bot.user)+'``', inline=True)
          embed.add_field(name="<:ip:565968375772217354> Id", value = '``'+str(self.bot.user.id)+'``', inline=True)
          embed.add_field(name="<:api:565975875804463114> Api", value = '``Discord.py '+str(discord.__version__)+'``', inline=True)
          embed.add_field(name="<:python:565975875481501697> Python", value = '``'+str(sys.version[:5])+'``', inline=True)
          embed.add_field(name="<:ram:565975875930292234> Memoria", value = '``'+str(mem["memory_used"])+'/'+str(mem["memory_total"])+' ('+str(mem["memory_percent"])+')``', inline=True)
          embed.add_field(name="<:timer:565975875988750336> Tempo de atividade", value = '``'+str(botstatus.timetotal()).replace("{day}","dia").replace("{hour}","hora").replace("{minute}","minuto").replace("{second}","segundo")+'``', inline=True)
          embed.add_field(name="<:guilds:565976828276113429> Servidores", value = '``'+str(len(self.bot.guilds))+' (shards '+"1"+')``', inline=True)
          embed.add_field(name="<:ping:565975875728703488> Lâtencia", value = '``{0:.2f}ms``'.format(self.bot.latency * 1000), inline=True)
          embed.add_field(name="<:cpu:565975875653337088> Cpu",value=f'``{botstatus.cpu_usage()}%``', inline=True)
          #embed.add_field(name="<:ping:564890304839417887> Processador", value=f'``{botstatus.host_name()}``', inline=True)
          embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
          await ctx.send(embed=embed)
    
    @commands.guild_only()
    @commands.command()
    async def serverinfo(self, ctx):
           servidor = ctx.guild
           if servidor.icon_url_as(format="png") == "":
              img = "https://i.imgur.com/To9mDVT.png"
           else:
             img  = servidor.icon_url
           online = len([y.id for y in servidor.members if y.status == discord.Status.online])
           afk  = len([y.id for y in servidor.members if y.status == y.status == discord.Status.idle])
           offline = len([y.id for y in servidor.members if y.status == y.status == discord.Status.offline])
           dnd = len([y.id for y in servidor.members if y.status == y.status == discord.Status.dnd])
           geral = len([y.id for y in servidor.members])
           bots= len([y.id for y in servidor.members if y.bot])
           criado_em = str(servidor.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
           usuarios = "<:online:565972011873206273> : ``"+str(online)+"`` <:ausente:565972012066013197> : ``"+str(afk)+"`` <:noperturbe:565972011990384651> : ``"+str(dnd)+"`` <:offline:565972011952635913> : ``"+str(offline)+"`` <:bots:565972012325928980> : ``"+str(bots)+"``"
           texto = "<:texto:565968741788155907> : ``"+str(len(servidor.text_channels))+"``<:voz:565968741729435668>  : ``"+str(len(servidor.voice_channels))+"``"
           cargos = len([y.id for y in servidor.roles])
           emojis = len([y.id for y in servidor.emojis])
           embed = discord.Embed(description="Olá {}, aqui estão todas as informaçôes do servidor `{}`.".format(ctx.author.name, servidor.name),colour=0x00d200)
           embed.set_author(name="Informação do servidor", icon_url=ctx.author.avatar_url_as())
           embed.add_field(name="<:dono:565969060228104194> Dono", value = "``"+str(servidor.owner)+"``", inline=True)
           embed.add_field(name="<:nome:565969826611462174> Nome", value = "``"+str(servidor.name)+"``", inline=True)
           embed.add_field(name="<:ip:565968375772217354> Id", value = "``"+str(servidor.id)+"``", inline=True)
           embed.add_field(name="<:notas:565968375898046464> Criação", value = "``"+str(criado_em)+"``", inline=True)
           embed.add_field(name="<:roles:565970506390700077> Cargos", value = "``"+str(cargos)+"``", inline=True)
           embed.add_field(name="<:emoji:565968375956897829> Emojis", value = "``"+str(emojis)+"``", inline=True)
           embed.add_field(name="<:canais:565968375314907146> Canais", value = texto, inline=True)
           embed.add_field(name="<:local:565968375562371074> Localização", value = "``"+str(servidor.region).title()+"``", inline=True)
           embed.add_field(name="<:cadeado:565968375369695251> Verificação", value = "``"+str(servidor.verification_level).replace("none","Nenhuma").replace("low","Baixa").replace("medium","Média").replace("high","Alta").replace("extreme","Muito alta")+"``", inline=True)
           embed.add_field(name="<:pessoas:565968375847845908> Usuários"+" ["+str(geral)+"]", value = usuarios, inline=True)
           embed.set_thumbnail(url=img)
           embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
           await ctx.send(embed = embed)


    @commands.guild_only()
    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member = None):
           if user is None:
               usuario = ctx.author
               titulo = "Olá {}, esse é o seu perfil e aqui estão suas informações.".format(ctx.author.name)
           else:
              usuario = user
              titulo = "Olá {}, este é o perfil de {} e nele contém umas informações.".format(ctx.author.name, usuario.name)

           if usuario.display_name == usuario.name:
               apelido = "Não defindo"
           else:
              apelido = usuario.display_name
           if usuario.avatar_url_as()  == "":
           	  img = "https://i.imgur.com/To9mDVT.png"
           else:
             img = usuario.avatar_url_as()
           try:
             jogo = usuario.activity.name
           except:
               jogo = "No momento nada."
           if usuario.id in [y.id for y in ctx.guild.members if not y.bot]:
              bot = "Não"
           else:
             bot = "Sim"
           svs = '\n\u200b'.join([f"{s.name} | {s.id}\nDono: {s.owner}" for s in self.bot.guilds if user in s.members])
           entrou_servidor = str(usuario.joined_at.strftime("%H:%M:%S - %d/%m/20%y"))
           conta_criada = str(usuario.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
           conta_dias = (datetime.utcnow() - usuario.created_at).days
           cargos = len([r.name for r in usuario.roles if r.name != "@everyone"])
           if not svs: svs = 'Nenhum servidor em comum.'
           on = "Disponível"
           off = "Offline"
           dnd = "Não Pertubar"
           afk = "Ausente"
           stat = str(usuario.status).replace("online",on).replace("offline",off).replace("dnd",dnd).replace("idle",afk)
           cargos2 = len([y.id for y in ctx.guild.roles])
           embed = discord.Embed(description=titulo,colour=0x00d200)
           embed.set_author(name="Informação de perfil", icon_url=ctx.author.avatar_url_as())
           embed.add_field(name="<:tag:565975875749675039> Tag", value = "``"+str(usuario.name)+"#"+str(usuario.discriminator)+"``", inline=True)
           embed.add_field(name="<:ip:565968375772217354> Id", value = "``"+str(usuario.id)+"``", inline=True)
           embed.add_field(name="<:nome:565969826611462174> Apelido", value = "``"+str(apelido)+"``", inline=True)
           embed.add_field(name="<:notas:565968375898046464> Criação (conta)", value =f"``{conta_criada}+``==``{conta_dias}``dias", inline=True)
           embed.add_field(name="<:entrou:565978463882706973> Entrou (servidor)", value = "``"+str(entrou_servidor)+"``", inline=True)
           embed.add_field(name="<:toprole:565979057490231297> Maior cargo", value = "``"+str(usuario.top_role)+"``", inline=True)
           embed.add_field(name="<:roles:565970506390700077> Cargos", value = "``"+str(cargos)+"/"+str(cargos2)+"``", inline=True)
           embed.add_field(name="<:bots:565972012325928980> Bot", value = "``"+str(bot)+"``", inline=True)
           embed.add_field(name="<:status:565979407567552517> Status", value = "``"+str(stat)+"``", inline=True)
           embed.add_field(name="<:jogando:565979683829710848> servidores",value=f"```{svs}```")
           embed.set_thumbnail(url=img)
           embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
           await ctx.send(embed = embed)

    @commands.guild_only()
    @commands.command()
    async def channelinfo(self, ctx, *, num=None):
         if num is None:
            num = ctx.channel.id
         if str(num).isdigit() == True:
           channel = discord.utils.get(ctx.guild.channels, id=int(num))
         else:
           if "<#" in num:
              num = str(num).replace("<#","").replace(">","")
              channel = discord.utils.get(ctx.guild.channels, id=int(num))
           else:
             channel = discord.utils.get(ctx.guild.channels, name=num)

         if channel is None:
           embed = discord.Embed(description="<:help:565985431284350985> **|** O canal {} não existe.".format(num), color=0x00d200)
           await ctx.send(embed=embed)
           return  

         if channel in list(ctx.guild.text_channels):
            channel_type = "Texto"
         elif channel in list(ctx.guild.voice_channels):
           channel_type = "Audio"
         else:
           embed = discord.Embed(description="<:help:565985431284350985> **|** O canal {} não existe.".format(num), color=0x00d200)
           await ctx.send(embed=embed)
           return  
         
         channel_created = str(channel.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
         embed = discord.Embed(description="Olá {}, esta são as informações do canal {}.".format(ctx.author.name, channel.mention),colour=0x00d200)
         embed.set_author(name="Informações do canal", icon_url=ctx.author.avatar_url_as())
         embed.add_field(name="<:nome:565969826611462174> Nome", value = "``"+str(channel.name)+"``", inline=True)
         embed.add_field(name="<:ip:565968375772217354> ID", value = "``"+str(channel.id)+"``", inline=True)
         embed.add_field(name="<:notas:565968375898046464> Criação", value = "``"+str(channel_created)+"``", inline=True)
         embed.add_field(name="<:canais:565968375314907146> Posição", value = "``"+str(channel.position)+"``", inline=True)
         embed.add_field(name="<:tipo:565986477708935168> Tipo do canal", value = "``"+str(channel_type)+"``", inline=True)
         try:
           embed.add_field(name="<:porn:565986782966054912> +18", value = "```"+str(channel.is_nsfw()).replace("False","Não").replace("True","Sim")+"```", inline=True)
           if channel.slowmode_delay == 0:
              valor = "Não definido"
           else:
             valor = "{} segundos".format(channel.slowmode_delay)
           embed.add_field(name="<:timer:565975875988750336> Slowmode", value = "``"+str(valor)+"``", inline=True)
           if channel.topic is None:
              topic = "Não definido"
           else:
             topic = channel.topic
           embed.add_field(name="<:tpico:565987376745283594> Tópico", value = "``"+str(topic[:1024])+"``", inline=True)          
         except:
           pass
         try:
           embed.add_field(name="<:voz:565968741729435668> Bitrate", value = "``"+str(channel.bitrate)+"``", inline=True)
           if channel.user_limit != 0:
             embed.add_field(name="<:pessoas:565968375847845908> Usuários conectados", value="``{}/{}``".format(len(channel.members), channel.user_limit))
           else:
             embed.add_field(name="<:pessoas:565968375847845908> Usuários conectados", value="``{}``".format(len(channel.members)))          
         except:
           pass         


         embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
         await ctx.send(embed = embed)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(colour=0x00d200, description="Olá {}, aqui contém todos os comandos do {}.".format(ctx.author.name, self.bot.user.name))
        embed.set_author(name="Ajuda ao usuário", icon_url=ctx.author.avatar_url_as())
        embed.add_field(name="<:discord:565988914138054656> Discord", value ="``channelinfo``, ``serverinfo``, ``userinfo``", inline=True)
        embed.add_field(name="<:musica:565989217486897163> Música", value ="``play``, ``stop``, ``pause``, ``volume`` , ``seek``, ``queue``, ``np``, ``rework``", inline=True)
        embed.add_field(name="<:cripton:564878721677525013> Cripton", value ="``botinfo``, ``ping``, ``config``", inline=True)
        #embed.add_field(name="<:search:564893705111076864> Pesquisa", value ="``image``, ``link``", inline=True)
        embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(informacao(bot))
