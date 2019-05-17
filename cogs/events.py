import discord
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageColor
from io import BytesIO
import requests
import asyncio
from pymongo import MongoClient
from discord.ext import commands
aviso1 = []
aviso2 = []
aviso3 = []
regex = re.compile('discord(?:app\?[\s\S]com\?/invite|\?[\s\S]gg|\?[\s\S]me)\?/[\s\S]', re.IGNORECASE)

class eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.staff = bot.db.staff
        self.bots = bot.db.bots

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
          comma = error.args[0].split('"')[1]
          embed = discord.Embed(title=f"<:incorreto:571040727643979782> | Comando não encontrado", color=0x7289DA, description=f"O comando `{comma}` não existe.")
          await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            perms = '\n'.join([f"**`{perm.upper()}`**" for perm in error.missing_perms])
            await ctx.send(f"**{ctx.author.name}**, eu preciso das seguintes permissões para poder executar o comando **`{ctx.invoked_with}`** nesse servidor:\n\n{perms}", delete_after=30)
            print("sem perm")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            print("erro ao checar")
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            return await ctx.send(f"**{ctx.author.name}**, aguarde **`{int(s)}`** segundo(s) para poder usar o comando **`{ctx.invoked_with}`** novamente.", delete_after=45)
        elif isinstance(error, (commands.BadArgument, commands.BadUnionArgument, commands.MissingRequiredArgument)):
            uso = ctx.command.usage if ctx.command.usage else "Não especificado."
            await ctx.send(f"**{ctx.author.name}**, você usou o comando **`{ctx.command.name}`** de forma incorreta!\nUse seguinte o modelo: **`{uso}`**", delete_after=45)
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f"<:incorreto:571040727643979782> | **{ctx.author.name}**, o comando **`{ctx.invoked_with}`** está temporariamente desativado.")
        
        else:
            print(error)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.author.id in self.bot.staff and ctx.command.is_on_cooldown(ctx):
            ctx.command.reset_cooldown(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
          return
        if "discord.gg" in message.content.lower() or "discordapp.com/invite" in message.content.lower() or "invite.gg" in message.content.lower() or "mybotlist"in message.content.lower():
        #if regex.search(ctx.message.content) in message.content.lower():
         if str("</Link>") in [r.name for r in message.author.roles if r.name != "@everyone"]:
           print("OK")
         else:
           if not message.author.id in aviso1:
             aviso1.append(message.author.id)
             await message.delete()
             embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá {message.author.mention}, não é permitido **CONVITES** de outros servidores sem a permissão dos **Adminstradores** segundo as regras.\nTendo isso em mente irei avisa-lo esse é seu **1° Strike**.\nNo **3° Strike** você será banido.", color=0x7289DA)
             msg = await message.channel.send(embed=embed)
             await asyncio.sleep(10)
             await msg.delete()
           elif not message.author.id in aviso2:
             aviso2.append(message.author.id)
             await message.delete()
             embed=discord.Embed(description=f"<:incorreto:571040727643979782> **|** Olá {message.author.mention}, não é permitido **CONVITES** de outros servidores sem a permissão dos **Adminstradores** segundo as regras.\nTendo isso em mente irei avisa-lo esse é seu **2° Strike**.\nNo **3° Strike** você será banido.", color=0x7289DA)
             msg = await message.channel.send(embed=embed)
             await asyncio.sleep(10)
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

    @commands.Cog.listener()
    async def on_user_update(self,before,after):
      if before.avatar_url != after.avatar_url:
        url = requests.get(before.avatar_url_as(format="png"))
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.convert('RGBA')
        avatar = avatar.resize((245, 245),Image.NEAREST);
        avatar.save('cogs/img/before.png')
        
        aurl = requests.get(after.avatar_url_as(format="png"))
        after = Image.open(BytesIO(aurl.content))
        after = after.convert('RGBA')
        after = after.resize((245, 245),Image.NEAREST);
        after.save('cogs/img/after.png')

        fundo = Image.open('cogs/img/update.png')
        fonte = ImageFont.truetype('cogs/img/arial.ttf',42)

        escrever = ImageDraw.Draw(fundo)
        escrever.text(xy=(400, 135), text=f'{before.name}#{before.discriminator}', fill=(245, 255, 250), font=fonte)
        

        fundo.paste(avatar, (45, 100), avatar)
        fundo.paste(after, (950, 100), after)
        fundo.save('cogs/img/updates.png')
        canal = self.bot.get_channel(571016071209811972)
        if canal is None:
            return
        else:
            await canal.send(file=discord.File('cogs/img/updates.png'))
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
      db = self.staff
      canal = self.bot.get_channel(570908359864352768)
      user = db.find_one({"_id": after.id})
      if after.roles != before.roles and after.guild.id == 570906068277002271:
        Founder = after.guild.get_role(570908340184416285)
        administrador = after.guild.get_role(570908340742520832)
        moderador = after.guild.get_role(570908341287518208)
        estagiario = after.guild.get_role(571030324872740864)

        if estagiario in after.roles and estagiario not in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[estagiario] : inserido")
            serv ={"_id": str(after.id),"nome": str(after.name),"id": str(after.id),"estagiario": True}
            db.insert_one(serv) #new
            await canal.send(f'{after.mention} novo estágiario,inserindo ele na database.')
          else:
              print("[moderador] : updatado")
              db.update_one({'_id': str(after.id)}, {'$set': {'estagiario': True}})
              await canal.send(f'{after.mention} novo estágiario,atualizando ele na database.')

        elif moderador in after.roles and moderador not in before.roles: 
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[moderador] : inserido")
            serv ={"_id": str(after.id),"nome": str(after.name),"id": str(after.id),"moderador": True}
            db.insert_one(serv) #new
            await canal.send(f'{after.mention} novo moderador,inserindo ele na database.')
          else:
              print("[moderador] : updatado")
              db.update_one({'_id': str(after.id)}, {'$set': {'moderador': True}})
              await canal.send(f'{after.mention} novo moderador,atualizando ele na database.')

        elif administrador in after.roles and administrador not in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[administrador] : inserido")
            serv ={"_id": str(after.id),"nome": str(after.name),"id": str(after.id),"administrador": True}
            db.insert_one(serv) #new
            await canal.send(f'{after.mention} novo administrador,inserindo ele na database.')
          else:
              print("[administrador] : updatado")
              db.update_one({'_id': str(after.id)}, {'$set': {'administrador': True}})
              await canal.send(f'{after.mention} novo administrador,atualizando ele na database.')

        elif Founder in after.roles and Founder not in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[Founder] : inserido")
            serv ={"_id": str(after.id),"nome": str(after),"id": str(after.id),"Founder": True}
            db.insert_one(serv) #new
            await canal.send(f'{after.mention} novo founder,inserindo ele na database.')
          else:
              print("[Founder] : updatado")
              db.update_one({'_id': str(after.id)}, {'$set': {'Founder': True}})
              await canal.send(f'{after.mention} novo founder,atualizando ele na database.')

            
        elif estagiario not in after.roles and estagiario in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[estagiario] : inserido demote")
            serv ={"_id": str(after.id),"nome": str(after),"id": str(after.id),"estagiario": False}
            db.insert_one(serv) #new
            await canal.send(f'o estagiario {after.mention} foi demotado,removendo ele da db')
          else:
              print("[estagiario] : updatado demote ")
              db.update_one({'_id': str(after.id)}, {'$set': {'estagiario': False}})
              await canal.send(f'o estagiario{after.mention} foi demotado,removendo ele da db')

        elif moderador not in after.roles and moderador in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[moderador] : inserido demote")
            serv ={"_id": str(after.id),"nome": str(after),"id": str(after.id),"moderador": False}
            db.insert_one(serv) #new
            await canal.send(f'o mod {after.mention} foi demotado,removendo ele da db')
          else:
              print("[moderador] : updatado demote ")
              db.update_one({'_id': str(after.id)}, {'$set': {'moderador': False}})
              await canal.send(f'o mod {after.mention} foi demotado,removendo ele da db')

        elif administrador not in after.roles and administrador in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[administrador] : inserido demote")
            serv ={"_id": str(after.id),"nome": str(after),"id": str(after.id),"administrador": False}
            db.insert_one(serv)
            await canal.send(f'o adm {after.mention} foi demotado,removendo ele da db')#new
          else:
              print("[administrador] : updatado demote")
              db.update_one({'_id': str(after.id)}, {'$set': {'administrador': False}})
              await canal.send(f'o adm {after.mention} foi demotado,removendo ele da db')

        elif Founder not in after.roles and Founder in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[Founder] : inserido demote")
            serv ={"_id": str(after.id),"nome": str(after),"id": str(after.id),"Founder": False}
            db.insert_one(serv) #new
            await canal.send(f'o founder {after.mention} foi demotado,removendo ele da db')
          else:
              print("[Founder] : updatado demote ")
              db.update_one({'_id': str(after.id)}, {'$set': {'Founder': False}})
              await canal.send(f' o founder {after.mention} foi demotado,removendo ele da db')

        

     
def setup(bot):
  bot.add_cog(eventos(bot))
