import discord
from discord.ext import commands
import requests


class cu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    

def setup(bot):
    bot.add_cog(cu(bot))