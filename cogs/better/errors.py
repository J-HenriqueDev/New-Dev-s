from discord.ext import commands
import discord

class DeveloperError(commands.CommandError):
    def __init__(self, message=None, *args):
        super().__init__(message, *args)