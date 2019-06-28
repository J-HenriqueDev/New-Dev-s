import discord
from pymongo import MongoClient, ASCENDING, DESCENDING
from discord.ext import commands
from asyncio import TimeoutError as Esgotado
from datetime import datetime



class comandos(commands.Cog):
    def __init__(self, lab):
        self.lab = lab
        self.users = []
        self.linguagens = {
            "py": {
                "aliases": ["python", "py", "discord.py"],
                "nome": "Python",
                "cor": 0x007AFF,
                "author": "COMANDOS NA LINGUAGEM PYTHON:",
                "logo": "https://imgur.com/LD60DLf.png"
            },
            "js": {
                "aliases": ["javascript", "js", "discord.js", "node", "node.j"],
                "nome": "JavaScript",
                "cor": 0xFF4500,
                "author": "COMANDOS NA LINGUAGEM JAVASCRIPT:",
                "logo": "https://imgur.com/T0RjAz1.png"
            }
        }


    @commands.command(
        name='comandos',
        aliases=['cmds'],
        description='Mostra a lista de todos os comandos registrados no sistema pra linguagem especificada',
        usage='c.comandos [py|js]'
    )
    async def _comandos(self, ctx, linguagem):
        if not str(ctx.channel.id) in self.lab.canais and not str(ctx.message.author.id) in self.lab.staff:
           await ctx.message.add_reaction(":incorreto:594222819064283161")
           return
        linguagens = self.linguagens
        linguagem = linguagem.lower()
        

        if linguagem not in linguagens['js']['aliases'] and linguagem not in linguagens['py']['aliases']:
            return await ctx.send(f"{self.lab._emojis['incorreto']} | **{ctx.author.name}**, você não especificou uma linguagem válida!\n**Linguagens disponíveis**: `py` e `js`")

        linguagem = linguagens['py'] if linguagem in linguagens['py']['aliases'] else linguagens['js']

        em = discord.Embed(
            colour=self.lab.cor,
            description=" , ".join([f"**`{c['nome']}`**" for c in self.lab.db.cmds.find({"linguagem": linguagem['nome'].lower(), "pendente": False}).sort("vPositivos", DESCENDING)]))
        em.set_author(name=linguagem['author'],icon_url=linguagem['logo'])
        em.set_footer(
            text=self.lab.user.name+" © 2019",
            icon_url=self.lab.user.avatar_url_as()
        )

        await ctx.send(embed=em)

    @commands.command(
        name='comandopy',
        aliases=['cmdpy'],
        description='Visualiza o código de um comando em Python publicado por um membro',
        usage='c.comandopy <Nome do Comando>'
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def _comandopy(self, ctx, *, nome):
        if not str(ctx.channel.id) in self.lab.canais and not str(ctx.message.author.id) in self.lab.staff:
           await ctx.message.add_reaction(":incorreto:594222819064283161")
           return
        cmd = self.lab.db.cmds.find_one({"linguagem": "python", "nome": nome.lower(), "pendente": False})
        if cmd is None:
            return await ctx.send(f"{self.lab._emojis['incorreto']} | **{ctx.author.name}**, não foi possível encontrar um comando em `Python` com o nome ``{nome}``.")
        

        try:
            autor = await self.lab.fetch_user(int(cmd['autor']))
        except:
            autor = "Não encontrado"

        data = cmd['data'].strftime("%d/%m/20%y - %H:%M:%S")

        em = discord.Embed(
            colour=self.lab.cor,
            description=f"\n**NOME DO COMANDO:** ``{nome.lower()}``\n**AUTOR:** `{autor}`\n**DATA DE ENVIO:** `{data}`\n```py\n{cmd['code']}```")
        #em.set_footer(
            #text=f"👍 {cmd['vPositivos']} votos e {cmd['vNegativos']} votos Negativos",)
        #em.set_thumbnail(url="https://imgur.com/LD60DLf.png")
        em.set_footer(
            text=self.lab.user.name+" © 2019",
            icon_url=self.lab.user.avatar_url_as()
        )

        await ctx.send(embed=em)

    @commands.command(
        name='comandojs',
        aliases=['cmdjs'],
        description='Visualiza o código de um comando em JavaScript publicado por um membro',
        usage='c.comandojs <Nome do Comando>'
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def _comandojs(self, ctx, *, nome = None):
        if not str(ctx.channel.id) in self.lab.canais and not str(ctx.message.author.id) in self.lab.staff:
           await ctx.message.add_reaction(":incorreto:594222819064283161")
           return
        cmd = self.lab.db.cmds.find_one({"linguagem": "javascript", "nome": nome.lower(), "pendente": False})
        if cmd is None:
            return await ctx.send(f"{self.lab._emojis['incorreto']} | **{ctx.author.name}**, não foi possível encontrar um comando em `Python` com o nome ``{nome}``.")
        

        try:
            autor = await self.lab.fetch_user(int(cmd['autor']))
        except:
            autor = "Não encontrado"

        data = cmd['data'].strftime("%d/%m/20%y - %H:%M:%S")

        em = discord.Embed(
            colour=self.lab.cor,
            description=f"\n**NOME DO COMANDO:** ``{nome.lower()}``\n**AUTOR:** `{autor}`\n**DATA DE ENVIO:** `{data}`\n```py\n{cmd['code']}```")
        #em.set_footer(
            #text=f"👍 {cmd['vPositivos']} votos e {cmd['vNegativos']} votos Negativos",)
        #em.set_thumbnail(url="https://imgur.com/LD60DLf.png")
        em.set_footer(
            text=self.lab.user.name+" © 2019",
            icon_url=self.lab.user.avatar_url_as()
        )

        await ctx.send(embed=em)

    @commands.command(
        name='enviarcomando',
        aliases=['enviarcmd', 'adicionarcomando', 'addcomando','addcmd'],
        description='Envia um código de comando para aprovação',
        usage='c.enviarcomando'
    )
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def _enviarcomando(self, ctx):
        if not str(ctx.channel.id) in self.lab.canais and not str(ctx.message.author.id) in self.lab.staff:
           await ctx.message.add_reaction(":incorreto:594222819064283161")
           return
        reactions = [":incorreto:594222819064283161", ':correto:594222662717538330']
        if ctx.author.id in self.users:
            return await ctx.send(f"{self.lab._emojis['incorreto']} | **{ctx.author.name}**, já tem um formulário em aberto no seu DM.", delete_after=30)

        try:
            nome = discord.Embed(description=f"<:newDevs:573629564627058709> **|** Então você quer adicionar um **Comando** no NewDevs?\nPara isso precisamos que você preencha um pequeno formulário para cadastramento de seu **comando** em nosso sistema.\n\n{self.lab._emojis['nome']} **|** Diga-nos o nome do **comando**: \n{self.lab._emojis['timer']} **|** **2 minutos**", color=0x7289DA)
            msg_nome = await ctx.author.send(embed=nome, delete_after=120)
        except:
            await ctx.send(f"{self.lab._emojis['incorreto']} | **{ctx.author.name}**, você precisa ativar as **`Mensagens Diretas`** para que eu possa prosseguir com o formulário de adicionar comandos.")
        
        self.users.append(ctx.author.id)
        embed = discord.Embed(description=f":envelope_with_arrow: **|** Olá **{ctx.author.name}**, verifique sua mensagens diretas (DM).", color=0x7289DA)
        await ctx.send(embed=embed)

        def check(m):
            return m.channel.id == msg_nome.channel.id and m.author == ctx.author

        nome = None
        limite = 12
        tentativas = 0
        while nome is None:
            try:
                resposta = await self.lab.wait_for("message", check=check, timeout=120)
            except Esgotado:
                
                await ctx.author.send(f"{self.lab._emojis['seta']} | **{ctx.author.name}**, você demorou muito para fornecer um nome!", delete_after=30)
                break

            if tentativas == 3:
                await ctx.author.send(f"{self.lab._emojis['incorreto']} **{ctx.author.name}**, você atingiu o limite de 3 tentativas e por isso a ação foi cancelada.", delete_after=20)
                break
            elif len(resposta.content) > limite:
                tentativas += 1
                await ctx.author.send(f"{self.lab._emojis['seta']} O **`nome`** fornecido é muito grande! **Máximo de {limite} caracteres\nTentativa: `{tentativas}/3`**", delete_after=15)
            else:
                nome = resposta.content
        
        if not nome:
            return self.users.remove(ctx.author.id)

        nome = nome.lower()
    
        embed=discord.Embed(description=f"{self.lab._emojis['api']} **|** Agora diga-me a linguagem que o **comando** foi feito\n{self.lab._emojis['api']} Linguagens : [**PYTHON | JAVASCRIPT**]\n{self.lab._emojis['timer']} **|** **2 minutos**", color=0x7289DA)
        msg_lang = await ctx.author.send(embed=embed)
        
        def check_author1(m):
            return m.author == ctx.author and m.guild is None

        linguagem = None
        linguagens = self.linguagens
        tentativas = 0
        while linguagem is None:
            try:
                resposta = await self.lab.wait_for("message", check=check_author1, timeout=120)
            except Esgotado:
                await ctx.author.send(f" | **{ctx.author.name}**, você demorou muito para especificar a linguagem!", delete_after=30)
                break

            if tentativas == 3:
                await ctx.author.send(f" **{ctx.author.name}**, você errou e atingiu o máximo de tentativas permitidas. `(3)`", delete_after=20)
                break
            elif resposta.content.lower() not in linguagens['py']['aliases'] and resposta.content.lower() not in linguagens['js']['aliases']:
                tentativas += 1
                await ctx.author.send(f"{self.lab._emojis['seta']} A **`linguagem`** especificada é inválida! **Linguagens permitidas: `Python`**, **`JavaScript`\nTentativa: `{tentativas}/3`**", delete_after=15)
            else:
                linguagem = resposta.content
        
        if not linguagem:
            return self.users.remove(ctx.author.id)

        linguagem = linguagens['py'] if linguagem.lower() in linguagens['py']['aliases'] else linguagens['js']
        #       < < < ------------------------------------- > > >

        comando = self.lab.db.cmds.find_one({"linguagem": linguagem['nome'].lower(), "nome": nome})
        if comando:
            self.users.remove(ctx.author.id)
            return await ctx.author.send(f"{self.lab._emojis['incorreto']} | **{ctx.author.name}**, já temos um comando chamado **`{nome}`** para a linguagem **`{linguagem['nome']}`**.")

        #       < < < ------------------------------------- > > >
        texto = f"{self.lab._emojis['api']} **|** Agora cole-o **comando** ou escreva ele. (limite 2000 caracteres)\n{self.lab._emojis['timer']} **|** **2 minutos**"
        embed=discord.Embed(description=texto, color=0x7289DA)
        msg_code = await ctx.author.send(embed=embed)
        
        def check_author(m):
            return m.author == ctx.author and m.guild is None

        code = None
        limite = 2000
        tentativas = 0
        while code is None:
            try:
                resposta = await self.lab.wait_for("message", check=check_author, timeout=300)
            except Esgotado:
                await ctx.author.send(f"{self.lab._emojis['incorreto']} | **{ctx.author.name}**, você demorou muito para especificar a linguagem!", delete_after=30)
                break

            if tentativas == 3:
                await ctx.author.send(f"{self.lab._emojis['incorreto']} **{ctx.author.name}**, você atingiu o limite de 3 tentativas e por isso a ação foi cancelada.", delete_after=20)
                break
            elif len(resposta.content) > limite:
                tentativas += 1
                embed=discord.Embed(description=f"<:incorreto:594222819064283161> **|** Olá **{ctx.author.name}**, o **código** do comando que você inseriu passou do limite de 2000 caracteres.\n\n{self.lab._emojis['seta']} | **Tentativa: `{tentativas}/3`**", color=0x7289DA)
                await ctx.author.send(f"{self.lab._emojis['seta']} Seu código ultrapassa o limite de **`{limite}`** caracteres permitidos.\n**Tentativa: `{tentativas}/3`**", delete_after=15)
            else:
                code = resposta.content
        
        if not code:
            return self.users.remove(ctx.author.id)
        #       < < < ------------------------------------- > > >

        embed=discord.Embed(description=f"```{linguagem['nome'].lower()}\n{code}\n```", color=0x7289DA,timestamp=datetime.utcnow())
        embed.set_author(name="SOLICITAÇÃO ADICIONAR COMANDO", icon_url=ctx.author.avatar_url_as())
        embed.add_field(name=f"{self.lab._emojis['nome']} Nome", value = "``"+str(nome)+"``", inline=True)
        embed.add_field(name=f"{self.lab._emojis['api']} Linguagem ", value = "``"+str(linguagem['nome'])+"``", inline=True)
        embed.add_field(name=f"{self.lab._emojis['mention']} Enviado por", value = "``"+str(ctx.author)+"`` ("+str(ctx.author.mention)+")", inline=True)
        embed.set_footer(text=self.lab.user.name+" © 2019", icon_url=self.lab.user.avatar_url_as())
        
    
        
        logs = self.lab.get_channel(582984537546424331)
        aprovar_comandos = self.lab.get_channel(571087828482523146)
        #pendente_msg = await aprovar_comandos.send(embed=em, content="**NOVO COMANDO AGUARDANDO POR APROVAÇÃO!**")
        pendente_msg = await aprovar_comandos.send(embed=embed, content="@here")

        await logs.send(f"{self.lab._emojis['discord']} {ctx.author.mention} enviou o comando **`{nome}`** para verificação.")
        for e in reactions:
            await pendente_msg.add_reaction(e)

        self.lab.db.cmds.insert_one({
            "_id": ctx.author.id,
            "linguagem": linguagem['nome'].lower(),
            "nome": nome,
            "code": code,
            "autor": ctx.author.id,
            "categoria": None,
            "vMembros": [],
            "vPositivos": 0,
            "vNegativos": 0,
            "aprovado_por": None,
            "data": datetime.now(),
            "pendente": True,
            "pendente_msg": pendente_msg.id
        })

        await ctx.author.send(f"{self.lab._emojis['correto']} | Seu comando **`{nome}`** na linguagem **`{linguagem['nome']}`** foi enviado para a verificação.")
        self.users.remove(ctx.author.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != 571087828482523146 or payload.user_id == self.lab.user.id:
            return

        comando = self.lab.db.cmds.find_one({"pendente": True, "pendente_msg": payload.message_id})
        if not comando:
            return

        logs = self.lab.get_channel(582984537546424331)
        canal = self.lab.get_channel(payload.channel_id)
        mensagem = await canal.fetch_message(payload.message_id)
        staffer = mensagem.guild.get_member(payload.user_id)
        autor = mensagem.guild.get_member(comando['autor'])
        if str(payload.emoji) == self.lab._emojis['correto']:
            self.lab.db.cmds.update_one(comando, {"$set": {"pendente": False, "aprovado_por": payload.user_id}})
            await logs.send(f"{self.lab._emojis['discord']} O comando **`{comando['nome']}`** enviado por <@{comando['autor']}> foi aprovado por **{staffer.name}**.")
            await mensagem.delete()

            if autor:
                try:
                    await autor.send(f"{self.lab._emojis['correto']} | **{autor.name}**, seu comando **`{comando['nome']}`** foi aceito por **{staffer.name}**.")
                except:
                    pass
        elif str(payload.emoji) == self.lab._emojis['incorreto']:
            enviador = await self.lab.fetch_user(comando['autor'])
            try:
                embed = discord.Embed(description=f"{self.lab._emojis['api']} | **INFORME O MOTIVO DE ESTAR RECUSANDO O COMANDO `{comando['nome'].title()}`**.\n\n{self.lab._emojis['timer']} | **`5 minutos`**", color=0x7289DA)
                embed.set_footer(text=f"Autor: {enviador}.",icon_url=enviador.avatar_url_as(format="png"))
                pergunta = await staffer.send(embed=embed)
            except:
                await mensagem.remove_reaction(payload.emoji, staffer)
                return await canal.send(f"{self.lab._emojis['discord']} {staffer.mention}, **você precisa ativar as DMs para prosseguir**.")

            def check(m):
                return m.channel.id == pergunta.channel.id and m.author == staffer
        
            try:
                resposta = await self.lab.wait_for("message", check=check, timeout=300)
            except Esgotado:

                embed=discord.Embed(colour=0x7289DA, description=f"{self.lab._emojis['incorreto']} | **{staffer.name}**, você demorou demais para fornecer um motivo.")
                await mensagem.remove_reaction(payload.emoji, staffer)
                return await staffer.send(embed=embed)
            
            embed=discord.Embed(colour=0x7289DA, description=f"{self.lab._emojis['correto']} **{staffer.name}**, você recusou o comando `{comando['nome']}`.\n\n{self.lab._emojis['tipo']} | **MOTIVO:** ```{resposta.content}```")
            embed.set_footer(text=self.lab.user.name+" © 2019", icon_url=self.lab.user.avatar_url_as())
            await staffer.send(embed=embed)
            await logs.send(f"{self.lab._emojis['discord']} **{staffer.name}** rejeitou o comando **`{comando['nome']}`** enviado por <@{comando['autor']}>.")

            if autor:
                try:
                    embed=discord.Embed(colour=0x7289DA, description=f"{self.lab._emojis['incorreto']} **{autor.name}**, seu comando **`{comando['nome']}`** foi recusado.\n{self.lab._emojis['mention']} | **STAFFER:** ``{staffer}``\n\n{self.lab._emojis['tipo']} | **MOTIVO:** ```{resposta.content}```")
                    embed.set_footer(text=self.lab.user.name+" © 2019", icon_url=self.lab.user.avatar_url_as())
                    #await autor.send(f"{self.lab._emojis['incorreto']} | **{autor.name}**, seu comando **`{comando['nome']}`** foi recusado por **{staffer.name}**.```Motivo: {resposta.content}```")
                    await autor.send(embed=embed)
                except:
                    pass
            
            self.lab.db.cmds.delete_one(comando)
            await mensagem.delete()

def setup(lab):
    lab.add_cog(comandos(lab))
