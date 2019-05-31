import discord
import asyncio
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


class eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.staff = bot.db.staff
        self.bots = bot.db.bots

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
          comma = error.args[0].split('"')[1]
          embed = discord.Embed(title=f"{self.bot._emojis['incorreto']} | Comando não encontrado", color=0x7289DA, description=f"O comando `{comma}` não existe.")
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
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f"<:incorreto:571040727643979782> | **{ctx.author.name}**, o comando **`{ctx.invoked_with}`** está temporariamente desativado.")
        

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.author.id in self.bot.staff and ctx.command.is_on_cooldown(ctx):
            ctx.command.reset_cooldown(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
      if re.search(r'discord(?:app\\?[\s\S]com\\?\/invite|\\?[\s\S]gg|\\?[\s\S]me)\/', message.content) or re.search(r'invite\\?[\s\S]gg\\?\/[\s\S]', message.content):
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
            aviso1.remove(message.author.id)     
            aviso2.remove(message.author.id)       
            print('ban')
            await message.author.ban(reason="Divulgando.")
          
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
      if len(await guild.invites()) > 0:
                    for x in await guild.invites():
                        if x.max_age == 0:
                            invite = x.url
      else:
          for c in guild.channels:
            inv = await discord.abc.GuildChannel.create_invite(c)
            invite = inv.url
      canal = self.bot.get_user(558396463873392640)
      embed = discord.Embed(color=0x36393F)
      embed.add_field(name=f"{self.bot._emojis['nome']} NOME",value=guild.name)
      embed.add_field(name=f'{self.bot._emojis["ip"]} ID',value=guild.id)
      embed.add_field(name=f'{self.bot._emojis["dono"]} DONO',value=f'{guild.owner}\n({guild.owner_id})')
      embed.add_field(name=f'{self.bot._emojis["tipo"]} INVITE',value=invite)
      await canal.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
      if len(await guild.invites()) > 0:
                    for x in await guild.invites():
                        if x.max_age == 0:
                            invite = x.url
      else:
          for c in guild.channels:
            inv = await discord.abc.GuildChannel.create_invite(c)
            invite = inv.url
      canal = self.bot.get_user(558396463873392640)
      embed = discord.Embed(color=0x36393F)
      embed.add_field(name=f"{self.bot._emojis['nome']} NOME",value=guild.name)
      embed.add_field(name=f'{self.bot._emojis["ip"]} ID',value=guild.id)
      embed.add_field(name=f'{self.bot._emojis["dono"]} DONO',value=f'{guild.owner}\n({guild.owner_id})')
      embed.add_field(name=f'{self.bot._emojis["tipo"]} INVITE',value=invite)
      await canal.send(guild.id)
      await canal.send(embed=embed)
    
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
          else:
              print("[moderador] : updatado")
              db.update_one({'_id': str(after.id)}, {'$set': {'estagiario': True}})

        elif moderador in after.roles and moderador not in before.roles: 
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[moderador] : inserido")
            serv ={"_id": str(after.id),"nome": str(after.name),"id": str(after.id),"moderador": True}
            db.insert_one(serv) #new
          else:
              print("[moderador] : updatado")
              db.update_one({'_id': str(after.id)}, {'$set': {'moderador': True}})

        elif administrador in after.roles and administrador not in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[administrador] : inserido")
            serv ={"_id": str(after.id),"nome": str(after.name),"id": str(after.id),"administrador": True}
            db.insert_one(serv) #new
          else:
              print("[administrador] : updatado")
              db.update_one({'_id': str(after.id)}, {'$set': {'administrador': True}})

        elif Founder in after.roles and Founder not in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[Founder] : inserido")
            serv ={"_id": str(after.id),"nome": str(after),"id": str(after.id),"Founder": True}
            db.insert_one(serv) #new
          else:
              print("[Founder] : updatado")
              db.update_one({'_id': str(after.id)}, {'$set': {'Founder': True}})
        

            
        elif estagiario not in after.roles and estagiario in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[estagiario] : inserido demote")
            serv ={"_id": str(after.id),"nome": str(after),"id": str(after.id),"estagiario": False}
            db.insert_one(serv) #new
           
          else:
              print("[estagiario] : updatado demote ")
              db.update_one({'_id': str(after.id)}, {'$set': {'estagiario': False}})
              
        elif moderador not in after.roles and moderador in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[moderador] : inserido demote")
            serv ={"_id": str(after.id),"nome": str(after),"id": str(after.id),"moderador": False}
            db.insert_one(serv) #new
           
          else:
              print("[moderador] : updatado demote ")
              db.update_one({'_id': str(after.id)}, {'$set': {'moderador': False}})

        elif administrador not in after.roles and administrador in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[administrador] : inserido demote")
            serv ={"_id": str(after.id),"nome": str(after),"id": str(after.id),"administrador": False}
            db.insert_one(serv)
          else:
              print("[administrador] : updatado demote")
              db.update_one({'_id': str(after.id)}, {'$set': {'administrador': False}})
          

        elif Founder not in after.roles and Founder in before.roles:
          users = db.find_one({"_id": str(after.id)})
          if not users:
            print("[Founder] : inserido demote")
            serv ={"_id": str(after.id),"nome": str(after),"id": str(after.id),"Founder": False}
            db.insert_one(serv) #new
            
          else:
              print("[Founder] : updatado demote ")
              db.update_one({'_id': str(after.id)}, {'$set': {'Founder': False}})

        

    @commands.Cog.listener()  
    async def on_member_remove(self, member):
       if member.guild.id == 570906068277002271:
        await asyncio.sleep(50)
        mongo = MongoClient(self.bot.database)
        bard = mongo['bard']
        users = bard['users']
        print(f'membro id = {member.id}')
        user = self.bot.get_user(member.id)
        usuario = bard.users.find_one({'_id': str(member.id)})
        if usuario:
            bard.users.delete_one({'_id': str(member.id)})
            print(f'o membro {user}({member.id}) que estava no TOPHELPER foi removido.') 

    @commands.Cog.listener()
    async def on_member_join(self, member):
      mongo = MongoClient(self.bot.database)
      bard = mongo['bard']
      users = bard['users']
      bot = bard.users.find_one({"_id": str(member.id)})
      print(bot["linguagem"])
      if bot is None:
        pass
      elif bot["linguagem"] == "python":
          cargo = discord.utils.get(member.guild.roles, name="</NewHelper Python>")
          cargo1 = discord.utils.get(member.guild.roles, name="</NewHelper>")
          await member.add_roles(cargo)
          await member.add_roles(cargo1)
          print('funcionou')
      elif bot["linguagem"] == "javascript":
          cargo = discord.utils.get(member.guild.roles, name="</NewHelper Javascript>")
          cargo1 = discord.utils.get(member.guild.roles, name="</NewHelper>")
          await member.add_roles(cargo)
          await member.add_roles(cargo1)
          print('funcionou')
      

def setup(bot):
  bot.add_cog(eventos(bot))
