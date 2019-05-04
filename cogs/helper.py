
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
prefixos = ["rd.","!","@","/"]
linguagem = ["python","javascript","java","kotlin","golang","ruby","nenhuma"]
blocklist = []




class helper(commands.Cog):
    def __init__(self, bard):
        self.bard = bard
    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def gg(self,ctx):   
       if ('manage_roles', True) in list(ctx.author.guild_permissions):
          print("Ok")
       else:
         print("Not")


    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def helper(self,ctx):   
        if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:571040727643979782")
           return
        try:
         try:
           embed=discord.Embed(description=f":envelope_with_arrow: **|** Olá **{ctx.author.name}**, verifique sua mensagens diretas (DM).", color=0x00d200)
           msg = await ctx.send(embed=embed)
           txs = f"<:newDevs:573629564627058709> **|** Então você quer ser um **</Helper>** em nosso servidor?\nPara isso precisamos que você preencha um pequeno formulário para cadastramento de seu dados em nosso sistema.\n\n<:nome:565969826611462174> **|** Diga-nos seu **Nome completo**: \n<:timer:565975875988750336> **|** **2 minutos**"
           embed=discord.Embed(description=txs, color=0x00d200)
           msg = await ctx.author.send(embed=embed)
 
           def pred(m):
               return m.author == ctx.author and m.guild is None

           nome = await self.bard.wait_for('message', check=pred, timeout=120.0) 
           if len(nome.content) >=40:              
              await msg.delete()
              embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, o **Nome** que você inseriu passou do limite de 40 caracteres.", color=0x00d200)
              msg = await ctx.author.send(embed=embed)
              await asyncio.sleep(30)
              await msg.delete()
           else:
             await msg.delete()
             texto = f"<:newDevs:573629564627058709> **|** Agora diga-me sua idade (10 anos a 99 anos)\n<:timer:565975875988750336> **|** **2 minutos**"
             embed=discord.Embed(description=texto, color=0x00d200)
             msg = await ctx.author.send(embed=embed)
             idade = await self.bard.wait_for('message', check=pred, timeout=120.0) 
             if idade.content.isnumeric() == False:
                await msg.delete()
                embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, a idade que você inseriu não é válida.", color=0x00d200)
                msg = await ctx.author.send(embed=embed)
                await asyncio.sleep(30)
                await msg.delete()
             else:
               if len(idade.content) >=3:              
                  await msg.delete()
                  embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, a idade que você inseriu não é válida. (10 anos a 99 anos.)", color=0x00d200)
                  msg = await ctx.author.send(embed=embed)
                  await asyncio.sleep(30)
                  await msg.delete()
               else:
                 await msg.delete()
                 lang = ", ".join(linguagem)
                 langg = str(lang).replace("nenhuma","")
                 texto = f"<:newDevs:573629564627058709> **|** Diga-nos a linguagem que você programa. (**Primária**)\nLinguagens : {langg}\n<:timer:565975875988750336> **|** **2 minutos**"
                 embed=discord.Embed(description=texto, color=0x00d200)
                 msg = await ctx.author.send(embed=embed)
                 lang1 = await self.bard.wait_for('message', check=pred, timeout=120.0) 
                 if not str(lang1.content.lower()) in linguagem:                      
                    await msg.delete()
                    embed = discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, a linguagem que você forneceu é invalida e por isso ação foi cancelada.", color=0x00d200)
                    msg = await ctx.author.send(embed=embed)
                    await asyncio.sleep(30)
                    await msg.delete()
                 elif str(lang1.content.lower()) in linguagem:                      
                   lang = ", ".join(linguagem)
                   await msg.delete()
                   texto = f"<:newDevs:573629564627058709> **|** Diga-nos a linguagem que você programa. (**Secundária**)\n(Caso não tenha nenhuma digite **nenhuma**)\nLinguagens : {langg}\n<:timer:565975875988750336> **|** **2 minutos**"
                   embed=discord.Embed(description=texto, color=0x00d200)
                   msg = await ctx.author.send(embed=embed)
                   lang2 = await self.bard.wait_for('message', check=pred, timeout=120.0) 
                   if not str(lang2.content.lower()) in linguagem:                      
                      await msg.delete()
                      embed = discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, a linguagem que você forneceu é invalida e por isso ação foi cancelada.", color=0x00d200)
                      msg = await ctx.author.send(embed=embed)
                      await asyncio.sleep(30)
                      await msg.delete()
                   elif str(lang2.content.lower()) in linguagem:
                    if str(lang2.content.lower()) == str(lang1.content.lower()): 
                      await msg.delete()
                      embed = discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, a linguagem (**Secundária**) que você forneceu é igual a (**Primária**) e por isso a ação foi cancelada.", color=0x00d200)
                      msg = await ctx.author.send(embed=embed)
                      await asyncio.sleep(30)
                      await msg.delete()
                    else:
                     await msg.delete()
                     texto = f"<:newDevs:573629564627058709> **|** Diga-nos por qual motivo quer se tornar um **</Helper>**? (**Motivo** : 20 caracteres no mínimo)\n<:timer:565975875988750336> **|** **2 minutos**"
                     embed=discord.Embed(description=texto, color=0x00d200)
                     msg = await ctx.author.send(embed=embed)
                     motivo = await self.bard.wait_for('message', check=pred, timeout=120.0)
                     if len(motivo.content) <= 20:
                        await msg.delete()
                        embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, o motivo é muito pequeno. (20 caracteres no mínimo)", color=0x00d200)
                        msg = await ctx.author.send(embed=embed)
                        await asyncio.sleep(30)
                        await msg.delete()
                     else:
                       await msg.delete()
                       embed=discord.Embed(description=f"<:newDevs:573629564627058709> **|** Olá **{ctx.author.name}**, abaixo está localizado as informações do seu cadastro caso tenha alguma coisa errada clique na reação (<:incorreto:571040727643979782>) para recusar e deletar, caso esteja certo clique na reação (<:correto:571040855918379008>).", color=0x00d200)
                       embed.set_author(name="SOLICITAÇÂO DE </HELPER>", icon_url=ctx.author.avatar_url_as())
                       embed.add_field(name="<:nome:565969826611462174> Nome", value = "``"+str(nome.content)+"``", inline=True)
                       embed.add_field(name="<:ip:565968375772217354> Idade", value = "``"+str(idade.content)+"``", inline=True)
                       embed.add_field(name="<:api:565975875804463114> Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                       embed.add_field(name="<:api:565975875804463114> Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                       embed.add_field(name="<:estrela:519465388669403136> Motivo", value = "``"+str(motivo.content)+"``", inline=True)
                       msg = await ctx.author.send(embed=embed)
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
                          embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** A solicitação de cadastramento foi cancelada.", color=0x00d200)
                          msg = await ctx.author.send(embed=embed)
                          await asyncio.sleep(30)
                          await msg.delete()
                       if reaction.emoji.name == 'correto':
                           await msg.delete()
                           embed=discord.Embed(color=0x00d200)
                           embed.set_author(name="SOLICITAÇÂO DE </HELPER>", icon_url=ctx.author.avatar_url_as())
                           embed.add_field(name="<:nome:565969826611462174> Nome", value = "``"+str(nome.content)+"``", inline=True)
                           embed.add_field(name="<:ip:565968375772217354> Idade", value = "``"+str(idade.content)+"``", inline=True)
                           embed.add_field(name="<:api:565975875804463114> Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                           embed.add_field(name="<:api:565975875804463114> Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                           embed.add_field(name="<:estrela:519465388669403136> Motivo", value = "``"+str(motivo.content)+"``", inline=True)
                           #servidor
                           server = self.bard.get_guild(570906068277002271)
                           #canal solicitação
                           channel = discord.utils.get(server.channels, id=571087828482523146)
                           msg = await channel.send(embed=embed, content="<@&571015748517101578>")
                           user = ctx.message.author
                           if user == ctx.message.author:
                            for reaction in reactions:
                                await msg.add_reaction(reaction)
                           
                           def check(reaction, user):
                              return user.id != 572097258380853249 and reaction.message.id == msg.id


                           reaction, author = await self.bard.wait_for('reaction_add', check=check)
                           if reaction.emoji.name == 'correto':
                              await msg.delete()
                              embed = discord.Embed(color=0x00d200)
                              embed.set_author(name="</HELPER> ACEITO", icon_url=ctx.author.avatar_url_as())
                              embed.add_field(name="<:nome:565969826611462174> Helper", value ="``"+str(ctx.author)+"`` (<@"+str(ctx.author.id)+">)", inline=True)
                              embed.add_field(name="<:ip:565968375772217354> ID", value ="``"+str(ctx.author.id)+"``", inline=True)
                              embed.add_field(name="<:api:565975875804463114> Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                              embed.add_field(name="<:api:565975875804463114> Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                              embed.add_field(name="<:mention:573230888029126657> Aceito por", value = f"<@{author.id}>", inline=True)
                              embed.set_thumbnail(url=ctx.author.avatar_url_as())
                              embed.set_footer(text=self.bard.user.name+" © 2019", icon_url=self.bard.user.avatar_url_as())
                              server = self.bard.get_guild(570906068277002271)
                              channel = discord.utils.get(server.channels, id=571046268378546206)
                              await channel.send(embed=embed)
                              mongo = MongoClient(config.database.database)
                              bard = mongo['bard']
                              users = bard['users']
                              users = bard.users.find_one({"_id": str(ctx.author.id)})
                              if users is None:
                                 print("[Helper] : inserido")
                                 serv ={"_id": str(ctx.author.id),"nome": str(nome.content),"id": str(ctx.author.id),"foi_mute":"Não","vezes_mute":"0","foi_devhelper":"Não","vezes_reportado":"0","reputação":int(0),"level":"0","exp":"0","aceito_por":str(author.id),"historico":"Sem punições","bots":["SD"]}
                                 bard.users.insert_one(serv).inserted_id
                                 server = self.bard.get_guild(570906068277002271)
                                 cargo = discord.utils.get(server.roles, name="</New Helper>")
                                 await ctx.author.add_roles(cargo)
                                 if str(lang1.content) == "python":
                                   cargo = discord.utils.get(server.roles, name="</NewHelper Python>")
                                   await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "javascript":
                                    cargo = discord.utils.get(server.roles, name="</NewHelper Javascript>")
                                    await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "kotlin":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Kotlin/Discord.kt")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "java":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Java/Discord.jda")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "ruby":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Ruby/Discord.rb")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "golang":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Golang/Discord.go")
                                     await ctx.author.add_roles(cargo)
                                 if str(lang2.content) == "python":
                                   cargo = discord.utils.get(server.roles, name="</NewHelper Python>")
                                   await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "javascript":
                                    cargo = discord.utils.get(server.roles, name="</NewHelper Javascript>")
                                    await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "kotlin":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Kotlin/Discord.kt")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "java":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Java/Discord.jda")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "ruby":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Ruby/Discord.rb")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "golang":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Golang/Discord.go")
                                     await ctx.author.add_roles(cargo)
                              else:
                                 print("[Helper] : updatado")
                                 bard.users.update_many({"_id": str(ctx.author.id)}, {'$set': {"nome": str(nome.content),"id": str(ctx.author.id),"foi_mute":"Não","vezes_mute":"0","foi_devhelper":"Não","vezes_reportado":"0","reputação":int(0),"level":"0","exp":"0","aceito_por":str(author.id),"historico":"Sem punições","bots":["Nenhum bot"]}})
                                 server = self.bard.get_guild(570906068277002271)
                                 cargo = discord.utils.get(server.roles, name="</New Helper>")
                                 await ctx.author.add_roles(cargo)
                                 if str(lang1.content) == "python":
                                   cargo = discord.utils.get(server.roles, name="</NewHelper Python>")
                                   await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "javascript":
                                    cargo = discord.utils.get(server.roles, name="</NewHelper Javascript>")
                                    await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "kotlin":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Kotlin/Discord.kt")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "java":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Java/Discord.jda")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "ruby":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Ruby/Discord.rb")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "golang":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Golang/Discord.go")
                                     await ctx.author.add_roles(cargo)
                                 if str(lang2.content) == "python":
                                   cargo = discord.utils.get(server.roles, name="</NewHelper Python>")
                                   await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "javascript":
                                    cargo = discord.utils.get(server.roles, name="</NewHelper Javascript>")
                                    await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "kotlin":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Kotlin/Discord.kt")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "java":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Java/Discord.jda")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "ruby":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Ruby/Discord.rb")
                                     await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "golang":
                                     cargo = discord.utils.get(server.roles, name="</NewHelper>Golang/Discord.go")
                                     await ctx.author.add_roles(cargo)

                           elif reaction.emoji.name == 'incorreto':
                                   await msg.delete()
                                   embed = discord.Embed(description=f"<:incorreto:571040727643979782> **|** Diga-me o motivo da recusa do **Helper** ``{str(ctx.author)}``", color=0x7BCDE8)
                                   server = self.bard.get_guild(570906068277002271)
                                   channel = discord.utils.get(server.channels, id=571087828482523146)
                                   await channel.send(embed=embed)                                   
                                   recused = await self.bard.wait_for('message') 
                                   if recused.content.lower().startswith("motivo:"):
                                      await msg.delete()
                                      embed = discord.Embed(color=0x00d200)
                                      embed.set_author(name="</HELPER> RECUSADO", icon_url=ctx.author.avatar_url_as())
                                      embed.add_field(name="<:nome:565969826611462174> Helper", value ="``"+str(ctx.author)+"`` (<@"+str(ctx.author.id)+">)", inline=True)
                                      embed.add_field(name="<:ip:565968375772217354> ID", value ="``"+str(ctx.author.id)+"``", inline=True)
                                      embed.add_field(name="<:api:565975875804463114> Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                                      embed.add_field(name="<:api:565975875804463114> Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                                      embed.add_field(name="<:mention:573230888029126657> Aceito por", value = f"<@{author.id}>", inline=True)
                                      embed.add_field(name="<:tipo:565986477708935168> Motivo", value = f"``{recused.content}``", inline=True)
                                      embed.set_thumbnail(url=ctx.author.avatar_url_as())
                                      embed.set_footer(text=self.bard.user.name+" © 2019", icon_url=self.bard.user.avatar_url_as())
                                      server = self.bard.get_guild(570906068277002271)
                                      #canal solicitação
                                      channel = discord.utils.get(server.channels, id=571087828482523146)
                                      await channel.send(embed=embed)
         except asyncio.TimeoutError:             
             await msg.delete()
             embed = discord.Embed(colour=0x00d200)
             embed=discord.Embed(description=f"<:timer:565975875988750336> **|** Olá **{ctx.author.name}**, passou do tempo limite e por isso a cadastramento foi cancelado.", color=0x7BCDE8)
             msg = await ctx.author.send(embed=embed)
             await asyncio.sleep(30)
             await msg.delete()


        except discord.errors.Forbidden:
             await msg.delete()
             embed = discord.Embed(colour=0x00d200)
             embed=discord.Embed(description=f":envelope_with_arrow:**|** Olá **{ctx.author.name}**, para iniciar o processo precisamos que você libere suas mensagens privadas.", color=0x7BCDE8)
             msg = await ctx.send(embed=embed)
             await asyncio.sleep(30)
             await msg.delete()
                      


def setup(bard):
    print("[Bot] : Cmd (helper) ")
    bard.add_cog(helper(bard))
