
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

class mute():
    def __init__(self, bard):
        self.bard = bard



    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def mute(self, ctx, *, user: discord.Member = None):
         if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:518624535742906371")
           return
         channel = discord.utils.get(ctx.guild.channels, id=523490486401499157)
         message = await channel.get_message(523511092920451098)
         message1 = await channel.get_message(523511105113423884)
         message2 = await channel.get_message(523511110683459594)
         message3 = await channel.get_message(523511114387030017)

         await message.remove_reaction(":python:507486258184978443", member=user)
         await message.remove_reaction(":js:507487247604514826", member=user)
         await message.remove_reaction(":kt:507488880824418305", member=user)
         await message.remove_reaction(":go:507489369041403904", member=user)
         await message.remove_reaction(":java:507488363767660545", member=user)

         await message1.remove_reaction(":berinjela:515552584543633409", member=user)
         await message1.remove_reaction(":ruby:507489813017133056", member=user)
         await message1.remove_reaction(":php:521167543034183680", member=user)
         await message1.remove_reaction(":htcs:520417824867614761", member=user)
         await message1.remove_reaction(":update:507490959198519308", member=user)

         await message2.remove_reaction(":linux:519662273363443734", member=user)
         await message2.remove_reaction(":tametirando:507925591282941963", member=user)
         await message2.remove_reaction(":designer:509411177281880084", member=user)
         await message2.remove_reaction(":youtube:515550311981514772", member=user)
         await message2.remove_reaction(":dmb:515549320385265688", member=user)

         await message3.remove_reaction(":mac:519690472533524490", member=user)
         await message3.remove_reaction(":windows:519662275150217226", member=user)
         mute = discord.utils.get(ctx.guild.roles, name="</Muted>")

         await user.add_roles(mute)

         embed=discord.Embed(description=f"<:cool:521807306741121024> **|** O usuário {user.name} ({user.id}) foi mutado!", color=0x7BCDE8)
         await ctx.send(embed=embed)





def setup(bard):
    print("[Moderation] : Cmd (mute) ")
    bard.add_cog(mute(bard))
