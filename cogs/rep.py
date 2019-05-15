
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

startTime = time.time()
def getUptime():
  return time.time() - startTime  

timetime=dict()


class rep(commands.Cog):
    def __init__(self, bard):
        self.bard = bard
    
    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def cooldown(self, ctx):
             if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
               await ctx.message.add_reaction(":incorreto:571040727643979782")
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
                   embed=discord.Embed(description=f"<:timer:565975875988750336> **|** Olá **{ctx.author.name}**, você precisa esperar **{str(string)}** para da uma nova reputação ao usuário.", color=0x7289DA)
                   await ctx.send(embed=embed)
                   return
             embed=discord.Embed(description=f"<:timer:565975875988750336> **|** Olá **{ctx.author.name}**, seu tempo está zerado.", color=0x7289DA)
             await ctx.send(embed=embed)


    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command(description='Dê um ponto de reputação para quando um </New Helper> lhe ajudar.',usage='c.rep </New Helper>')
    async def rep(self, ctx, *, user: discord.Member = None):
           if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
               await ctx.message.add_reaction(":incorreto:571040727643979782")
               return
           if user is None:
              embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, mencione o usuário que você gostaria de dá a reputação.", color=0x7289DA)
              msg = await ctx.send(embed=embed)
              await asyncio.sleep(20)
              await msg.delete()              
              return
           else:
             usuario = user
             if usuario.bot is True:
                embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, não é possível dá reputação ao um **BOT**.", color=0x7289DA)
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(20)
                await msg.delete()              
                return
             if not str("</New Helper>") in [r.name for r in user.roles if r.name != "@everyone"]:
                embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, o usuário {user.mention} não é um **</NewHelper>** registrado.", color=0x7289DA)
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(20)
                await msg.delete()              
                return
             if ctx.author.id == user.id:
                embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá **{ctx.author.name}**, não é possível dá reputação a si mesmo.", color=0x7289DA)
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(20)
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
                   embed=discord.Embed(description=f"<:timer:565975875988750336> **|** Olá **{ctx.author.name}**, você precisa esperar **{str(string)}** para da uma nova reputação ao usuário.", color=0x7289DA)
                   await ctx.send(embed=embed)
                   return
             mongo = MongoClient(config.database.database)
             bard = mongo['bard']
             users = bard['users']
             usuario = bard.users.find_one({'_id': str(usuario.id)})
             if usuario is None:
                embed=discord.Embed(description=f"<:correto:571040855918379008> **|** Olá **{ctx.author.name}**, você deu **1** de reputação ao usuário {user.mention}.", color=0x7289DA)
                await ctx.send(embed=embed)
                rep = int(usuario["reputação"])+int(1)
                bard.users.update_one({'_id': str(user.id)}, {'$set': {'reputação':int(rep)}})
             else:
               embed=discord.Embed(description=f"<:correto:571040855918379008> **|** Olá **{ctx.author.name}**, você deu **1** de reputação ao usuário {user.mention}.", color=0x7289DA)
               await ctx.send(embed=embed)
               rep = int(usuario["reputação"])+int(1)
               bard.users.update_one({'_id': str(user.id)}, {'$set': {'reputação':int(rep)}})

    @commands.command(
      name='delrep',
      description='Reseta os pontos mensais de reputação de todos os helpers',
      usage='c.delrep'
    )
    async def _resetarreps(self, ctx):
       if not ctx.author.id in self.bard.staff:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
       mongo = MongoClient(config.database.database)
       bard = mongo['bard']
       users = bard['users']
       bard.users.update_many({}, {"$set": {"reputação": 0}})
       await ctx.send(f"<:correto:571040855918379008> | **{ctx.author.name}**, você resetou os reps de todo mundo.")


    @commands.command()
    async def reps(self, ctx, membro: discord.Member = None):
         if membro is None:
            usuario = ctx.author
            titulo = f"Olá {usuario.name}, veja a sua quantidade de rep's a baixo."
         else:
              usuario = membro
              titulo = f"Olá {ctx.author.name}, veja a quantidade de rep's de `{usuario.name}` abaixo."
         embed = discord.Embed(description=titulo,colour=0x7289DA)
         mongo = MongoClient(config.database.database)
         bard = mongo['bard']
         users = bard['users']
         users = bard.users.find_one({"_id": str(usuario.id)})
         if not users is None:
            embed.add_field(name=f"Reputação:", value =  "``"+str(users["reputação"])+"``", inline=True)
         if users is None:
            return await ctx.send(f'**{ctx.author.name}** o usuário `{membro.name}` não está registrado.')
        
         await ctx.send(embed=embed)

def setup(bard):
    bard.add_cog(rep(bard))
