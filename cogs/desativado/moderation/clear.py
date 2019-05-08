
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
numeros = ["1","2","3"]

class clear():
    def __init__(self, bard):
        self.bard = bard

    @commands.command()
    async def feedbeck(self,ctx):
       await ctx.message.delete()
       embed=discord.Embed(description=f"Seu produto acaba de ser ativo! (EMBED)", color=0x7BCDE8)
       msg = await ctx.send(embed=embed)
       embed=discord.Embed(description=f"De uma nota de 0 a 5 pro suporte.", color=0x7BCDE8)
       msg2 = await ctx.send(embed=embed)
       def pred(m):
         return m.author == ctx.author

       message1 = await self.bard.wait_for('message', check=pred, timeout=120.0) 
       if message1.content:
        await msg.delete()
        await msg2.delete()
        embed=discord.Embed(description=f"Escreva seu feedback", color=0x7BCDE8)
        msg2 = await ctx.send(embed=embed)
        message2 = await self.bard.wait_for('message', check=pred, timeout=120.0) 
        if message2.content:
         await msg2.delete()
         produto = "nada"
         embed=discord.Embed(description=f"Usuário : {ctx.author.mention}\nProduto : {produto}\nFeedback : {message2.content}", color=0x7BCDE8)
         embed.set_author(name="SISTEMA DE FEEDBACK", icon_url=ctx.author.avatar_url_as())
         canal = discord.utils.get(ctx.guild.channels, id=520367302798082058)
         await canal.send(embed=embed)


    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def clear(self,ctx,* ,num=None):
        if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:518624535742906371")
           return
        try:
          if str(ctx.author.id) in config.database.admin:
            numero = int(num)
            if numero>100:
               numb = 100
               await ctx.channel.purge(limit=numb)
               embed=discord.Embed(description=f"<:correto:518624536082776084> **|** Foram apagadas **{numb}** mensagens.", color=0x7BCDE8)
               msg = await ctx.send(embed=embed)
               await asyncio.sleep(10)
               await msg.delete()
            elif numero>0:
               await ctx.channel.purge(limit=numero)
               embed=discord.Embed(description=f"<:correto:518624536082776084> **|** Foram apagadas **{numero}** mensagens.", color=0x7BCDE8)
               msg = await ctx.send(embed=embed)
               await asyncio.sleep(10)
               await msg.delete()
            else:
              embed=discord.Embed(description=f"<:incorreto:518624535742906371> **|** Insirá um valor válido entre (1 a 100).", color=0x7BCDE8)
              msg = await ctx.send(embed=embed)
              await asyncio.sleep(10)
              await msg.delete()
        except ValueError:
             embed=discord.Embed(description=f"<:incorreto:518624535742906371> **|** Insirá um valor válido entre (1 a 100).", color=0x7BCDE8)
             msg = await ctx.send(embed=embed)
             await asyncio.sleep(10)
             await msg.delete()





def setup(bard):
    print("[Moderation] : Cmd (clear) ")
    bard.add_cog(clear(bard))
