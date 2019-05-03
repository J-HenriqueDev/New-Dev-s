

import discord
from discord.ext import commands
import random
import json
import config.database
import config.db
import sys
from datetime import datetime
import time
class debug():
    def __init__(self, bard):
        self.bard = bard



    @commands.guild_only()
    @commands.command()
    async def debug(self, ctx, *, args):
       if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:518624535742906371")
           return
       try:
         erro = '```py\n{}```'.format(eval(args))
         embed = discord.Embed(description=str(erro), color=0x3499DB)
         await ctx.send(embed=embed)
       except Exception as e:

               erro = ('```py\n{}```'.format(str(e)))
               embed = discord.Embed(description=str(erro), color=0x3499DB)
               await ctx.send(embed=embed)



def setup(bard):
    print("[Bot] : Cmd (debug) ")
    bard.add_cog(debug(bard))
