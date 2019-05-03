
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


class cmdtop():
    def __init__(self, bard):
        self.bard = bard
   

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def bestcmd(self, ctx):
        if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:518624535742906371")
           return
        mongo = MongoClient(config.database.database)
        bard = mongo['bard']
        cmds = bard['cmds']
        top = cmds.find().sort('gostei', pymongo.DESCENDING).limit(10)
        valores = {}
        cmds = {}
        index = 1
        texto = []
        rank = []
        for valor in top:
          count = len(rank)
          simb = "count°"
          numero = f"{count}{simb}"
          simbolo = str(numero).replace("0count°", "🥇 **1°**").replace("1count°","🥈 **2°**").replace("2count°","🥉 **3°**").replace("3count°","🏅 **4°**").replace("4count°","🏅 **5°**").replace("5count°","🏅 **6°**").replace("6count°","🏅 **7°**").replace("7count°","🏅 **8°**").replace("8count°","🏅 **9°**").replace("9count°","🏅 **10°**")
          msg = str(valor['_id']).replace("_py", " (py)").replace("_js", " (js)")
          url = f"{simbolo} : ``{msg}`` - ({valor['gostei']}) por <@{valor['enviado_por']}>"
          rank.append(url)
           

        url = "\n".join(rank)
        embed=discord.Embed(description=url, color=0x7BCDE8)
        embed.set_author(name="Top rank dos melhores comandos", icon_url=ctx.author.avatar_url_as())
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/519287277499973632/522607596851691524/icons8-leaderboard-100.png")
        embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
        await ctx.send(embed=embed)

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def worsecmd(self, ctx):
        if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:518624535742906371")
           return
        mongo = MongoClient(config.database.database)
        bard = mongo['bard']
        cmds = bard['cmds']
        top = cmds.find().sort('no_gostei', pymongo.DESCENDING).limit(10)
        valores = {}
        cmds = {}
        index = 1
        texto = []
        rank = []
        for valor in top:
          count = len(rank)
          simb = "count°"
          numero = f"{count}{simb}"
          simbolo = str(numero).replace("0count°", "🥇 **1°**").replace("1count°","🥈 **2°**").replace("2count°","🥉 **3°**").replace("3count°","🏅 **4°**").replace("4count°","🏅 **5°**").replace("5count°","🏅 **6°**").replace("6count°","🏅 **7°**").replace("7count°","🏅 **8°**").replace("8count°","🏅 **9°**").replace("9count°","🏅 **10°**")
          msg = str(valor['_id']).replace("_py", " (py)").replace("_js", " (js)")
          url = f"{simbolo} : ``{msg}`` - ({valor['no_gostei']}) por <@{valor['enviado_por']}>"
          rank.append(url)
           

        url = "\n".join(rank)
        embed=discord.Embed(description=url, color=0x7BCDE8)
        embed.set_author(name="Top rank dos melhores comandos", icon_url=ctx.author.avatar_url_as())
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/519287277499973632/522607596851691524/icons8-leaderboard-100.png")
        embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
        await ctx.send(embed=embed)

def setup(bard):
    print("[Server] : Cmd (cmdtop) ")
    bard.add_cog(cmdtop(bard))
