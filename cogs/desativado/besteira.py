import discord
from discord.ext import commands
import requests


class cu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def cmd(self, ctx):
        config_embed = discord.Embed(color=self.bot.cor, description="asas")
            
        await ctx.send(embed=config_embed)
    
    @cmd.error
    async def cmd_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
          comma = error.args[0].split('"')[1]
          embed = discord.Embed(title=f"{self.bot._emojis['incorreto']} | LANG INVALIDA", color=0x7289DA, description=f"A linguagem `{comma}` não está cadastrada em minha database.")
          await ctx.send(embed=embed)
          return

    @cmd.command(
        name='py',
        aliases=['python','discord.py'],
        description='Visualiza o código de um comando em Python publicado por um membro',
        usage='c.comandopy <Nome do Comando>'
    )
    async def _comandopy(self, ctx, *, nome):
        cmd = self.bot.db.cmds.find_one({"linguagem": "python", "nome": nome.lower(), "pendente": False})
        if cmd is None:
            return await ctx.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, não foi possível encontrar um comando em `Python` com o nome ``{nome}``.")
        

        try:
            autor = await self.bot.fetch_user(int(cmd['autor']))
        except:
            autor = "Não encontrado"

        data = cmd['data'].strftime("%d/%m/20%y - %H:%M:%S")

        em = discord.Embed(
            colour=self.bot.cor,
            description=f"\n**NOME DO COMANDO:** ``{nome.lower()}``\n**AUTOR:** `{autor}`\n**DATA DE ENVIO:** `{data}`\n```py\n{cmd['code']}```")
        #em.set_footer(
            #text=f"👍 {cmd['vPositivos']} votos e {cmd['vNegativos']} votos Negativos",)
        #em.set_thumbnail(url="https://imgur.com/LD60DLf.png")
        em.set_footer(
            text=self.bot.user.name+" © 2019",
            icon_url=self.bot.user.avatar_url_as()
        )

        await ctx.send(embed=em)
        

    @cmd.command(
        name='js',
        aliases=['javascript','discord.js'],
        description='Visualiza o código de um comando em JavaScript publicado por um membro',
        usage='c.comandojs <Nome do Comando>'
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _comandojs(self, ctx, *, nome = None):
        if nome is None:
            return await ctx.send("Digite um comando.")
        cmd = self.bot.db.cmds.find_one({"linguagem": "javascript", "nome": nome.lower(), "pendente": False})
        if cmd is None:
            return await ctx.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, não foi possível encontrar um comando em `JavaScript` com o nome enviado.")

        try:
            autor = await self.bot.fetch_user(int(cmd['autor']))
        except:
            autor = "Não encontrado"

        data = cmd['data'].strftime("%d/%m/20%y - %H:%M:%S")

        em = discord.Embed(
            colour=self.bot.cor,
            description=f"\n**NOME DO COMANDO:** ``{nome.lower()}``\n**AUTOR:** `{autor}`\n**DATA DE ENVIO:** `{data}`\n```js\n{cmd['code']}```")
        em.set_footer(
            text=self.bot.user.name+" © 2019",
            icon_url=self.bot.user.avatar_url_as()
        )

        await ctx.send(embed=em)

    
    

def setup(bot):
    bot.add_cog(cu(bot))