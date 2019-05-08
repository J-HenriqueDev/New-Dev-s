
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
import config.time

class message(commands.Cog):
    def __init__(self, bard):
        self.bard = bard

	@commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        
        error = getattr(error, 'original', error)
        

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CommandOnCooldown):
      
            gg = '{}'.format(round(error.retry_after, 1))
            embed=discord.Embed(description=f"<:timer:565975875988750336> **|** Aguarde "+str(config.time.tempopt(gg))+" para executar este comando novamente!", color=0x7BCDE8)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()


def setup(bard):
    print("[Event] : Cmd (message) ")
    bard.add_cog(message(bard))
