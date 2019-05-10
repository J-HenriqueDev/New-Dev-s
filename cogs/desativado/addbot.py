
import discord
from discord.ext import commands
import random
import time
import asyncio
from pymongo import MongoClient
import pymongo
import json
import config.database
import config.db
from datetime import datetime, timedelta


python = ['python', 'py']
javascript = ['javascript','js']
kotlin = ['kotlin','kt']
java = ['java']
ruby = ['ruby','rb']
go = ['golang', 'go']

prefixos = ["c.","!","@","/"]
linguagem = ["python","javascript","java","kotlin","golang","ruby"]
blocklist = []

class addbot(commands.Cog):
    def __init__(self, bard):
        self.bard = bard




    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def addbot(self,ctx):   
         if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
            await ctx.message.add_reaction(":incorreto:571040855918379008")
            return
         dias_servidor = (datetime.utcnow() - ctx.author.joined_at).days
         if dias_servidor < 5:
            embed = discord.Embed(colour=0x7289DA)
            embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, você precisa ser membro desse servidor há mais de **`5`** dias para poder adicionar um bot.", color=0x7289DA)
            return await ctx.send(embed=embed)
         try:
           embed=discord.Embed(description=f":envelope_with_arrow:  **|** Olá **{ctx.author.name}**, verifique sua mensagens diretas (DM).", color=0x7289DA)
           msg = await ctx.send(embed=embed)
           txs = f"<:newDevs:573629564627058709> **|** Então você quer adicionar o seu **BOT** em nosso servidor?\nPara isso precisamos que você preencha um pequeno formulário para cadastramento de seu **BOT** em nosso sistema e discord.\n\n<:bots:565972012325928980> **|** Insira o **ID** do bot que deseja adicionar: \n<:timer:565975875988750336> **|** **2 minutos**"
           embed=discord.Embed(description=txs, color=0x7289DA)
           msg = await ctx.author.send(embed=embed)
           def pred(m):
               return m.author == ctx.author and m.guild is None

           id_bot = await self.bard.wait_for('message', check=pred, timeout=120.0) 
           if id_bot.content.isnumeric() == False:
              await msg.delete()
              embed=discord.Embed(description=f"<:incorreto:571040727643979782>  **|** Olá **{ctx.author.name}**, o argumento que você inseriu não é um **ID** e por isso o cadastramento foi cancelado.", color=0x7289DA)
              msg = await ctx.author.send(embed=embed)
              await asyncio.sleep(30)
              await msg.delete()
           else:           
             try:
               usuario = await self.bard.fetch_user(id_bot.content)
               if usuario.bot == True:
                if usuario in ctx.guild.members: 
                   gg = 1
                   texto = f"<:incorreto:571040727643979782>  **|** o **ID** que você forneceu corresponde a de um **BOT** chamado `{usuario}`, é o bot já está no servidor e por isso a cadastramento foi cancelado."
                else:
                  gg = 2
                  texto = f"<:newDevs:573629564627058709> **|** o **ID** que você forneceu corresponde a de um **BOT** chamado `{usuario}`.\n\n<:incorreto:571040727643979782>  : Não é meu **BOT**\n<:correto:571040855918379008> : É meu **BOT**\n\n{self.bot._emojis['timer']} **|** **2 minutos**"
               else:
                 gg = 1
                 texto = f"<:incorreto:571040727643979782>  **|** o **ID** que você forneceu corresponde a de um usuário chamado `{usuario}` não é possível adiciona-lo ao servidor por que ele não e um usuário **BOT** e por isso a cadastramento foi cancelado."
             except:
                usuario = None
             if usuario == None:
                embed=discord.Embed(description=f"<:incorreto:571040727643979782>  **|** Olá **{ctx.author.name}**, o **ID** que você inseriu é invalído e por isso o cadastramento foi cancelado", color=0x7289DA)
                msg = await ctx.author.send(embed=embed)
                await asyncio.sleep(30)
                await msg.delete()
             else:
               embed=discord.Embed(description=texto, color=0x7289DA)
               msg = await ctx.author.send(embed=embed)
               if gg == 1:
                  await asyncio.sleep(30)             
                  await msg.delete()
               else:
                  reactions = [":incorreto:571040727643979782", ':correto:571040855918379008']
                  user = ctx.message.author
                  if user == ctx.message.author:
                    for reaction in reactions:
                        await msg.add_reaction(reaction)

                  def check(reaction, user):
                      return user == ctx.message.author and str(reaction.emoji)

                  reaction, user = await self.bard.wait_for('reaction_add', check=check, timeout=120.0)

                  if reaction.emoji.name == 'incorreto':
                     await msg.delete()
                     embed=discord.Embed(description=f"<:incorreto:571040727643979782>  **|** o **ID** que você forneceu corresponde a de um **BOT** chamado `{usuario}`, já que **BOT** não é seu o cadastramento foi cancelado.", color=0x7289DA)
                     msg = await ctx.author.send(embed=embed)
                     await asyncio.sleep(30)
                     await msg.delete()
                  if reaction.emoji.name == 'correto':
                   await msg.delete()
                   txs = f"<:texto:565968741788155907> **|** Diga-nos agora o prefixo do seu **BOT** (máximo 8 caracteres)\n<:block:576119613385998338>Prefixo banidos **|** **[c.],[!],[/][@],[#]**\n<:timer:565975875988750336> **|** **2 minutos**"
                   embed=discord.Embed(description=txs, color=0x7289DA)
                   msg = await ctx.author.send(embed=embed)

                   prefix = await self.bard.wait_for('message', check=pred, timeout=120.0) 
                   if len(prefix.content) +1 >= 8:                      
                      await msg.delete()
                      embed = discord.Embed(description=f"<:incorreto:571040727643979782>  **|** Olá **{ctx.author.name}**, o prefixo que você forneceu execedeu o limite máximo **(8)** caracteres e por isso ação foi cancelada.", color=0x7289DA)
                      msg = await ctx.author.send(embed=embed)
                      await asyncio.sleep(30)
                      await msg.delete()
                   elif str(prefix.content) in prefixos:                      
                      await msg.delete()
                      embed = discord.Embed(description=f"<:incorreto:571040727643979782>  **|** Olá **{ctx.author.name}**, o prefixo que você forneceu está banido e por isso ação foi cancelada.", color=0x7289DA)
                      msg = await ctx.author.send(embed=embed)
                      await asyncio.sleep(30)
                      await msg.delete()
                   else:
                     await msg.delete()
                     lang = ", ".join(linguagem)
                     txs = f"<:newDevs:573629564627058709> **|** Diga-nos agora o linguagem do seu **BOT** foi criado.\n<:api:565975875804463114>Linguagens **|** **{lang}**\n<:timer:565975875988750336> **|** **2 minutos**"
                     embed=discord.Embed(description=txs, color=0x7289DA)
                     msg = await ctx.author.send(embed=embed)
                     lang = await self.bard.wait_for('message', check=pred, timeout=120.0) 
                     if not str(lang.content) in linguagem:                      
                        await msg.delete()
                        embed = discord.Embed(description=f"<:incorreto:571040727643979782>  **|** Olá **{ctx.author.name}**, a linguagem que você forneceu é invalida e por isso ação foi cancelada.", color=0x7289DA)
                        msg = await ctx.author.send(embed=embed)
                        await asyncio.sleep(30)
                        await msg.delete()
                     elif str(lang.content) in linguagem:                      
                        await msg.delete()
                        embed = discord.Embed(description=f"<:newDevs:573629564627058709> **|** Olá **{ctx.author.name}**, abaixo está localizado as informações do **BOT** caso tenha alguma coisa errada clique na reação (<:incorreto:571040727643979782> ) para recusar e deletar, caso esteja certo clique na reação (<:correto:571040855918379008>).",color=0x7289DA)
                        embed.set_author(name="SOLICITAÇÂO DE ADD(BOT)", icon_url=ctx.author.avatar_url_as())
                        embed.add_field(name="<:bots:565972012325928980> Bot", value = "``"+str(usuario)+"``", inline=True)
                        embed.add_field(name="<:ip:565968375772217354> Id", value = "``"+str(usuario.id)+"``", inline=True)
                        embed.add_field(name="<:texto:565968741788155907> Prefixo", value = "``"+str(prefix.content)+"``", inline=True)
                        embed.add_field(name="<:api:565975875804463114> Linguagem", value = "``"+str(lang.content)+"``", inline=True)
                        embed.set_thumbnail(url=usuario.avatar_url_as())
                        embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
                        msg = await ctx.author.send(embed=embed)
                        reactions = [":incorreto:571040727643979782", ':correto:571040855918379008']
                        user = ctx.message.author
                        if user == ctx.message.author:
                          for reaction in reactions:
                              await msg.add_reaction(reaction)

                        def _check(reaction, user):
                            return user == ctx.message.author and str(reaction.emoji)

                        reaction, user = await self.bard.wait_for('reaction_add', check=_check, timeout=120.0)
                        if reaction.emoji.name == 'incorreto':
                           await msg.delete()
                           embed=discord.Embed(description=f"<:incorreto:571040727643979782>  **|** A solicitação foi cancelada.. tente novamente caso queira adicionar o bot novamente ao servidor.", color=0x7289DA)
                           msg = await ctx.author.send(embed=embed)
                           await asyncio.sleep(30)
                           await msg.delete()
                        if reaction.emoji.name == 'correto':
                           await msg.delete()
                           embed=discord.Embed(description=f"<:correto:571040855918379008> **|** A solicitação foi realizada com sucesso, agora aguarde algum staff convidar seu bot para o servidor.", color=0x7289DA)
                           msg = await ctx.author.send(embed=embed)
                           await asyncio.sleep(10)
                           await msg.delete()
                           embed = discord.Embed(color=0x7289DA)
                           embed.set_author(name="SOLICITAÇÂO DE ADD(BOT)", icon_url=ctx.author.avatar_url_as())
                           embed.add_field(name="<:bots:565972012325928980> Bot", value = "``"+str(usuario)+"``", inline=True)
                           embed.add_field(name="<:ip:565968375772217354> Id", value = "``"+str(usuario.id)+"``", inline=True)
                           embed.add_field(name="<:texto:565968741788155907> Prefixo", value = "``"+str(prefix.content)+"``", inline=True)
                           embed.add_field(name="<:api:565975875804463114> Linguagem", value = "``"+str(lang.content)+"``", inline=True)
                           embed.add_field(name="<:mention:573230888029126657> Dono", value = "``"+str(ctx.author)+"``"+" ("+str(ctx.author.mention)+")", inline=True)
                           embed.add_field(name="<:convite:519288102775291904> Convite", value = f"[Link](https://discordapp.com/api/oauth2/authorize?client_id={usuario.id}&permissions=0&scope=bot)", inline=True)
                           embed.set_thumbnail(url=usuario.avatar_url_as())
                           embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
                           #servidor
                           server = self.bard.get_guild(570906068277002271)
                           #canal solicitação
                           channel = discord.utils.get(server.channels, id=571087828482523146)
                           msg = await channel.send(embed=embed, content="<@&571015748517101578>")
                           reactions = [":incorreto:571040727643979782", ':correto:571040855918379008']
                           user = ctx.message.author
                           if user == ctx.message.author:
                            for reaction in reactions:
                                await msg.add_reaction(reaction)
                           
                            def check(reaction, user):
                              return user.id != 572097258380853249 and reaction.message.id == msg.id


                            reaction, author = await self.bard.wait_for('reaction_add', check=check)
                            if reaction.emoji.name == 'correto':
                                   mongo = MongoClient(config.database.database)
                                   bard = mongo['bard']
                                   bot = bard['bot']
                                   bot = bard.bot.find_one({"_id": str(usuario.id)})
                                   if bot is None:
                                      print("[Bot] : inserido")
                                      serv ={"_id": str(usuario.id), "prefixo": str(prefix.content),"dono": str(ctx.author.id), "tags":"Não definidas", "linguagem":str(lang.content.lower()), "aceito por":str(author.id), "reputação":"0"}
                                      bard.bot.insert_one(serv).inserted_id
                                   else:
                                     print("[Bot] : Atualizado")
                                     bard.bot.update_many({'_id': str(usuario.id)}, {'$set': {"prefixo": str(prefix.content),"dono": str(ctx.author.id), "tags":"Não definidas", "linguagem":str(lang.content.lower()), "aceito por":str(author.id), "reputação":"0"}})

                                   await msg.delete()
                                   embed = discord.Embed(color=0x7289DA)
                                   embed.set_author(name="BOT ACEITO", icon_url=ctx.author.avatar_url_as())
                                   embed.add_field(name="<:bots:565972012325928980> Bot", value = "``"+str(usuario)+"``", inline=True)
                                   embed.add_field(name="<:ip:565968375772217354> Id", value = "``"+str(usuario.id)+"``", inline=True)
                                   embed.add_field(name="<:texto:565968741788155907> Prefixo", value = "``"+str(prefix.content)+"``", inline=True)
                                   embed.add_field(name="<:api:565975875804463114> Linguagem", value = "``"+str(lang.content)+"``", inline=True)
                                   embed.add_field(name="<:mention:573230888029126657> Dono", value = "``"+str(ctx.author)+"``"+" ("+str(ctx.author.mention)+")", inline=True)
                                   embed.add_field(name="<:mention:573230888029126657> Aceito por", value = f"<@{author.id}>", inline=True)
                                   embed.set_thumbnail(url=usuario.avatar_url_as())
                                   embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
                                   server = self.bard.get_guild(570906068277002271)
                                   channel = discord.utils.get(server.channels, id=571046221121060894)
                                   await channel.send(embed=embed)
                                   link = f"<:correto:571040855918379008> **|** Convite do **BOT** ``{str(usuario)} ({str(usuario.id)})`` - https://discordapp.com/api/oauth2/authorize?client_id={usuario.id}&permissions=0&scope=bot"
                                   embed=discord.Embed(description=link, color=0x7289DA)
                                   usuario = await self.bard.fetch_user(author.id)
                                   await usuario.send(embed=embed)
                                
                            if reaction.emoji.name == 'incorreto':
                                  try:
                                   await msg.delete()
                                   server = self.bard.get_guild(570906068277002271)
                                   channel = discord.utils.get(server.channels, id=571046221121060894)
                                   embed = discord.Embed(description=f"<:incorreto:571040727643979782>  **|** Diga-me o motivo da recusa do **BOT** ``{str(usuario)}``", color=0x7289DA)
                                   msg = await channel.send(embed=embed)
                                   recused = await self.bard.wait_for('message') 
                                   if recused.content.lower().startswith("motivo :"):
                                       await msg.delete()
                                       embed = discord.Embed(color=0x7289DA)
                                       embed.set_author(name="BOT RECUSADO", icon_url=ctx.author.avatar_url_as())
                                       embed.add_field(name="<:bots:565972012325928980> Bot", value = "``"+str(usuario)+"``", inline=True)
                                       embed.add_field(name="<:ip:565968375772217354> Id", value = "``"+str(usuario.id)+"``", inline=True)
                                       embed.add_field(name="<:texto:565968741788155907> Prefixo", value = "``"+str(prefix.content)+"``", inline=True)
                                       embed.add_field(name="<:api:565975875804463114> Linguagem", value = "``"+str(lang.content)+"``", inline=True)
                                       embed.add_field(name="<:mention:573230888029126657> Dono", value = "``"+str(ctx.author)+"``"+" ("+str(ctx.author.mention)+")", inline=True)
                                       embed.add_field(name="<:mention:573230888029126657> Recusado por", value = f"<@{author.id}>", inline=True)
                                       texto = str(recused.content).replace("motivo :", "")
                                       embed.add_field(name="<:incorreto:571040727643979782>  Motivo", value = f"``{texto}``", inline=True)
                                       embed.set_thumbnail(url=usuario.avatar_url_as())
                                       embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
                                       server = self.bard.get_guild(570906068277002271)
                                       channel = discord.utils.get(server.channels, id=571046221121060894)
                                       await channel.send(embed=embed)
                                  except Exception as e:
                                      print(e)

         except asyncio.TimeoutError:             
            await msg.delete()
            embed = discord.Embed(colour=0x7289DA)
            embed=discord.Embed(description=f"<:timer:565975875988750336> **|** Olá **{ctx.author.name}**, passou do tempo limite e por isso a cadastramento foi cancelado.", color=0x7289DA)
            msg = await ctx.author.send(embed=embed)
            await asyncio.sleep(30)
            await msg.delete()


         except discord.errors.Forbidden:

            await msg.delete()
            embed = discord.Embed(colour=0x7289DA)
            embed=discord.Embed(description=f"<:messagem:518615610721173505> **|** Olá **{ctx.author.name}**, para iniciar o processo precisamos que você libere suas mensagens privadas.", color=0x7289DA)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(30)
            await msg.delete()

def setup(bard):
    print("[Bot] : Cmd (addbot) ")
    bard.add_cog(addbot(bard))
