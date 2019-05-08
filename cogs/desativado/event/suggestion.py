
import discord
from discord.ext import commands
import random
import asyncio
import pytz
from datetime import datetime
from pymongo import MongoClient
import pymongo
import json
import config.database
import config.db
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
aviso1 = []
aviso2 = []
aviso3 = []
class suggestion():
    def __init__(self, bard):
        self.bard = bard
        

    async def on_message_edit(self, before, after):
       if before.author.bot == False:
        if before.content != after.content:
          embed=discord.Embed(color=0x7BCDE8)
          embed.set_author(name="Logs (Message editada)", icon_url=before.author.avatar_url)
          if len(before.attachments) >=1:
             link = before.attachments[0].url
             url = str(link).replace("https://cdn.discordapp.com/","https://media.discordapp.net/")
             embed.set_image(url=url)
          else:
            pass
          if len(before.content) >=1:
             embed.add_field(name="<:messagem:518615610721173505> Messagem (Antes)", value=f"``{before.content[:900]}``", inline=True)
             embed.add_field(name="<:messagem:518615610721173505> Messagem (Depois)", value=f"``{after.content[:900]}``", inline=True)

          else:
            pass          
          embed.add_field(name="<:usuario:519194953042100262> Usuário", value=f"``{before.author}`` - (<@{before.author.id}>)", inline=True)
          embed.add_field(name="<:batepapo:519463996017868801> Canal", value=f"``{before.channel.name}`` - (<#{before.channel.id}>)", inline=True)
          tz = pytz.timezone('America/Sao_Paulo')
          hora = datetime.now(tz)
          time = str(hora.strftime("%H:%M:%S - %d/%m/20%y"))          
          embed.add_field(name="<:tempo:518615474120949789> Horario", value=f"``{time}``", inline=True)
          canal = discord.utils.get(before.guild.channels, id=520747443906936848)
          await canal.send(embed=embed)
    
    async def on_message_delete(self, message):
       if message.author.bot == False:
          embed=discord.Embed(color=0x7BCDE8)
          embed.set_author(name="Logs (Message apagada)", icon_url=message.author.avatar_url)
          if len(message.attachments) >=1:
             link = message.attachments[0].url
             url = str(link).replace("https://cdn.discordapp.com/","https://media.discordapp.net/")
             embed.set_image(url=url)
          else:
            pass
          if len(message.content) >=1:
             embed.add_field(name="<:messagem:518615610721173505> Messagem", value=f"``{message.content[:900]}``", inline=True)
          else:
            pass          
          embed.add_field(name="<:usuario:519194953042100262> Usuário", value=f"``{message.author}`` - (<@{message.author.id}>)", inline=True)
          embed.add_field(name="<:batepapo:519463996017868801> Canal", value=f"``{message.channel.name}`` - (<#{message.channel.id}>)", inline=True)
          tz = pytz.timezone('America/Sao_Paulo')
          berlin_now = datetime.now(tz)
          time = str(berlin_now.strftime("%H:%M:%S - %d/%m/20%y"))          
          embed.add_field(name="<:tempo:518615474120949789> Horario", value=f"``{time}``", inline=True)
          canal = discord.utils.get(message.guild.channels, id=520747443906936848)
          await canal.send(embed=embed)

    async def on_member_remove(self, member):
       if member.guild.id == 498011182620475412:
        canal = discord.utils.get(member.guild.channels, id=507307468016058369)
        membros = len(member.guild.members)
        texto = "<a:link_emoji:516076366328889358> | **Membros** : "+str(membros).replace("0", "0⃣").replace("1", "1⃣").replace("2", "2⃣").replace("3", "3⃣").replace("4", "4⃣").replace("5", "5⃣").replace("6", "6⃣").replace("7", "7⃣").replace("8", "8⃣").replace("9", "9⃣")
        await canal.edit(topic=texto)
    
    async def on_member_join(self, member):
       if member.guild.id == 498011182620475412:
        url = requests.get(member.avatar_url)
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((245, 245));
        bigsize = (avatar.size[0] * 2,  avatar.size[1] * 2)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        saida = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        saida.putalpha(mask)
        saida.save('cogs/event/img/avatar.png')

        fundo = Image.open('cogs/event/img/bemvindo.png')
        fonte = ImageFont.truetype('cogs/event/img/arial.ttf',42)
        fonte2 = ImageFont.truetype('cogs/event/img/arial.ttf',58)

        escrever = ImageDraw.Draw(fundo)
        escrever.text(xy=(365,215), text=str(member.name),fill=(255,255,255),font=fonte)
        escrever.text(xy=(405,283), text=str(member.discriminator),fill=(255,255,255),font=fonte2)
        escrever.text(xy=(365,372), text="New Dev's",fill=(255,255,255),font=fonte)

        fundo.paste(avatar, (52, 133), avatar)
        fundo.save("cogs/event/img/welcome.png")   
        canal = discord.utils.get(member.guild.channels, id=521139968320602112)
        await canal.send(f"Olá {member.mention}, seja bem vindo ao **New Dev's**, caso queria algum **CARGO** use o <#523490486401499157> para pegar, e leia as <#507395636883357697> para ficar por dentro do servidor.", file=discord.File('cogs/event/img/welcome.png'))
        
        canal = discord.utils.get(member.guild.channels, id=555449220950392843)
        membros = len(member.guild.members)
        texto = "<a:link_emoji:516076366328889358> | **Membros** : "+str(membros).replace("0", "0⃣").replace("1", "1⃣").replace("2", "2⃣").replace("3", "3⃣").replace("4", "4⃣").replace("5", "5⃣").replace("6", "6⃣").replace("7", "7⃣").replace("8", "8⃣").replace("9", "9⃣")
        await canal.edit(topic=texto)
        if member.bot == True:
           mongo = MongoClient(config.database.database)
           bard = mongo['bard']
           bot = bard['bot']
           bot = bard.bot.find_one({"_id": str(member.id)})
           if bot is None:
              print(f"[Evento] Bot {member} entrou!")
           else:
             if bot["linguagem"] == "python":
                cargo = discord.utils.get(member.guild.roles, name="</Bot.py>")
                await member.add_roles(cargo)
             elif bot["linguagem"] == "javascript":
                  cargo = discord.utils.get(member.guild.roles, name="</Bot.js>")
                  await member.add_roles(cargo)
             elif bot["linguagem"] == "java":
                  cargo = discord.utils.get(member.guild.roles, name="</Bot.jda>")
                  await member.add_roles(cargo)
             elif bot["linguagem"] == "kotlin":
                  cargo = discord.utils.get(member.guild.roles, name="</Bot.kt>")
                  await member.add_roles(cargo)
             elif bot["linguagem"] == "golang":
                  cargo = discord.utils.get(member.guild.roles, name="</Bot.go>")
                  await member.add_roles(cargo)
             elif bot["linguagem"] == "ruby":
                  cargo = discord.utils.get(member.guild.roles, name="</Bot.rb>")
                  await member.add_roles(cargo)
             else:
                cargo = discord.utils.get(member.guild.roles, name="</Muted>")
                await member.add_roles(cargo)

    async def on_message(self, message):
        if message.guild is None:
          return
        if "discord.gg" in message.content.lower() or "discord.me" in message.content.lower() or "discordapp.com/invite" in message.content.lower():
         if str("</Link>") in [r.name for r in message.author.roles if r.name != "@everyone"]:
           print("OK")
         else:
           if not message.author.id in aviso1:
             aviso1.append(message.author.id)
             await message.delete()
             embed=discord.Embed(description=f"<:incorreto:518624535742906371> **|** Olá {message.author.mention}, não é permitido **CONVITES** de outros servidores sem a permissão dos **Adminstradores** segundo as regras.\nTendo isso em mente irei avisa-lo esse é seu **1° Strike**.\nNo **3° Strike** você será banido.", color=0x7BCDE8)
             msg = await message.channel.send(embed=embed)
             await asyncio.sleep(60)
             await msg.delete()
           elif not message.author.id in aviso2:
             aviso2.append(message.author.id)
             await message.delete()
             embed=discord.Embed(description=f"<:incorreto:518624535742906371> **|** Olá {message.author.mention}, não é permitido **CONVITES** de outros servidores sem a permissão dos **Adminstradores** segundo as regras.\nTendo isso em mente irei avisa-lo esse é seu **2° Strike**.\nNo **3° Strike** você será banido.", color=0x7BCDE8)
             msg = await message.channel.send(embed=embed)
             await asyncio.sleep(60)
             await msg.delete()
           else:
             await message.delete()
             await message.author.ban()

        
        if str(message.channel.id) == str(512629173668413460):
           emoji1 = discord.utils.get(message.guild.emojis, id=515519909434753041)
           emoji2 = discord.utils.get(message.guild.emojis, id=515519909330157569)
           await message.add_reaction(emoji1)
           await message.add_reaction(emoji2)
           return



def setup(bard):
    print("[Event] : Cmd (suggestion) ")
    bard.add_cog(suggestion(bard))
