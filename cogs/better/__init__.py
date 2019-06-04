from discord.ext import commands
from .errors import *
from .markup import *
from .text import *
import requests

__copyright__ = "NewDev's (c) 2019"

developers = {
    'Yuka Tuka': 499321522578522112,
    'Obi Wan': 558396463873392640,
    'Razy': 456108986756759563
}

emojics = {
    'python': '<:python:576143949102841876>',
    'tag': '<:tag:576143950482767892>' 
}

def is_developer():
    async def predicate(ctx):
        if not ctx.author.id in list(developers.values()):
            raise DeveloperError('você não é um desenvolvedor.')
        return True
    return commands.check(predicate)


async def try_await(coro, onerror=lambda e, coro: coro):
    try:
        return await coro
    except Exception as e:
        return onerror(e, coro)
    return coro

def download_image(url):
    return requests.get(url).content
