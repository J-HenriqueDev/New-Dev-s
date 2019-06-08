from datetime import datetime
from utils.role import emojis
import discord
from config import secrets
import time
import os
import pytz
from discord.ext import commands
import asyncio
from pymongo import MongoClient




class main(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=secrets.PREFIXO,
                         case_insensitive=True,
                         pm_help=None,
                         description="New Dev's bot")
        self.remove_command('help')
        self.staff = secrets.STAFF
        self.dono = secrets.DONO
        self.cor = 0x7289DA
        self.database = secrets.DATAB
        self.canais = ["570908357032935425","571014988622331905"]
        self.token = 'blz,talvez outro dia.'
        self._emojis = emojis
        self.carregados = 1
        self.falhas = 0
        print("( * ) | Tentando se conectar ao banco de dados...")
        try:
            mongo = MongoClient(self.database)
        except Exception as e:
            print(f"\n<---------------->\n( ! ) | Erro na tentativa de conexão com o banco de dados!\n<----------->\n{e}\n<---------------->\n")
            exit()
    
        self.db = mongo['bard']
        print(f"( > ) | Conectado ao banco de dados!")
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
    
        log_ready = self.get_channel(568040355933716500)
        await log_ready.send(f"**{self.user.name}** online | `{self.carregados}` Modulos Funcionando corretamente e `{self.falhas}` falhas detectadas.")
        print(f"[OK] - {self.user.name} ({self.user.id}) - (Status - Online)")
        print(f"{len(bot.cogs)} Modulos Ativos.")
        
    async def on_message(self, message):
        canal = [570908350481432587]
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

        #if message.content.lower().startswith(f"<@!{self.user.id}>") or message.content.lower().startswith(f"<@{self.user.id}>") :
           
            #await message.channel.send(f"<:329325674827612162:556216891484536833> **|** {message.author.mention} **Digite `c.help` para ver meus comandos.**",delete_after=60)

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

