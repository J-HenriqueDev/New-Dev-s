from datetime import datetime
import discord
from config import database,secrets
import time
import os
import pytz
from discord.ext import commands
import asyncio





def diff_list(li1, li2): 
    return (list(set(li1) - set(li2))) 

class main(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix='c.',
                         case_insensitive=True,
                         pm_help=None,
                         description="crypto bot")
        self.remove_command('help')
        self.staff = secrets.STAFF
        self.token = secrets.TOKEN
        self.dbl_key = secrets.DBL_TOKEN
        self.carregados = 0
        self.falhas = 0
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.load_extension(f"cogs.{name}")
                    self.carregados += 1
                    print(f'MÓDULO [{file}] CARREGADO')
                except Exception as e:
                    print(f"FALHA AO CARREGAR  [{file}] MODULO ERROR [{e}]")
                    self.falhas += 1


    async def on_ready(self):
        
        canale = self.get_channel(568233418299801615)
        log_ready = self.get_channel(568040355933716500)
        await log_ready.send(f"**{self.user.name}** online | `{self.carregados}` Modulos Funcionando corretamente e `{self.falhas}`falhas detectadas.")
        print(f"[OK] - {self.user.name} ({self.user.id}) - (Status - Online)")
        
    async def on_message(self, message):
        canal = [568035468751667239,568933678282047490,570908350481432587]
        """ Evento de message. Bloquear message de bots e messagens no dm e adicionar messagem ao mencionar o bot"""
        if message.author.bot:
            return
        if isinstance(message.channel, discord.abc.GuildChannel) is False:
            return

        if message.channel.id in canal:
            if message.author.bot:
                return
            await message.add_reaction(":correto:571040855918379008")
            await message.add_reaction(":incorreto:571040727643979782")

        if message.content.lower().startswith(f"<@!{self.user.id}>") or message.content.lower().startswith(f"<@{self.user.id}>") :
           
            await message.channel.send(f"<:329325674827612162:556216891484536833> **|** {message.author.mention} **Digite `c.help` para ver meus comandos.**",delete_after=60)

        else:
            await bot.process_commands(message)

    
    def iniciar(self):
       try:
           super().run(secrets.TOKEN,reconnect=True)
       except Exception as e:
           print(f"Erro ao logar o bot: {e}")


if __name__ == '__main__':
    bot = main()
    bot.iniciar()

