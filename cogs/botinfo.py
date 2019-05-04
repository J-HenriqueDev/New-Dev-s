
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




class botinfo(commands.Cog):
    def __init__(self, bard):
        self.bard = bard


    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def botinfo(self,ctx, *, word=None):
        if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:571040727643979782")
           return
        if word is None:
           embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Você não marcou um **BOT** para visualizar sua Informações.", color=0x7BCDE8)
           msg = await ctx.send(embed=embed)
           await asyncio.sleep(30)
           await msg.delete()
           return
        
        mongo = MongoClient(config.database.database)
        bard = mongo['bard']
        bot = bard['bot']
        numero = str(word).replace("<","").replace(">","").replace("@","").replace("!","")
        bot = bard.bot.find_one({"_id": str(numero)})
        
        if bot is None:
           embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** o <@{numero}>** que você forneceu não está registrado em meu banco de dados!", color=0x7BCDE8)
           msg = await ctx.send(embed=embed)
           await asyncio.sleep(30)
           await msg.delete()
           return

        usuario = await self.bard.get_user_info(numero)
        aceito = await self.bard.get_user_info(bot["aceito"])
        dono = await self.bard.get_user_info(bot["dono"])

        embed = discord.Embed(color=0x7BCDE8)
        embed.set_author(name="Informações (BOT)", icon_url=ctx.author.avatar_url_as())
        embed.add_field(name="<:bot:518620111448309770> Bot", value = "``"+str(usuario)+"``", inline=True)
        embed.add_field(name="<:numeros:518885155407003698> Id", value = "``"+str(usuario.id)+"``", inline=True)
        embed.add_field(name="<:hastag:518647415490871297> Prefixo", value = "``"+str(bot["prefixo"])+"``", inline=True)
        embed.add_field(name="<:codigo:518775250863783947> Linguagem", value = "``"+str(bot["linguagem"])+"``", inline=True)
        embed.add_field(name="<:usuario:519194953042100262> Dono", value =  "``"+str(dono)+"``", inline=True)
        embed.add_field(name="<:estrela:519465388669403136> Reputação", value =  "``"+str(bot["reputação"])+"``", inline=True)
        embed.add_field(name="<:check:520444915310788608> Aceito por", value = "``"+str(aceito)+"``", inline=True)
        embed.add_field(name="<:local:519464624299573274> Convite", value = f"[Link](https://discordapp.com/api/oauth2/authorize?client_id={usuario.id}&permissions=0&scope=bot)", inline=True)

        embed.set_thumbnail(url=usuario.avatar_url_as())
        embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
        await ctx.send(embed=embed)


def setup(bard):
    print("[Bot] : Cmd (botinfo) ")
    bard.add_cog(botinfo(bard))
