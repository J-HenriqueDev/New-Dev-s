import discord
from discord.ext import commands

class errors(commands.Cog):
    def __init__(self, bard):
        self.bard = bard

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass

        elif isinstance(error, commands.BotMissingPermissions):
            perms = '\n'.join([f"**`{perm.upper()}`**" for perm in error.missing_perms])
            await ctx.send(f"**{ctx.author.name}**, eu preciso das seguintes permissões para poder executar o comando **`{ctx.invoked_with}`** nesse servidor:\n\n{perms}", delete_after=30)
            print("sem perm")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            print("erro ao checar")
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            print(f"cooldown em ({ctx.command})")
        elif isinstance(error, (commands.BadArgument, commands.BadUnionArgument, commands.MissingRequiredArgument)):
            uso = ctx.command.usage if ctx.command.usage else "Não especificado."
            await ctx.send(f"**{ctx.author.name}**,parece que você usou o comando **`{ctx.command.name}`** de forma errada!\nUso correto: **`{uso}`**", delete_after=45)
        else:
            print(error)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.author.id in config.database.admin and ctx.command.is_on_cooldown(ctx):
            ctx.command.reset_cooldown(ctx)

def setup(bard):
  bard.add_cog(errors(bard))
