
import discord
from discord.ext import commands
import random
import time
import asyncio
from pymongo import MongoClient
import pymongo
import json

timetime=dict()

class cmds(commands.Cog):
    def __init__(self, bard):
        self.bard = bard

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=["cmd_js"])
    async def x_cmd(self,ctx, *,word=None):   
           if not str(ctx.channel.id) in self.bard.canais and not str(ctx.message.author.id) in self.bard.staff:
               await ctx.message.add_reaction(":incorreto:571040727643979782")
               return
           if word is None:
              embed=discord.Embed(description=f"{self.bard._emojis['incorreto']} **|** Olá **{ctx.author.name}**, para buscar seu comando digite **c.cmd py (nome comando)** ou **c.cmd js (nome comando)** para sua busca ter exito.", color=0x7289DA)
              msg = await ctx.send(embed=embed)
              await asyncio.sleep(18)
              await msg.delete()
              return           
           cmd = f"{word}_js"
           mongo = MongoClient(self.bard.database)
           bard = mongo['bard']
           cmds = bard['cmds']
           cmds = bard.cmds.find_one({"_id": str(cmd)})
           if cmds is None:
              embed=discord.Embed(description=f"{self.bard._emojis['incorreto']} **|** Olá **{ctx.author.name}**, o comando **{word}** não existe salvo em meu banco de dados.", color=0x7289DA)
              msg = await ctx.send(embed=embed)
              await asyncio.sleep(5)
              await msg.delete()
              return           
           if ctx.author.id in timetime:
                w = json.loads(timetime[ctx.author.id])
                if time.time() < w:
                   w = int(w) - int(time.time())
                   minute = 60
                   hour = minute * 60
                   day = hour * 24
                   days =  int(w / day)
                   hours = int((w % day) / hour)
                   minutes = int((w % hour) / minute)
                   seconds = int(w % minute)
                   string = ""
                   if days > 0:
                      string += str(days) + " " + (days == 1 and "dia" or "dias" ) + ", "
                   if len(string) > 0 or hours > 0:
                      string += str(hours) + " " + (hours == 1 and "hora" or "horas" ) + ", "
                   if len(string) > 0 or minutes > 0:
                      string += str(minutes) + " " + (minutes == 1 and "minuto" or "minutos" ) + ", "
                   string += str(seconds) + " " + (seconds == 1 and "segundo" or "segundos" )
                   pv = f"```py\n"+str(cmds["code"])+"```" 
                   embed=discord.Embed(description=str(pv), color=0x7289DA)
                   embed.set_author(name="INFORMAÇÕES (CMD)", icon_url=ctx.author.avatar_url_as())
                   embed.add_field(name=f"{self.bard._emojis['nome']} Nome", value = "``"+str(cmds["_id"]).replace("_py","")+"``", inline=True)
                   embed.add_field(name=f"{self.bard._emojis['api']} Linguagem ", value = "``"+str(cmds["linguagem"])+"``", inline=True)
                   embed.add_field(name=f"{self.bard._emojis['seta']} String", value = "``"+str(cmds["string"])+"``", inline=True)
                   embed.add_field(name=f"{self.bard._emojis['link']} Link", value = "[link]("+str(cmds["link"])+")", inline=True)
                   enviado = await self.bard.get_user(cmds["enviado_por"])
                   aceito = await self.bard.get_user(cmds["aceito_por"])
                   embed.add_field(name=f"{self.bard._emojis['mention']} Enviado por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
                   embed.add_field(name=f"{self.bard._emojis['mention']} Aceito por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
                   embed.add_field(name=f"<:gostei:533672310729605141> Gostaram", value = "``"+str(cmds["gostei"])+"``", inline=True)
                   embed.add_field(name=f"<:nao_gostei:533672311841226753> Não gostaram", value = "``"+str(cmds["no_gostei"])+"``", inline=True)
                   embed.add_field(name="⠀⠀", value = f"{self.bard._emojis['timer']} Olá **{ctx.author.name}**, você precisa esperar **{str(string)}** para dar denovo reputação ao um comando.", inline=True)
                   await ctx.send(embed=embed)
                   return
           pv = f"```py\n"+str(cmds["code"])+"```" 
           embed=discord.Embed(description=str(pv), color=0x7289DA)
           embed.set_author(name="INFORMAÇÕES (CMD)", icon_url=ctx.author.avatar_url_as())
           embed.add_field(name=f"{self.bard._emojis['nome']} Nome", value = "``"+str(cmds["_id"]).replace("_py","")+"``", inline=True)
           embed.add_field(name=f"{self.bard._emojis['api']} Linguagem ", value = "``"+str(cmds["linguagem"])+"``", inline=True)
           embed.add_field(name=f"{self.bard._emojis['seta']} String", value = "``"+str(cmds["string"])+"``", inline=True)
           embed.add_field(name=f"{self.bard._emojis['link']} Link", value = "[link]("+str(cmds["link"])+")", inline=True)
           enviado = await self.bard.get_user(cmds["enviado_por"])
           aceito = await self.bard.get_user(cmds["aceito_por"])
           embed.add_field(name=f"{self.bard._emojis['mention']} Enviado por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
           embed.add_field(name=f"{self.bard._emojis['mention']} Aceito por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
           embed.add_field(name=f"<:gostei:533672310729605141> Gostaram", value = "``"+str(cmds["gostei"])+"``", inline=True)
           embed.add_field(name=f"<:nao_gostei:533672311841226753> Não gostaram", value = "``"+str(cmds["no_gostei"])+"``", inline=True)
           msg = await ctx.send(embed=embed)
           reactions = [":incorreto:571040727643979782", ':correto:571040855918379008']
           user = ctx.message.author
           if user == ctx.message.author:
              for reaction in reactions:
                  await msg.add_reaction(reaction)
           def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji)

           reaction, user = await self.bard.wait_for('reaction_add', check=check, timeout=120.0)
           if reaction.emoji.name == 'incorreto':
             count = int(cmds["no_gostei"])+int(1)
             bard.cmds.update_one({'_id': str(cmd)}, {'$set': {"no_gostei":int(count)}})
             mongo = MongoClient(self.bard.database)
             bard = mongo['bard']
             cmds = bard['cmds']
             cmds = bard.cmds.find_one({"_id": str(cmd)}) 
             pv = f"```py\n"+str(cmds["code"])+"```" 
             embed=discord.Embed(description=str(pv), color=0x7289DA)
             embed.set_author(name="INFORMAÇÕES (CMD)", icon_url=ctx.author.avatar_url_as())
             embed.add_field(name=f"{self.bard._emojis['nome']} Nome", value = "``"+str(cmds["_id"]).replace("_py","")+"``", inline=True)
             embed.add_field(name=f"{self.bard._emojis['api']} Linguagem ", value = "``"+str(cmds["linguagem"])+"``", inline=True)
             embed.add_field(name=f"{self.bard._emojis['seta']} String", value = "``"+str(cmds["string"])+"``", inline=True)
             embed.add_field(name=f"{self.bard._emojis['link']} Link", value = "[link]("+str(cmds["link"])+")", inline=True)
             enviado = await self.bard.get_user(cmds["enviado_por"])
             aceito = await self.bard.get_user(cmds["aceito_por"])
             embed.add_field(name=f"{self.bard._emojis['mention']} Enviado por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
             embed.add_field(name=f"{self.bard._emojis['mention']} Aceito por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
             embed.add_field(name=f"<:gostei:533672310729605141> Gostaram", value = "``"+str(cmds["gostei"])+"``", inline=True)
             embed.add_field(name=f"<:nao_gostei:533672311841226753> Não gostaram", value = "``"+str(cmds["no_gostei"])+"``", inline=True)
             embed.add_field(name=f"⠀⠀", value = "<:oks:533779925803466762> Parabéns, você votou que **Não gostou** do comando, e seu voto foi computado.", inline=True)
             reactions = [":incorreto:571040727643979782", ':correto:571040855918379008']
             tempo = random.randint(14400,21600)
             timetime[ctx.author.id] = json.dumps(int(time.time())+int(tempo))
             user = ctx.message.author
             if user == ctx.message.author:
                for reaction in reactions:
                    await msg.remove_reaction(reaction, member=self.bard.user)
                    await msg.remove_reaction(reaction, member=ctx.author)

             await msg.edit(embed=embed)
           if reaction.emoji.name == 'correto':
                count = int(cmds["gostei"])+int(1)
                bard.cmds.update_one({'_id': str(cmd)}, {'$set': {"gostei":int(count)}})
                mongo = MongoClient(self.bard.database)
                bard = mongo['bard']
                cmds = bard['cmds']
                cmds = bard.cmds.find_one({"_id": str(cmd)}) 
                pv = f"```py\n"+str(cmds["code"])+"```" 
                embed=discord.Embed(description=str(pv), color=0x7289DA)
                embed.set_author(name="INFORMAÇÕES (CMD)", icon_url=ctx.author.avatar_url_as())
                embed.add_field(name=f"{self.bard._emojis['nome']} Nome", value = "``"+str(cmds["_id"]).replace("_py","")+"``", inline=True)
                embed.add_field(name=f"{self.bard._emojis['api']} Linguagem ", value = "``"+str(cmds["linguagem"])+"``", inline=True)
                embed.add_field(name=f"{self.bard._emojis['seta']} String", value = "``"+str(cmds["string"])+"``", inline=True)
                embed.add_field(name=f"{self.bard._emojis['link']} Link", value = "[link]("+str(cmds["link"])+")", inline=True)
                enviado = await self.bard.get_user(cmds["enviado_por"])
                aceito = await self.bard.get_user(cmds["aceito_por"])
                embed.add_field(name=f"{self.bard._emojis['mention']} Enviado por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
                embed.add_field(name=f"{self.bard._emojis['mention']} Aceito por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
                embed.add_field(name=f"<:gostei:533672310729605141> Gostaram", value = "``"+str(cmds["gostei"])+"``", inline=True)
                embed.add_field(name=f"<:nao_gostei:533672311841226753> Não gostaram", value = "``"+str(cmds["no_gostei"])+"``", inline=True)
                embed.add_field(name=f"⠀⠀", value = "<:oks:533779925803466762> Parabéns, você votou que **gostou** do comando, e seu voto foi computado.", inline=True)
                reactions = [":incorreto:571040727643979782", ':correto:571040855918379008']
                tempo = random.randint(14400,21600)
                timetime[ctx.author.id] = json.dumps(int(time.time())+int(tempo))
                user = ctx.message.author
                if user == ctx.message.author:
                   for reaction in reactions:
                       await msg.remove_reaction(reaction, member=self.bard.user)
                       await msg.remove_reaction(reaction, member=ctx.author)

                await msg.edit(embed=embed)
    
    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=["cmd_py"])
    async def xx_cmd(self,ctx, *,word=None):   
           if word is None:
              embed=discord.Embed(description=f"{self.bard._emojis['incorreto']} **|** Olá **{ctx.author.name}**, para buscar seu comando digite **c.cmd py (nome comando)** ou **c.cmd js (nome comando)** para sua busca ter exito.", color=0x7289DA)
              msg = await ctx.send(embed=embed)
              await asyncio.sleep(18)
              await msg.delete()
              return           
           cmd = f"{word}_py"
           mongo = MongoClient(self.bard.database)
           bard = mongo['bard']
           cmds = bard['cmds']
           cmds = bard.cmds.find_one({"_id": str(cmd)})
           if cmds is None:
              embed=discord.Embed(description=f"{self.bard._emojis['incorreto']} **|** Olá **{ctx.author.name}**, o comando **{word}** não existe salvo em meu banco de dados.", color=0x7289DA)
              msg = await ctx.send(embed=embed)
              await asyncio.sleep(5)
              await msg.delete()
              return           
           if ctx.author.id in timetime:
                w = json.loads(timetime[ctx.author.id])
                if time.time() < w:
                   w = int(w) - int(time.time())
                   minute = 60
                   hour = minute * 60
                   day = hour * 24
                   days =  int(w / day)
                   hours = int((w % day) / hour)
                   minutes = int((w % hour) / minute)
                   seconds = int(w % minute)
                   string = ""
                   if days > 0:
                      string += str(days) + " " + (days == 1 and "dia" or "dias" ) + ", "
                   if len(string) > 0 or hours > 0:
                      string += str(hours) + " " + (hours == 1 and "hora" or "horas" ) + ", "
                   if len(string) > 0 or minutes > 0:
                      string += str(minutes) + " " + (minutes == 1 and "minuto" or "minutos" ) + ", "
                   string += str(seconds) + " " + (seconds == 1 and "segundo" or "segundos" )
                   pv = f"```py\n"+str(cmds["code"])+"```" 
                   embed=discord.Embed(description=str(pv), color=0x7289DA)
                   embed.set_author(name="INFORMAÇÕES (CMD)", icon_url=ctx.author.avatar_url_as())
                   embed.add_field(name=f"{self.bard._emojis['nome']} Nome", value = "``"+str(cmds["_id"]).replace("_py","")+"``", inline=True)
                   embed.add_field(name=f"{self.bard._emojis['api']} Linguagem ", value = "``"+str(cmds["linguagem"])+"``", inline=True)
                   embed.add_field(name=f"{self.bard._emojis['seta']} String", value = "``"+str(cmds["string"])+"``", inline=True)
                   embed.add_field(name=f"{self.bard._emojis['link']} Link", value = "[link]("+str(cmds["link"])+")", inline=True)
                   enviado = await self.bard.get_user(cmds["enviado_por"])
                   aceito = await self.bard.get_user(cmds["aceito_por"])
                   embed.add_field(name=f"{self.bard._emojis['mention']} Enviado por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
                   embed.add_field(name=f"{self.bard._emojis['mention']} Aceito por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
                   embed.add_field(name=f"<:gostei:533672310729605141> Gostaram", value = "``"+str(cmds["gostei"])+"``", inline=True)
                   embed.add_field(name=f"<:nao_gostei:533672311841226753> Não gostaram", value = "``"+str(cmds["no_gostei"])+"``", inline=True)
                   embed.add_field(name=f"⠀⠀", value = f"{self.bard._emojis['timer']} Olá **{ctx.author.name}**, você precisa esperar **{str(string)}** para dar denovo reputação ao um comando.", inline=True)
                   await ctx.send(embed=embed)
                   return
           pv = f"```py\n"+str(cmds["code"])+"```" 
           embed=discord.Embed(description=str(pv), color=0x7289DA)
           embed.set_author(name="INFORMAÇÕES (CMD)", icon_url=ctx.author.avatar_url_as())
           embed.add_field(name=f"{self.bard._emojis['nome']} Nome", value = "``"+str(cmds["_id"]).replace("_py","")+"``", inline=True)
           embed.add_field(name=f"{self.bard._emojis['api']} Linguagem ", value = "``"+str(cmds["linguagem"])+"``", inline=True)
           embed.add_field(name=f"{self.bard._emojis['seta']} String", value = "``"+str(cmds["string"])+"``", inline=True)
           embed.add_field(name=f"{self.bard._emojis['link']} Link", value = "[link]("+str(cmds["link"])+")", inline=True)
           enviado = await self.bard.get_user(cmds["enviado_por"])
           aceito = await self.bard.get_user(cmds["aceito_por"])
           embed.add_field(name=f"{self.bard._emojis['mention']} Enviado por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
           embed.add_field(name=f"{self.bard._emojis['mention']} Aceito por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
           embed.add_field(name=f"<:gostei:533672310729605141> Gostaram", value = "``"+str(cmds["gostei"])+"``", inline=True)
           embed.add_field(name=f"<:nao_gostei:533672311841226753> Não gostaram", value = "``"+str(cmds["no_gostei"])+"``", inline=True)
           msg = await ctx.send(embed=embed)
           reactions = [":incorreto:571040727643979782", ':correto:571040855918379008']
           user = ctx.message.author
           if user == ctx.message.author:
              for reaction in reactions:
                  await msg.add_reaction(reaction)
           def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji)

           reaction, user = await self.bard.wait_for('reaction_add', check=check, timeout=120.0)
           if reaction.emoji.name == 'incorreto':
             count = int(cmds["no_gostei"])+int(1)
             bard.cmds.update_one({'_id': str(cmd)}, {'$set': {"no_gostei":int(count)}})
             mongo = MongoClient(self.bard.database)
             bard = mongo['bard']
             cmds = bard['cmds']
             cmds = bard.cmds.find_one({"_id": str(cmd)}) 
             pv = f"```py\n"+str(cmds["code"])+"```" 
             embed=discord.Embed(description=str(pv), color=0x7289DA)
             embed.set_author(name="INFORMAÇÕES (CMD)", icon_url=ctx.author.avatar_url_as())
             embed.add_field(name=f"{self.bard._emojis['nome']} Nome", value = "``"+str(cmds["_id"]).replace("_py","")+"``", inline=True)
             embed.add_field(name=f"{self.bard._emojis['api']} Linguagem ", value = "``"+str(cmds["linguagem"])+"``", inline=True)
             embed.add_field(name=f"{self.bard._emojis['seta']} String", value = "``"+str(cmds["string"])+"``", inline=True)
             embed.add_field(name=f"{self.bard._emojis['link']} Link", value = "[link]("+str(cmds["link"])+")", inline=True)
             enviado = await self.bard.get_user(cmds["enviado_por"])
             aceito = await self.bard.get_user(cmds["aceito_por"])
             embed.add_field(name=f"{self.bard._emojis['mention']} Enviado por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
             embed.add_field(name=f"{self.bard._emojis['mention']} Aceito por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
             embed.add_field(name=f"<:gostei:533672310729605141> Gostaram", value = "``"+str(cmds["gostei"])+"``", inline=True)
             embed.add_field(name=f"<:nao_gostei:533672311841226753> Não gostaram", value = "``"+str(cmds["no_gostei"])+"``", inline=True)
             embed.add_field(name="⠀⠀", value = "<:oks:533779925803466762> Parabéns, você votou que **Não gostou** do comando, e seu voto foi computado.", inline=True)
             reactions = [":incorreto:571040727643979782", ':correto:571040855918379008']
             tempo = random.randint(14400,21600)
             timetime[ctx.author.id] = json.dumps(int(time.time())+int(tempo))
             user = ctx.message.author
             if user == ctx.message.author:
                for reaction in reactions:
                    await msg.remove_reaction(reaction, member=self.bard.user)
                    await msg.remove_reaction(reaction, member=ctx.author)

             await msg.edit(embed=embed)
           if reaction.emoji.name == 'correto':
                count = int(cmds["gostei"])+int(1)
                bard.cmds.update_one({'_id': str(cmd)}, {'$set': {"gostei":int(count)}})
                mongo = MongoClient(self.bard.database)
                bard = mongo['bard']
                cmds = bard['cmds']
                cmds = bard.cmds.find_one({"_id": str(cmd)}) 
                pv = f"```py\n"+str(cmds["code"])+"```" 
                embed=discord.Embed(description=str(pv), color=0x7289DA)
                embed.set_author(name="INFORMAÇÕES (CMD)", icon_url=ctx.author.avatar_url_as())
                embed.add_field(name=f"{self.bard._emojis['nome']} Nome", value = "``"+str(cmds["_id"]).replace("_py","")+"``", inline=True)
                embed.add_field(name=f"{self.bard._emojis['api']} Linguagem ", value = "``"+str(cmds["linguagem"])+"``", inline=True)
                embed.add_field(name=f"{self.bard._emojis['seta']} String", value = "``"+str(cmds["string"])+"``", inline=True)
                embed.add_field(name=f"{self.bard._emojis['link']} Link", value = "[link]("+str(cmds["link"])+")", inline=True)
                enviado = await self.bard.get_user(cmds["enviado_por"])
                aceito = await self.bard.get_user(cmds["aceito_por"])
                embed.add_field(name=f"{self.bard._emojis['mention']} Enviado por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
                embed.add_field(name=f"{self.bard._emojis['mention']} Aceito por", value = "``"+str(enviado)+"`` (<@"+str(enviado.id)+">)", inline=True)
                embed.add_field(name=f"<:gostei:533672310729605141> Gostaram", value = "``"+str(cmds["gostei"])+"``", inline=True)
                embed.add_field(name=f"<:nao_gostei:533672311841226753> Não gostaram", value = "``"+str(cmds["no_gostei"])+"``", inline=True)
                embed.add_field(name=f"⠀⠀", value = "<:oks:533779925803466762> Parabéns, você votou que **gostou** do comando, e seu voto foi computado.", inline=True)
                reactions = [":incorreto:571040727643979782", ':correto:571040855918379008']
                tempo = random.randint(14400,21600)
                timetime[ctx.author.id] = json.dumps(int(time.time())+int(tempo))
                user = ctx.message.author
                if user == ctx.message.author:
                   for reaction in reactions:
                       await msg.remove_reaction(reaction, member=self.bard.user)
                       await msg.remove_reaction(reaction, member=ctx.author)

                await msg.edit(embed=embed)

def setup(bard):
    bard.add_cog(cmds(bard))
