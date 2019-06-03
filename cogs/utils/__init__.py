from discord.ext import commands

developers = {
    'Yuka Tuka': 499321522578522112,
    'Obi Wan': 558396463873392640,
    'Razy': 456108986756759563
}

def is_owner():
    async def predicate(ctx):
        return ctx.author.id in list(developers.values())
    return commands.check(predicate)