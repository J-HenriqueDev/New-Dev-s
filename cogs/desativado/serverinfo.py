
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

class serverinfo(commands.Cog):
    def __init__(self, bard):
        self.bard = bard


    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=['server'])
    async def serverinfo(self, ctx):
           if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
               await ctx.message.add_reaction(":incorreto:571040727643979782")
               return

           servidor = ctx.message.guild
           if ctx.message.guild.icon_url_as() == "":
              img = "https://i.imgur.com/To9mDVT.png"
           else:
             img  = ctx.guild.icon_url
           online = len([y.id for y in servidor.members if y.status == discord.Status.online])
           afk  = len([y.id for y in servidor.members if y.status == y.status == discord.Status.idle])
           offline = len([y.id for y in servidor.members if y.status == y.status == discord.Status.offline])
           dnd = len([y.id for y in servidor.members if y.status == y.status == discord.Status.dnd])
           geral = len([y.id for y in servidor.members])
           bots= len([y.id for y in servidor.members if y.bot])
           criado_em = str(servidor.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
           usuarios = "<:online:510815469121437697> : ``"+str(online)+"`` <:idle:510815469192740865> : ``"+str(afk)+"`` <:dnd:510815469339410435> : ``"+str(dnd)+"`` <:offline:510815469339541515> : ``"+str(offline)+"`` <:robo:510469604234100748> : ``"+str(bots)+"``"
           texto = "<:batepapo:519463996017868801> : ``"+str(len(servidor.text_channels))+"``<:voz:519463730698780674>  : ``"+str(len(servidor.voice_channels))+"``"
           cargos = len([y.id for y in servidor.roles])
           emojis = len([y.id for y in servidor.emojis])
           embed = discord.Embed(title="Olá {}, este e o perfil do servidor {} e nele contém algumas informações.".format(ctx.message.author.name, servidor.name),colour=0x7BCDE8)
           embed.set_author(name="INFORMAÇÂO SERVIDOR", icon_url=ctx.author.avatar_url_as())
           embed.add_field(name="<:estrela:519465388669403136> Dono", value = "``"+str(servidor.owner)+"``", inline=True)
           embed.add_field(name="<:letra_a:519461766623920152> Nome", value = "``"+str(servidor.name)+"``", inline=True)
           embed.add_field(name="<:numeros:518885155407003698> Id", value = "``"+str(servidor.id)+"``", inline=True)
           embed.add_field(name="<:calendario:519462364165177365> Criado em", value = "``"+str(criado_em)+"``", inline=True)
           embed.add_field(name="<:rank:519462717141286923> Cargos", value = "``"+str(cargos)+"``", inline=True)
           embed.add_field(name="<:emoji:519462971530018819> Emojis", value = "``"+str(emojis)+"``", inline=True)
           embed.add_field(name="<:ordem:519463328079151104> Canais", value = texto, inline=True)
           embed.add_field(name="<:local:519464624299573274> Localização", value = "``"+str(servidor.region).title()+"``", inline=True)
           embed.add_field(name="<:cadeado:519465029079400449> Verificação", value = "``"+str(servidor.verification_level).replace("none","Nenhuma").replace("low","Baixa").replace("medium","Media").replace("high","Alta").replace("extreme","Muito alta")+"``", inline=True)
           embed.add_field(name="<:usuario:519194953042100262> Usuários ["+str(geral)+"]", value = usuarios, inline=True)
           embed.set_thumbnail(url=img)
           embed.set_footer(text=self.bard.user.name+" © 2018", icon_url=self.bard.user.avatar_url_as())
           await ctx.send(embed = embed)
def setup(bard):
    print("[Discord] : Cmd (serverinfo) ")
    bard.add_cog(serverinfo(bard))

