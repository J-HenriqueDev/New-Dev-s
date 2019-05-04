
import discord
from discord.ext import commands
import random
import time
import asyncio
from pymongo import MongoClient
import pymongo
import json
import config.database
import config.db

class userinfo(commands.Cog):
    def __init__(self, bard):
        self.bard = bard
    


    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=['user'])
    async def userinfo(self, ctx, *, user: discord.Member = None):
           if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
               await ctx.message.add_reaction(":incorreto:518624535742906371")
               return

           if user is None:
               usuario = ctx.author
               titulo = f"Olá {usuario.name}, este e seu perfil é nele contém alguma informações."
           else:
              usuario = user
              titulo = f"Olá {ctx.author.name}, , este e o perfil do {usuario.name} e nele contém alguma informações."

           if usuario.display_name == usuario.name:
               apelido = "Não definido"
           else:
              apelido = usuario.display_name
           if usuario.avatar_url_as()  == "":
              img = "https://i.imgur.com/To9mDVT.png"
           else:
             img = usuario.avatar_url_as()
           try:
             jogo = ctx.author.activity.name
           except:
               jogo = "Nada"
           if usuario.id in [y.id for y in ctx.message.guild.members if not y.bot]:
              bot = "Não"
           else:
             bot = "Sim"
           entrou_servidor = str(usuario.joined_at.strftime("%H:%M:%S - %d/%m/20%y"))
           conta_criada = str(usuario.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
           cargos = len([r.name for r in usuario.roles if r.name != "@everyone"])
           stat = str(usuario.status).replace("online","Disponível").replace("offline","Indisponível").replace("dnd","Não Pertubar").replace("idle","Ausente")
           cargos2 = len([y.id for y in ctx.message.guild.roles])
           embed = discord.Embed(title=titulo,colour=0x7BCDE8)
           embed.set_author(name="Informação perfil", icon_url=ctx.author.avatar_url_as())
           embed.add_field(name="<:hastag:518647415490871297> Tag", value = "``"+str(usuario.name)+"#"+str(usuario.discriminator)+"``", inline=True)
           embed.add_field(name="<:numeros:518885155407003698> Id", value = "``"+str(usuario.id)+"``", inline=True)
           embed.add_field(name="<:letra_a:519461766623920152> Apelido", value = "``"+str(apelido)+"``", inline=True)
           embed.add_field(name="<:calendario:519462364165177365> Conta (criada)", value = "``"+str(conta_criada)+"``", inline=True)
           embed.add_field(name="<:calendario_1:520291574970843194> Entrou (servidor)", value = "``"+str(entrou_servidor)+"``", inline=True)
           embed.add_field(name="<:convite:519288102775291904> Maior cargo", value = "``"+str(usuario.top_role)+" - ("+str(usuario.top_role.color)+")``", inline=True)
           embed.add_field(name="<:seta:520292614956908554> Cargos", value = "``"+str(cargos)+"/"+str(cargos2)+"``", inline=True)
           embed.add_field(name="<:bot:518620111448309770> Bot", value = "``"+str(bot)+"``", inline=True)
           embed.add_field(name="<:status:520293356975423498> Status", value = "``"+str(stat)+"``", inline=True)
           embed.add_field(name="<:controle:520295781249318927> Jogando", value = "``"+str(jogo)+"``", inline=True)
           mongo = MongoClient(config.database.database)
           bard = mongo['bard']
           users = bard['users']
           users = bard.users.find_one({"_id": str(usuario.id)})
           if not users is None:
              embed.add_field(name="<:estrela:519465388669403136> Reputação", value =  "``"+str(users["reputação"])+"``", inline=True)


           embed.set_thumbnail(url=img)
           embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
           await ctx.send(embed = embed)

def setup(bard):
    print("[Discord] : Cmd (userinfo) ")
    bard.add_cog(userinfo(bard))