
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




class helper():
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
           embed=discord.Embed(description=f"<:messagem:518615610721173505> **|** Olá **{ctx.author.name}**, verifique sua mensagens diretas (DM).", color=0x00d200)
           msg = await ctx.send(embed=embed)
           txs = f"<:new:518620334052737034> **|** Então você quer ser um **</Helper>** em nosso servidor?\nPara isso precisamos que você preencha um pequeno formulário para cadastramento de seu dados em nosso sistema.\n\n<:letra_a:519461766623920152> **|** Diga-nos seu **Nome completo**: \n<:tempo:518615474120949789> **|** **2 minutos**"
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
             texto = f"<:new:518620334052737034> **|** Agora diga-me sua idade (10 anos a 99 anos)\n<:tempo:518615474120949789> **|** **2 minutos**"
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
                 texto = f"<:new:518620334052737034> **|** Diga-nos a linguagem que você programa. (**Primária**)\nLinguagens : {langg}\n<:tempo:518615474120949789> **|** **2 minutos**"
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
                   texto = f"<:new:518620334052737034> **|** Diga-nos a linguagem que você programa. (**Secundária**)\n(Caso não tenha nenhuma digite **nenhuma**)\nLinguagens : {langg}\n<:tempo:518615474120949789> **|** **2 minutos**"
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
                     texto = f"<:new:518620334052737034> **|** Diga-nos por qual motivo quer se tornar um **</Helper>**? (**Motivo** : 20 caracteres no mínimo)\n<:tempo:518615474120949789> **|** **2 minutos**"
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
                       embed=discord.Embed(description=f"<:new:518620334052737034> **|** Olá **{ctx.author.name}**, abaixo está localizado as informações do seu cadastro caso tenha alguma coisa errada clique na reação (<:incorreto:571040727643979782>) para recusar e deletar, caso esteja certo clique na reação (<:correto:518624536082776084>).", color=0x00d200)
                       embed.set_author(name="SOLICITAÇÂO DE </HELPER>", icon_url=ctx.author.avatar_url_as())
                       embed.add_field(name="<:letra_a:519461766623920152> Nome", value = "``"+str(nome.content)+"``", inline=True)
                       embed.add_field(name="<:numeros:518885155407003698> Idade", value = "``"+str(idade.content)+"``", inline=True)
                       embed.add_field(name="<:codigo:518775250863783947> Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                       embed.add_field(name="<:codigo:518775250863783947> Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                       embed.add_field(name="<:estrela:519465388669403136> Motivo", value = "``"+str(motivo.content)+"``", inline=True)
                       msg = await ctx.author.send(embed=embed)
                       reactions = [":incorreto:515519909330157569", ':correto:515519909434753041']
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
                           embed.add_field(name="<:letra_a:519461766623920152> Nome", value = "``"+str(nome.content)+"``", inline=True)
                           embed.add_field(name="<:numeros:518885155407003698> Idade", value = "``"+str(idade.content)+"``", inline=True)
                           embed.add_field(name="<:codigo:518775250863783947> Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                           embed.add_field(name="<:codigo:518775250863783947> Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                           embed.add_field(name="<:estrela:519465388669403136> Motivo", value = "``"+str(motivo.content)+"``", inline=True)
                           #servidor
                           server = self.bard.get_guild(498011182620475412)
                           #canal solicitação
                           channel = discord.utils.get(server.channels, id=507570211499671576)
                           msg = await channel.send(embed=embed, content="<@&520270344964145162>")
                           user = ctx.message.author
                           if user == ctx.message.author:
                            for reaction in reactions:
                                await msg.add_reaction(reaction)
                           
                           def check(reaction, user):
                              return user.id != 501179533194690583 and reaction.message.id == msg.id


                           reaction, author = await self.bard.wait_for('reaction_add', check=check)
                           if reaction.emoji.name == 'correto':
                              await msg.delete()
                              embed = discord.Embed(color=0x00d200)
                              embed.set_author(name="</HELPER> ACEITO", icon_url=ctx.author.avatar_url_as())
                              embed.add_field(name="<:letra_a:519461766623920152> Helper", value ="``"+str(ctx.author)+"`` (<@"+str(ctx.author.id)+">)", inline=True)
                              embed.add_field(name="<:numeros:518885155407003698> ID", value ="``"+str(ctx.author.id)+"``", inline=True)
                              embed.add_field(name="<:codigo:518775250863783947> Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                              embed.add_field(name="<:codigo:518775250863783947> Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                              embed.add_field(name="<:usuario:519194953042100262> Aceito por", value = f"<@{author.id}>", inline=True)
                              embed.set_thumbnail(url=ctx.author.avatar_url_as())
                              embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
                              server = self.bard.get_guild(498011182620475412)
                              channel = discord.utils.get(server.channels, id=527142906406895636)
                              await channel.send(embed=embed)
                              mongo = MongoClient(config.database.database)
                              bard = mongo['bard']
                              users = bard['users']
                              users = bard.users.find_one({"_id": str(ctx.author.id)})
                              if users is None:
                                 print("[Helper] : inserido")
                                 serv ={"_id": str(ctx.author.id),"nome": str(nome.content),"id": str(ctx.author.id),"foi_mute":"Não","vezes_mute":"0","foi_devhelper":"Não","vezes_reportado":"0","reputação":int(0),"level":"0","exp":"0","aceito_por":str(author.id),"historico":"Sem punições","bots":["SD"]}
                                 bard.users.insert_one(serv).inserted_id
                                 server = self.bard.get_guild(498011182620475412)
                                 cargo = discord.utils.get(server.roles, name="</New Helper>")
                                 await ctx.author.add_roles(cargo)
                                 if str(lang1.content) == "python":
                                   cargo = discord.utils.get(server.roles, name="</NewHelper Python>")
                                   await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "javascript":
                                    cargo = discord.utils.get(server.roles, name="</NewHelper Javascript")
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
                                   cargo = discord.utils.get(server.roles, name="</NewHelper>Python/Discord.py")
                                   await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "javascript":
                                    cargo = discord.utils.get(server.roles, name="</NewHelper>Javascript/Discord.js")
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
                                 server = self.bard.get_guild(498011182620475412)
                                 cargo = discord.utils.get(server.roles, name="</NewHelper>")
                                 await ctx.author.add_roles(cargo)
                                 if str(lang1.content) == "python":
                                   cargo = discord.utils.get(server.roles, name="</NewHelper>Python/Discord.py")
                                   await ctx.author.add_roles(cargo)
                                 elif str(lang1.content) == "javascript":
                                    cargo = discord.utils.get(server.roles, name="</NewHelper>Javascript/Discord.js")
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
                                   cargo = discord.utils.get(server.roles, name="</NewHelper>Python/Discord.py")
                                   await ctx.author.add_roles(cargo)
                                 elif str(lang2.content) == "javascript":
                                    cargo = discord.utils.get(server.roles, name="</NewHelper>Javascript/Discord.js")
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
                                   embed = discord.Embed(description=f"<:incorreto:571040727643979782> **|** Diga-me o motivo da recusa do **Helper** ``{str(usuario)}``", color=0x00d200)
                                   server = self.bard.get_guild(498011182620475412)
                                   channel = discord.utils.get(server.channels, id=527142906406895636)
                                   await channel.send(embed=embed)                                   
                                   recused = await self.bard.wait_for('message') 
                                   if recused.content.lower().startswith("motivo :"):
                                      await msg.delete()
                                      embed = discord.Embed(color=0x00d200)
                                      embed.set_author(name="</HELPER> RECUSADO", icon_url=ctx.author.avatar_url_as())
                                      embed.add_field(name="<:letra_a:519461766623920152> Helper", value ="``"+str(ctx.author)+"`` (<@"+str(ctx.author.id)+">)", inline=True)
                                      embed.add_field(name="<:numeros:518885155407003698> ID", value ="``"+str(ctx.author.id)+"``", inline=True)
                                      embed.add_field(name="<:codigo:518775250863783947> Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                                      embed.add_field(name="<:codigo:518775250863783947> Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                                      embed.add_field(name="<:usuario:519194953042100262> Aceito por", value = f"<@{author.id}>", inline=True)
                                      embed.add_field(name="<:proibido:518648641791983616> Motivo", value = f"``{recused.content}``", inline=True)
                                      embed.set_thumbnail(url=ctx.author.avatar_url_as())
                                      embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
                                      server = self.bard.get_guild(498011182620475412)
                                      #canal solicitação
                                      channel = discord.utils.get(server.channels, id=507498277097177098)
                                      await channel.send(embed=embed)
         except asyncio.TimeoutError:             
             await msg.delete()
             embed = discord.Embed(colour=0x00d200)
             embed=discord.Embed(description=f"<:tempo:518615474120949789> **|** Olá **{ctx.author.name}**, passou do tempo limite e por isso a cadastramento foi cancelado.", color=0x00d200)
             msg = await ctx.author.send(embed=embed)
             await asyncio.sleep(30)
             await msg.delete()


        except discord.errors.Forbidden:
             await msg.delete()
             embed = discord.Embed(colour=0x00d200)
             embed=discord.Embed(description=f"<:messagem:518615610721173505> **|** Olá **{ctx.author.name}**, para iniciar o processo precisamos que você libere suas mensagens privadas.", color=0x00d200)
             msg = await ctx.send(embed=embed)
             await asyncio.sleep(30)
             await msg.delete()
                      


def setup(bard):
    print("[Bot] : Cmd (helper) ")
    bard.add_cog(helper(bard))
