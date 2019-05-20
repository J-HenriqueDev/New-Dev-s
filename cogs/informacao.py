import discord
from discord.ext import commands
from utils import botstatus
import sys
from datetime import datetime, timedelta
import discord
import requests

def perms_check(role):
    list_perms = ['empty']
    for perm in role:
        if perm[1] is True:
            if 'empty' in list_perms:
                list_perms = list()
            list_perms.append(perm[0])
    if 'empty' not in list_perms:
        all_perms = ", ".join(list_perms)
        return all_perms
    else:
        return "O cargo mencionado não tem nenhuma permissão."


class informacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Mostra o meu ping',usage='c.ping')
    async def ping(self, ctx):
        embed = discord.Embed(title="🏓 Pong!",
                              description=f' No Momento estou com: **{round(self.bot.latency * 1000)}ms**.',
                              color=0x36393f)
        embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=90)



    @commands.command(description='envia a sua foto de perfil ou a de um usuário.',usage='c.avatar',aliases=['pic'])
    async def avatar(self, ctx, *, user: discord.Member = None):
        if user is None:
            usuario = ctx.author.avatar_url
            texto = f"Olá {ctx.author.name}, está é sua imagem de perfil."
        else:
            usuario = user.avatar_url
            texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name}"

        embed = discord.Embed(title=texto, color=0x7289DA)
        embed.set_image(url=usuario)
        embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed=embed)


    @commands.guild_only()
    @commands.command(description='Mostra algumas informações sobre mim.',usage='c.botinfo',aliases=['bot'])
    async def botinfo(self,ctx):
        mem = botstatus.get_memory()
        embed = discord.Embed(description="Olá {}, este é o perfil do {} e nele contém algumas informações.".format(ctx.author.name, self.bot.user.name),colour=0x7289DA)
        embed.set_author(name="Informações do {}".format(self.bot.user.name), icon_url=ctx.author.avatar_url_as())
        embed.add_field(name=f"{self.bot._emojis['dono']} Criador", value = '``Luke_Skywalker#0841``', inline=True)
        embed.add_field(name=f"{self.bot._emojis['tag']} Tag", value = '``'+str(self.bot.user)+'``', inline=True)
        embed.add_field(name=f"{self.bot._emojis['ip']} Id", value = '``'+str(self.bot.user.id)+'``', inline=True)
        embed.add_field(name=f"{self.bot._emojis['api']} Api", value = '``Discord.py '+str(discord.__version__)+'``', inline=True)
        embed.add_field(name=f"{self.bot._emojis['python']} Python", value = '``'+str(sys.version[:5])+'``', inline=True)
        embed.add_field(name=f"{self.bot._emojis['ram']} Memoria", value = '``'+str(mem["memory_used"])+'/'+str(mem["memory_total"])+' ('+str(mem["memory_percent"])+')``', inline=True)
        embed.add_field(name=f"{self.bot._emojis['timer']} Tempo de atividade", value = '``'+str(botstatus.timetotal()).replace("{day}","dia").replace("{hour}","hora").replace("{minute}","minuto").replace("{second}","segundo")+'``', inline=True)
        embed.add_field(name=f"{self.bot._emojis['guilds']} Servidores", value = '``'+str(len(self.bot.guilds))+' (shards '+"1"+')``', inline=True)
        embed.add_field(name=f"{self.bot._emojis['ping']} Lâtencia", value = '``{0:.2f}ms``'.format(self.bot.latency * 1000), inline=True)
        embed.add_field(name=f"{self.bot._emojis['cpu']} Porcentagem da CPU",value=f'``{botstatus.cpu_usage()}%``', inline=True)
          #embed.add_field(name=f"<:ping:564890304839417887> Processador", value=f'``{botstatus.host_name()}``', inline=True)
        embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed=embed)
    
    @commands.guild_only()
    @commands.command(description='Mostra todas as informações do seu servidor.',usage='c.serverinfo',aliases=['sinfo', 'guildinfo'])
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
          usuarios = "<:online:565972011873206273> : ``"+str(online)+"`` <:ausente:565972012066013197> : ``"+str(afk)+"`` <:noperturbe:565972011990384651> : ``"+str(dnd)+"`` <:offline:565972011952635913> : ``"+str(offline)+f"`` {self.bot._emojis['bots']} : ``"+str(bots)+"``"
          texto = f"{self.bot._emojis['texto']} : ``"+str(len(servidor.text_channels))+f"``{self.bot._emojis['voz']}  : ``"+str(len(servidor.voice_channels))+"``"
          cargos = len([y.id for y in servidor.roles])
          emojis = len([y.id for y in servidor.emojis])
          embed = discord.Embed(description="Olá {}, aqui estão todas as informaçôes do servidor `{}`.".format(ctx.author.name, servidor.name),colour=0x7289DA)
          embed.set_author(name=f"Informação do servidor", icon_url=ctx.author.avatar_url_as())
          embed.add_field(name=f"{self.bot._emojis['dono']} Dono", value = "``"+str(servidor.owner)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['nome']} Nome", value = "``"+str(servidor.name)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['ip']} Id", value = "``"+str(servidor.id)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['notas']} Criação", value = "``"+str(criado_em)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['roles']} Cargos", value = "``"+str(cargos)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['emoji']} Emojis", value = "``"+str(emojis)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['canais']} Canais", value = texto, inline=True)
          embed.add_field(name=f"{self.bot._emojis['local']} Localização", value = "``"+str(servidor.region).title()+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['cadeado']} Verificação", value = "``"+str(servidor.verification_level).replace("none","Nenhuma").replace("low","Baixa").replace("medium","Média").replace("high","Alta").replace("extreme","Muito alta")+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['pessoas']} Usuários"+" ["+str(geral)+"]", value = usuarios, inline=True)
          embed.set_thumbnail(url=img)
          embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
          await ctx.send(embed = embed)


    @commands.guild_only()
    @commands.command(description='Mostra as informações de um usuário.',usage='c.userinfo @TOBIAS',aliases=['uinfo', 'usuario'])
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
          svs = ', '.join([c.name for c in self.bot.guilds if usuario in c.members])
          entrou_servidor = str(usuario.joined_at.strftime("%d/%m/20%y ás %H:%M:%S"))
          conta_criada = str(usuario.created_at.strftime("%d/%m/20%y"))
          conta_dias = (datetime.utcnow() - usuario.created_at).days
          cargos = len([r.name for r in usuario.roles if r.name != "@everyone"])
          if not svs: svs = 'Nenhum servidor em comum.'
          on = "Disponível"
          off = "Offline"
          dnd = "Não Pertubar"
          afk = "Ausente"
          stat = str(usuario.status).replace("online",on).replace("offline",off).replace("dnd",dnd).replace("idle",afk)
          cargos2 = len([y.id for y in ctx.guild.roles])
          embed = discord.Embed(description=titulo,colour=0x7289DA)
          embed.set_author(name=f"Informação de perfil", icon_url=ctx.author.avatar_url_as())
          embed.add_field(name=f"{self.bot._emojis['tag']} Tag", value = "``"+str(usuario.name)+"#"+str(usuario.discriminator)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['ip']} Id", value = "``"+str(usuario.id)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['nome']} Apelido", value = "``"+str(apelido)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['notas']} Data de criação da conta", value =f"``{conta_criada}`` ({conta_dias} dias)", inline=True)
          embed.add_field(name=f"{self.bot._emojis['entrou']} Entrou aqui em", value = "``"+str(entrou_servidor)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['toprole']} Maior cargo", value = "``"+str(usuario.top_role)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['roles']} Cargos", value = "``"+str(cargos)+"/"+str(cargos2)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['bots']} Bot", value = "``"+str(bot)+"``", inline=True)
          embed.add_field(name=f"{self.bot._emojis['status']} Status", value = "``"+str(stat)+"``", inline=True)
          embed.add_field(name=f"<:jogando:565979683829710848> servidores",value=f"```{svs}```")
          embed.set_thumbnail(url=img)
          embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
          await ctx.send(embed = embed)
    
    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
          comma = error.args[0].split('"')[1]
          embed = discord.Embed(title=f"{self.bot._emojis['incorreto']} | Membro não encontrado!", color=0x7289DA, description=f"O membro `{comma}` não está nesse servidor.")
          await ctx.send(embed=embed)
          return


    @commands.guild_only()
    @commands.command(description='Mostra as informações de um canal.',usage='c.channelinfo #canal',aliases=['canalinfo', 'cinfo'])
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
          embed = discord.Embed(description="<:help:565985431284350985> **|** O canal {} não existe.".format(num), color=0x7289DA)
          await ctx.send(embed=embed)
          return  

        if channel in list(ctx.guild.text_channels):
          channel_type = "Texto"
        elif channel in list(ctx.guild.voice_channels):
          channel_type = "Audio"
        else:
          embed = discord.Embed(description="<:help:565985431284350985> **|** O canal {} não existe.".format(num), color=0x7289DA)
          await ctx.send(embed=embed)
          return  
         
        channel_created = str(channel.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
        embed = discord.Embed(description="Olá {}, esta são as informações do canal {}.".format(ctx.author.name, channel.mention),colour=0x7289DA)
        embed.set_author(name=f"Informações do canal", icon_url=ctx.author.avatar_url_as())
        embed.add_field(name=f"{self.bot._emojis['nome']} Nome", value = "``"+str(channel.name)+"``", inline=True)
        embed.add_field(name=f"{self.bot._emojis['ip']} ID", value = "``"+str(channel.id)+"``", inline=True)
        embed.add_field(name=f"{self.bot._emojis['notas']} Criação", value = "``"+str(channel_created)+"``", inline=True)
        embed.add_field(name=f"{self.bot._emojis['canais']} Posição", value = "``"+str(channel.position)+"``", inline=True)
        embed.add_field(name=f"{self.bot._emojis['tipo']} Tipo do canal", value = "``"+str(channel_type)+"``", inline=True)
        try:
          embed.add_field(name=f"{self.bot._emojis['porn']} +18", value = "```"+str(channel.is_nsfw()).replace("False","Não").replace("True","Sim")+"```", inline=True)
          if channel.slowmode_delay == 0:
            valor = "Não definido"
          else:
            valor = "{} segundos".format(channel.slowmode_delay)
          embed.add_field(name=f"{self.bot._emojis['timer']} Slowmode", value = "``"+str(valor)+"``", inline=True)
          if channel.topic is None:
            topic = "Não definido"
          else:
            topic = channel.topic
          embed.add_field(name=f"{self.bot._emojis['tpico']} Tópico", value = "``"+str(topic[:1024])+"``", inline=True)          
        except:
          pass
        try:
          embed.add_field(name=f"{self.bot._emojis['voz']} Bitrate", value = "``"+str(channel.bitrate)+"``", inline=True)
          if channel.user_limit != 0:
            embed.add_field(name=f"{self.bot._emojis['pessoas']} Usuários conectados", value="``{}/{}``".format(len(channel.members), channel.user_limit))
          else:
            embed.add_field(name=f"{self.bot._emojis['pessoas']} Usuários conectados", value="``{}``".format(len(channel.members)))          
        except:
          pass         


        embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed = embed)

    @channelinfo.error
    async def channelinfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
          comma = error.args[0].split('"')[1]
          embed = discord.Embed(title=f"{self.bot._emojis['incorreto']} | Canal não encontrado!", color=0x7289DA, description=f"O canal `{comma}` não foi encontrado.")
          await ctx.send(embed=embed)
          return

    @commands.command(description='Listagem e informações de todos os comandos públicos lançados até o momento',usage='cu.ajuda',aliases=['help'])
    async def ajuda(self, ctx, nome = None):
        if nome:
            comando = self.bot.get_command(nome)
            if not comando:
                return await ctx.send(f"fia da mae, **{ctx.author.name}**! Não foi possível encontrar um comando chamado **`{nome[:15]}`**.", delete_after=15)

            nome = comando.name
            desc = comando.description
            uso = comando.usage
            if not desc: desc = "Descrição não definida."
            if not uso: uso = "Modo de uso não definido."
            if comando.aliases:
                aliases = ', '.join([f"**`{alias}`**" for alias in comando.aliases])
            else:
                aliases = "Nenhuma abreviação."

            embed = discord.Embed(colour=0x7289DA)
            embed.set_author(name=f"Informações do comando {nome}.")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
            embed.add_field(name=f"**Uso**",value=f"`{uso}`",inline=False)
            embed.add_field(name=f"**Abreviações**",value=aliases,inline=False)
            embed.add_field(name=f"**Descrição**",value=f"`{desc}`",inline=False)
            return await ctx.send(embed=embed)
    

        em = discord.Embed(colour=0x7289DA, description="Olá {}, aqui contém todos os comandos do {}.".format(ctx.author.name, self.bot.user.name))
        em.set_author(name=f"{self.bot.user.name} | Comandos",icon_url=self.bot.user.avatar_url)
        em.set_thumbnail(url=self.bot.user.avatar_url)
        em.add_field(name=f"{self.bot._emojis['discord']} Discord", value ="``channelinfo``, ``serverinfo``, ``userinfo``,``roleinfo``,``botinfo``, ``ping``, ``config``", inline=True)
        em.add_field(name=f"{self.bot._emojis['newdevs']} New Dev's", value ="``rep``, ``tophelper``, ``helper``", inline=True)
        em.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed=em)

    @commands.command(description='Mostra as informações de um cargo',usage='c.roleinfo dj',aliases=['rinfo'])
    async def roleinfo(self, ctx, *, role: discord.Role = None):
        if role is None:
            return await ctx.send(f'**{ctx.author.name}** você não mencionou um cargo.')
        criado_em = str(role.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
        embed = discord.Embed(color=0x7289DA)
        embed.set_author(name="Informação do cargo", icon_url=ctx.author.avatar_url_as())
        embed.add_field(name=f"{self.bot._emojis['tag']} Nome:", value="``"+str(role.name)+"``")
        embed.add_field(name=f"{self.bot._emojis['ip']} ID:", value=f"``"+str(role.id)+"``")
        mention = f"{role.mentionable}"
        embed.add_field(name=f"{self.bot._emojis['mention']} Mencionável:", value=f"``{mention.replace('False','Não').replace('True', 'Sim')}``")
        embed.add_field(name=f"{self.bot._emojis['cor']} Cor:", value="``"+str(role.colour)+"``")
        separado = f"{role.hoist}"
        embed.add_field(name=f"{self.bot._emojis['canais']} Posição do Cargo:", value=f"``{role.position}º``")
        embed.add_field(name=f"{self.bot._emojis['separado']} Separado dos Membros:", value=f"``{separado.replace('True','Sim').replace('False','Não')}``")
        embed.add_field(name=f"{self.bot._emojis['notas']} Data de Criação:", value=f"``"+str(criado_em)+"``")
        embed.add_field(name=f"{self.bot._emojis['pessoas']} Membro(s) com o cargo:", value=f"``{len(role.members)}``")
        perm = f"{perms_check(role.permissions)}"
        embed.add_field(name=f"{self.bot._emojis['cadeado']} Permissões:", value=f"``{perm.replace('use_voice_activation','Usar detecção de voz').replace('add_reactions','Adicionar reações').replace('administrator','Administrador').replace('attach_files','Anexar arquivos').replace('ban_members','Banir membros').replace('change_nickname','Mudar apelido').replace('connect','Conectar').replace('create_instant_invite','Criar um convite instatâneo').replace('deafen_members','Desativar áudio de membros').replace('embed_links','Inserir Links').replace('external_emojis','Emojis externos').replace('kick_members','Expulsar membros').replace('manage_channels','Gerenciar canais').replace('manage_emojis','Gerenciar emojis').replace('manage_guild','Gerenciar o servidor').replace('manage_messages','Gerenciar Mensagens').replace('manage_nicknames','Gerenciar apelidos').replace('manage_roles','Gerenciar cargos').replace('manage_webhooks','Gerenciar Webhooks').replace('mention_everyone','Mencionar todos').replace('move_members','Mover membros').replace('mute_members','Silenciar membros').replace('read_message_history','Ler histórico de mensagens').replace('read_messages','Ler mensagens').replace('send_messages','Enviar mensagens').replace('send_tts_messages','Enviar mensagem TTS').replace('speak','Falar').replace('view_audit_log','Ver registro de auditoria')}``")
        embed.set_thumbnail(url='https://htmlcolors.com/color-image/{}.png'.format(str(role.color).strip("#")))
        embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed=embed)

    @roleinfo.error
    async def roleinfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
          comma = error.args[0].split('"')[1]
          embed = discord.Embed(title=f"{self.bot._emojis['incorreto']} | Cargo não encontrado!", color=0x7289DA, description=f"O cargo `{comma}` não existe.")
          await ctx.send(embed=embed)
          return

def setup(bot):
    bot.add_cog(informacao(bot))
