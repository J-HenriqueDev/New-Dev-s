
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

class help():
    def __init__(self, bard):
        self.bard = bard
    
    

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def help(self,ctx):
        if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:518624535742906371")
           return

        embed=discord.Embed(title="Lista de comandos",colour=0x7BCDE8)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="<:servidor:519460738172190720> Servidor", value="``userinfo`` ``serverinfo``", inline=False)
        embed.add_field(name="<:bot:518620111448309770> Bots", value="``botinfo`` ``addbot``", inline=False)
        embed.add_field(name="<:cadeado:519465029079400449> Moderação", value="``clear``", inline=True)
        embed.add_field(name="<:usuario:519194953042100262> Helper", value="``helper`` ``rep`` ``tophelper``", inline=True)
        embed.set_footer(text="Bard ® 2019")
        await ctx.send(embed=embed)

def setup(bard):
    print("[Bot] : Cmd (help) ")
    bard.add_cog(help(bard))
