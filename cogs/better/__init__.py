from discord.ext import commands
from .errors import *
from .markup import *

__copyright__ = "NewDev's (c) 2019"

developers = {
    'Yuka Tuka': 499321522578522112,
    'Obi Wan': 558396463873392640,
    'Razy': 456108986756759563
}

def is_developer():
    async def predicate(ctx):
        return ctx.author.id in list(developers.values())
    return commands.check(predicate)


async def try_await(coro, onerror=lambda e, coro: coro):
    try:
        return await coro
    except Exception as e:
        return onerror(e, coro)
    return coro
