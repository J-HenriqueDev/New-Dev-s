from discord.ext import commands
from contextlib import redirect_stdout
from io import StringIO

from . import better

import traceback
import textwrap
import asyncio
import inspect
import discord
import random

import types

import json
import time
import sys

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #embed=discord.Embed(title="Ocorreu uma falha!!", description=str(type(error)), color=ctx.author.top_role.color)
        if isinstance(error, better.DeveloperError):
            return await ctx.send(f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",delete_after=15)
            #embed.description = "você precisa ser um desenvolvedor para executar este comando."
            #embed.add_field(name='Erro do desenvolvedor', value=str(error))
            #return await ctx.send(embed=embed, delete_after=5.0)


    @commands.command(aliases=["deb", "db", "run"])
    @better.is_developer()
    async def better_debug(self, ctx, *, string: str=None):
        string = string or repr('hello world')

        try: result = eval(string)
        except Exception as e:result = e
            
        if type(result) is types.CoroutineType:
            try: result = await result
            except Exception as e: result = e
        if type(result) in (map, filter, types.GeneratorType):
            result = tuple(result)

        embed = discord.Embed(title=f"{better.emojics['python']}{type(result)}".title(), color=ctx.author.top_role.color)
        
        embed.add_field(name='Resultado:', value=better.markdown(better.limit(repr(result), 500), lang='python'))
        embed.set_footer(text=better.__copyright__, icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=embed)
    
    @commands.command(aliases=['rld'])
    @better.is_developer()
    async def recarregar(self, ctx, *, cog: str=None):
        if not cog: return await ctx.send('Informe um cog válido.', delete_after=3.0)
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            return await ctx.send(f'O Cog "{cog}" foi carregado com sucesso!!', delete_after=3.0)
        except Exception as e:
            raise better.DeveloperError(f'O Cog "{cog}" não pode ser carregado. '+str(e))
        return self
    
    @commands.command()
    @better.is_developer()
    async def status(self, ctx, *, status: str=None):
        status = status or random.choice(['Radiação gama!!', 'Ondas pelo ar'])
        await self.bot.change_presence(
            activity=discord.Streaming(name=status.title()+" no NewDev's", url="https://www.twitch.tv/henrique_98"),
            status=discord.ActivityType.streaming
        )


class Dono(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx, *, cog: str = None):
        if not ctx.author.id in self.bot.dono:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
        if cog is None:
            return await ctx.send(f"{ctx.author.mention} Não foi inserido a cog para recarregar!", delete_after=15)
        await ctx.message.delete()
        if not cog in self.bot.cogs:
            cog_list = ",".join([c for c in self.bot.cogs])
            await ctx.send(f"{ctx.author.mention} **Módulo  invalido. Módulos disponiveis abaixo**\n```python\n{cog_list}\n```", delete_after=15)
            return
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            embed = discord.Embed(
                colour=0x7289DA,
                description=(f"**[Sucesso] O Modulo `{cog}` foi recarregado corretamente!**"))

            await ctx.send(embed=embed, delete_after=20)
        except Exception as e:
            embed = discord.Embed(
                colour=0x7289DA,
                description=(f"**[ERRO] O Modulo `{cog}` não foi recarregado corretamente**\n\n``{e}``"))

            await ctx.send(embed=embed, delete_after=20)
            print(f"RELOAD USADO POR : {ctx.author}")

    @commands.command()
    async def game(self, ctx, *, status: str = ''):
        if not ctx.author.id in self.bot.dono:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
        if status == '':
            await ctx.send("**Bota um status man**")
            return
        streamurl = "https://www.twitch.tv/henrique_98"
        await self.bot.change_presence(activity=discord.Streaming(name=status, url=streamurl),
                                       status=discord.ActivityType.streaming)
        await ctx.send(f" **Status alterado com sucesso.**\n`Novo Status`\n*{status}*")
        print(f"GAME USADO POR : {ctx.author}")


    @commands.guild_only()
    @commands.command()
    async def debug(self, ctx, *, args=None):
        if not ctx.author.id in self.bot.dono:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
        if args is None:
            embed = discord.Embed(description="**|** Olá {}, você não inseriu uma variável".format(ctx.author.mention),
                                  color=self.bot.cor)
            await ctx.send(embed=embed)
            return


        args = args.strip('` ')
        python = '```py\n{}\n```'
        result = None
        env = {'bot': self.bot, 'ctx': ctx}
        env.update(globals())
        try:
            result = eval(args, env)
            if inspect.isawaitable(result):
                result = await result
            embed = discord.Embed(colour=self.bot.cor)
            embed.add_field(name="Entrada", value='```py\n{}```'.format(args), inline=True)
            embed.add_field(name="Saida", value=python.format(result), inline=True)
            embed.set_footer(text=self.bot.user.name + " © 2019", icon_url=self.bot.user.avatar_url_as())
            print(f"DEGUG USADO POR : {ctx.author}")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(colour=self.bot.cor)
            embed.add_field(name="Entrada", value='```py\n{}```'.format(args), inline=True)
            embed.add_field(name="Saida", value=python.format(type(e).__name__ + ': ' + str(e)), inline=True)
            embed.set_footer(text=self.bot.user.name + " © 2019", icon_url=self.bot.user.avatar_url_as())
            await ctx.send(embed=embed)
            print(f"DEGUG USADO POR : {ctx.author}")
            return
        

    @commands.command(name="leave", hidden=True)
    async def cmd_leaveguild(self, ctx, id: int=0):
        guild = await self.bot.get_guild(id)
        print(guild)
        await ctx.send(f'sai da guild {guild}')
        await self.bot.get_guild(id).leave()


    @commands.command()
    async def reiniciar(self,ctx):
        if not ctx.author.id in self.bot.dono:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
        import os
        import sys
        await ctx.message.delete()
        embed = discord.Embed(description=f"<:correto:567782857678913547> O **{ctx.me.name}** está sendo reiniciado!", color=0x7289DA)
        await ctx.send(embed=embed)
        print(f"REINICIAR USADO POR : {ctx.author}")
        def reiniciar_code():
           python = sys.executable
           os.execl(python, python, * sys.argv)
        print('Reiniciando...')
        reiniciar_code()


    @commands.command(
        name='desativarcomando',
        aliases=['dcmd','acmd','ativarcomando'],
        description='desativa um comando do bot',
        usage='c.desativarcomando <Nome do Comando>'
    )
    async def _desativarcomando(self, ctx, *, nome=None):
        if not ctx.author.id in self.bot.dono:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
        if nome is None:
            return await ctx.send(f"{ctx.author.mention} você não inseriu um comando pra desativar.", delete_after=20)
       
        comando = self.bot.get_command(nome)
        if not comando:
            return await ctx.send(f"<:incorreto:594222819064283161> | **{ctx.author.name}**, não encontrei nenhum comando chamado **`{nome}`**.")

        if comando.enabled:
            comando.enabled = False
            await ctx.send(f"<:desligado:571038275314122754> **{ctx.author.name}**, você desativou o comando **`{comando.name}`**.")
        else:
            comando.enabled = True
            await ctx.send(f"<:ligado:571038226861522957> **{ctx.author.name}**, você ativou o comando **`{comando.name}`**.")

    @commands.command(hidden=True)
    async def exec(self, ctx, *, body: str):
        if not ctx.author.id in self.bot.dono:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
        def clean(content):
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])
            return content.strip('` \n')

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'msg': ctx.message,
        }

        env.update(globals())

        body = clean(body)
        stdout = StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "    ")}' # 4 espaços = tab, se quiser tab mesmo coloque \t dentro do ""

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()

        except:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        
        else:
            value = stdout.getvalue()
            try:
                emoji = await self.bot.get_emoji(571375157763899412)
                await ctx.message.add_reaction(emoji)
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                await ctx.send(f'```py\n{value}{ret}\n```')
def setup(bot):
    bot.add_cog(Dono(bot))
    bot.add_cog(Owner(bot))
