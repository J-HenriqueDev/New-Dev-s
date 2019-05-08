
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
import requests
import json
prefixos = ["rd.","!","@","/"]

langs = ["python","javascript"]

string = ["cogs","on_message","handler"]

string2 = ["stable","master","rewrite","async"]


def ghost(msg):
    url = "http://sprunge.us"
    r = requests.post(url, data={"sprunge": msg.encode('utf8')}, timeout=4)
    return r.text.strip() + "?py"


class addcmd():
    def __init__(self, bard):
        self.bard = bard


    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def addcmd(self,ctx):   
        if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:518624535742906371")
           return
        try:
         try:
           embed=discord.Embed(description=f"<:messagem:518615610721173505> **|** Olá **{ctx.author.name}**, verifique sua mensagens diretas (DM).", color=0x7BCDE8)
           msg = await ctx.send(embed=embed)
           txs = f"<:new:518620334052737034> **|** Então você quer adicionar um **Comando** no Bard?\nPara isso precisamos que você preencha um pequeno formulário para cadastramento de seu **comando** em nosso sistema.\n\n<:letra_a:519461766623920152> **|** Diga-nos o nome do **comando**: \n<:tempo:518615474120949789> **|** **2 minutos**"
           embed=discord.Embed(description=txs, color=0x7BCDE8)
           msg = await ctx.author.send(embed=embed)
 
           def pred(m):
               return m.author == ctx.author and m.guild is None

           nome = await self.bard.wait_for('message', check=pred, timeout=120.0) 
           if len(nome.content) >=20:              
              await msg.delete()
              embed=discord.Embed(description=f"<:incorreto:518624535742906371> **|** Olá **{ctx.author.name}**, o **nome** do comando que você inseriu passou do limite de 20 caracteres.", color=0x7BCDE8)
              msg = await ctx.author.send(embed=embed)
              await asyncio.sleep(30)
              await msg.delete()
           else:
             await msg.delete()
             texto = f"<:new:518620334052737034> **|** Agora diga-me a linguagem que o **comando** foi feito\n<:codigo:518775250863783947> Linguagens : **python** ou **javascript**\n<:tempo:518615474120949789> **|** **2 minutos**"
             embed=discord.Embed(description=texto, color=0x7BCDE8)
             msg = await ctx.author.send(embed=embed)
             lang = await self.bard.wait_for('message', check=pred, timeout=120.0) 
             if lang.content in langs:
              await msg.delete()
              if lang.content == "python":
                 string = "**cogs** ou **on_message**"
              else:
                string = "**handler** ou **on_message**"
              texto = f"<:new:518620334052737034> **|** Agora diga-me a se o **comando** é {string}.\n<:tempo:518615474120949789> **|** **2 minutos**"
              embed=discord.Embed(description=texto, color=0x7BCDE8)
              msg = await ctx.author.send(embed=embed)
              cogs_on_message = await self.bard.wait_for('message', check=pred, timeout=120.0)
              if not cogs_on_message.content in string:
                 await msg.delete()
                 embed=discord.Embed(description=f"<:incorreto:518624535742906371> **|** Olá **{ctx.author.name}**, a **váriavel** que você inseriu é inválida.", color=0x7BCDE8)
                 msg = await ctx.author.send(embed=embed)
                 await asyncio.sleep(30)
                 await msg.delete()
              else:
                await msg.delete()
                if lang.content == "python":
                 string = "**rewrite** ou **async**"
                else:
                  string = "**stable** ou **master**"
                texto = f"<:new:518620334052737034> **|** Agora diga-me a se o **comando** foi feito em {string}\n<:tempo:518615474120949789> **|** **2 minutos**"
                embed=discord.Embed(description=texto, color=0x7BCDE8)
                msg = await ctx.author.send(embed=embed)
                rewrite_async = await self.bard.wait_for('message', check=pred, timeout=120.0)
                if not rewrite_async.content in string2:
                   await msg.delete()
                   embed=discord.Embed(description=f"<:incorreto:518624535742906371> **|** Olá **{ctx.author.name}**, a **váriavel** que você inseriu é inválida.", color=0x7BCDE8)
                   msg = await ctx.author.send(embed=embed)
                   await asyncio.sleep(30)
                   await msg.delete()
                else:
                  await msg.delete()
                  texto = f"<:new:518620334052737034> **|** Agora cole-o **comando** ou escreva ele. (limite 2000 caracteres)\n<:tempo:518615474120949789> **|** **2 minutos**"
                  embed=discord.Embed(description=texto, color=0x7BCDE8)
                  msg = await ctx.author.send(embed=embed)
                  codigo = await self.bard.wait_for('message', check=pred, timeout=120.0)
                  if len(codigo.content) >=1999:              
                      await msg.delete()
                      embed=discord.Embed(description=f"<:incorreto:518624535742906371> **|** Olá **{ctx.author.name}**, o **código** do comando que você inseriu passou do limite de 2000 caracteres.", color=0x7BCDE8)
                      msg = await ctx.author.send(embed=embed)
                      await asyncio.sleep(30)
                      await msg.delete()
                  else:
                    await msg.delete()
                    if lang.content == "python":
                       pv = f"```py\n{codigo.content}```" 
                    else:
                      pv = f"```js\n{codigo.content}```" 
                    link = ghost(codigo.content)
                    embed=discord.Embed(description=str(pv), color=0x7BCDE8)
                    embed.set_author(name="SOLICITAÇÃO ADICIONA (CMD)", icon_url=ctx.author.avatar_url_as())
                    embed.add_field(name="<:letra_a:519461766623920152> Nome", value = "``"+str(nome.content)+"``", inline=True)
                    embed.add_field(name="<:codigo:518775250863783947> Linguagem ", value = "``"+str(lang.content)+"``", inline=True)
                    embed.add_field(name="<:seta:520292614956908554> String", value = "``"+str(cogs_on_message.content)+"``", inline=True)
                    embed.add_field(name="<:link:531320331076501525> Link", value = "[link]("+str(link)+")", inline=True)
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
                       embed=discord.Embed(description=f"<:incorreto:518624535742906371> **|** A solicitação de cadastramento foi cancelada.", color=0x7BCDE8)
                       msg = await ctx.author.send(embed=embed)
                       await asyncio.sleep(30)
                       await msg.delete()
                
                    if reaction.emoji.name == 'correto':
                       await msg.delete()
                       pv = f"```py\n{codigo.content}```" 
                       link = ghost(codigo.content)
                       embed=discord.Embed(description=str(pv), color=0x7BCDE8)
                       embed.set_author(name="SOLICITAÇÃO ADICIONA (CMD)", icon_url=ctx.author.avatar_url_as())
                       embed.add_field(name="<:letra_a:519461766623920152> Nome", value = "``"+str(nome.content)+"``", inline=True)
                       embed.add_field(name="<:codigo:518775250863783947> Linguagem ", value = "``"+str(lang.content)+"``", inline=True)
                       embed.add_field(name="<:seta:520292614956908554> String", value = "``"+str(cogs_on_message.content)+"``", inline=True)
                       embed.add_field(name="<:link:531320331076501525> Link", value = "[link]("+str(link)+")", inline=True)
                       embed.add_field(name="<:usuario:519194953042100262> Enviado por", value = "``"+str(ctx.author)+"`` ("+str(ctx.author.mention)+")", inline=True)
                       server = self.bard.get_guild(498011182620475412)
                       #canal solicitação
                       channel = discord.utils.get(server.channels, id=507570211499671576)
                       msg = await channel.send(embed=embed, content="<@&520270344964145162>")
                       user = ctx.message.author
                       if user == ctx.message.author:
                          for reaction in reactions:
                              await msg.add_reaction(reaction)
                           
                       def check(reaction, user):
                           return user.id != 515981047578492933 and reaction.message.id == msg.id

                       reaction, author = await self.bard.wait_for('reaction_add', check=check)                
                       if reaction.emoji.name == 'correto':
                          await msg.delete()
                          embed = discord.Embed(color=0x7BCDE8)
                          embed.set_author(name="CÓDIGO ACEITO (CMD)", icon_url=ctx.author.avatar_url_as())
                          embed.add_field(name="<:letra_a:519461766623920152> Nome", value = "``"+str(nome.content)+"``", inline=True)
                          embed.add_field(name="<:codigo:518775250863783947> Linguagem ", value = "``"+str(lang.content)+"``", inline=True)
                          embed.add_field(name="<:seta:520292614956908554> String", value = "``"+str(cogs_on_message.content)+"``", inline=True)
                          embed.add_field(name="<:link:531320331076501525> Link", value = "[link]("+str(link)+")", inline=True)
                          embed.add_field(name="<:usuario:519194953042100262> Enviado por", value = "``"+str(ctx.author)+"`` ("+str(ctx.author.mention)+")", inline=True)
                          embed.add_field(name="<:usuario:519194953042100262> Aceito por", value = "``"+str(author)+"`` ("+str(author.mention)+")", inline=True)
                          embed.set_thumbnail(url=ctx.author.avatar_url_as())
                          embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
                          server = self.bard.get_guild(498011182620475412)
                          channel = discord.utils.get(server.channels, id=533508786888114196)
                          await channel.send(embed=embed)
                          mongo = MongoClient(config.database.database)
                          bard = mongo['bard']
                          cmds = bard['cmds']
                          cmds = bard.cmds.find_one({"_id": str(nome.content)})
                          if cmds is None:
                           if lang.content == "python":
                              pv = f"{nome.content}_py" 
                           else:
                             pv = f"{nome.content}_js" 
                           print("[comando] : inserido")
                           serv ={"_id": str(pv.lower()), "code": str(codigo.content),"linguagem": str(lang.content),"string": str(cogs_on_message.content), "link":str(link), "enviado_por":int(ctx.author.id),"aceito_por":int(author.id), "gostei":int(0),"no_gostei":int(0)}
                           bard.cmds.insert_one(serv).inserted_id
                           return

                       if reaction.emoji.name == 'incorreto':
                         embed = discord.Embed(description=f"<:incorreto:518624535742906371> **|** Diga-me o motivo da recusa do **comando** ``{str(nome.content)}``", color=0x7BCDE8)
                         server = self.bard.get_guild(498011182620475412)
                         channel = discord.utils.get(server.channels, id=533508786888114196)
                         await channel.send(embed=embed)                                   
                         recused = await self.bard.wait_for('message') 
                         if recused.content.lower().startswith("motivo :"):                          
                           embed = discord.Embed(color=0x7BCDE8)
                           embed.set_author(name="CÓDIGO RECUSADO (CMD)", icon_url=ctx.author.avatar_url_as())
                           embed.add_field(name="<:letra_a:519461766623920152> Nome", value = "``"+str(nome.content)+"``", inline=True)
                           embed.add_field(name="<:codigo:518775250863783947> Linguagem ", value = "``"+str(lang.content)+"``", inline=True)
                           embed.add_field(name="<:seta:520292614956908554> String", value = "``"+str(cogs_on_message.content)+"``", inline=True)
                           embed.add_field(name="<:link:531320331076501525> Link", value = "[link]("+str(link)+")", inline=True)
                           embed.add_field(name="<:usuario:519194953042100262> Enviado por", value = "``"+str(ctx.author)+"`` ("+str(ctx.author.mention)+")", inline=True)
                           embed.add_field(name="<:usuario:519194953042100262> Recusado por", value = "``"+str(author)+"`` ("+str(author.mention)+")", inline=True)
                           embed.add_field(name="<:proibido:518648641791983616> Motivo", value = f"``{recused.content}``", inline=True)
                           embed.set_thumbnail(url=ctx.author.avatar_url_as())
                           embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
                           server = self.bard.get_guild(498011182620475412)
                           channel = discord.utils.get(server.channels, id=533508786888114196)
                           await channel.send(embed=embed)


             else:
               texto = f"<:new:518620334052737034> **|** A linguagem que você inseriu é invalida."
               embed=discord.Embed(description=texto, color=0x7BCDE8)
               msg = await ctx.author.send(embed=embed)
               await asyncio.sleep(30)
               await msg.delete()
           
         except asyncio.TimeoutError:             
             await msg.delete()
             embed = discord.Embed(colour=0x7BCDE8)
             embed=discord.Embed(description=f"<:tempo:518615474120949789> **|** Olá **{ctx.author.name}**, passou do tempo limite e por isso a cadastramento foi cancelado.", color=0x7BCDE8)
             msg = await ctx.author.send(embed=embed)
             await asyncio.sleep(30)
             await msg.delete()


        except discord.errors.Forbidden:
             await msg.delete()
             embed = discord.Embed(colour=0x7BCDE8)
             embed=discord.Embed(description=f"<:messagem:518615610721173505> **|** Olá **{ctx.author.name}**, para iniciar o processo precisamos que você libere suas mensagens privadas.", color=0x7BCDE8)
             msg = await ctx.send(embed=embed)
             await asyncio.sleep(30)
             await msg.delete()
                      


def setup(bard):
    print("[Bot] : Cmd (addcmd) ")
    bard.add_cog(addcmd(bard))
