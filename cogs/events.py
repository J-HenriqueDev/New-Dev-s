import discord
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests
import asyncio
import config.database
from discord.ext import commands
aviso1 = []
aviso2 = []
aviso3 = []
regex = re.compile('discord(?:app\?[\s\S]com\?/invite|\?[\s\S]gg|\?[\s\S]me)\?/[\s\S]', re.IGNORECASE)

class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        if regex.search(message.content) is not None:
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
      if before.avatar != after.avatar:
          url = requests.get(before.avatar_url_as(format="png"))
          after = requests.get(after.avatar_url_as(format="png"))
          avatar = Image.open(BytesIO(url.content))
          avtrafter = Image.open(BytesIO(after.content))
          avatar = avatar.resize((183, 183));
          avtrafter = avtrafter.resize((183, 183));
          bigsize = (avatar.size[0] * 3, avatar.size[1] * 3)
          afterbigsize = (avtrafter.size[0] * 3, after.size[1] * 3)
          mask = Image.new('L', bigsize, 0)
          draw = ImageDraw.Draw(mask)
          draw.ellipse((0, 0) + bigsize, fill=255)
          aftermask = Image.new('L', afterbigsize, 0)
          afterdrawe = ImageDraw.Draw(aftermask)
          afterdrawe.ellipse((0, 0) + afterbigsize, fill=255)
          mask = mask.resize(avatar.size, Image.ANTIALIAS)
          avatar.putalpha(mask)
          afteraftermask = mask.resize(after.size, Image.ANTIALIAS)
          after.putalpha(afteraftermask)

          output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
          output.putalpha(mask)
          outpute = ImageOps.fit(after, aftermask.size, centering=(0.5, 0.5))
          output.putalpha(aftermask)
          fundo = Image.open('cogs/img/update.png')
          fonte = ImageFont.truetype('cogs/img/arial.ttf', 35)
          escrever = ImageDraw.Draw(fundo)
          escrever.text(xy=(365, 135), text=f'{before.name}', fill=(245, 255, 250), font=fonte)
          escrever.text(xy=(398, 215), text=f'#{before.discriminator}', fill=(245, 255, 250), font=fonte)
          fundo.paste(avatar, (45, 113), avatar)
          fundo.paste(after, (45, 113), avatar)
          fundo.save('updates.png')
          canal = self.bot.get_channel(571016071209811972)
          if canal is None:
              return
          else:
              await canal.send(file=discord.File('updates.png'))
     
def setup(bot):
  bot.add_cog(errors(bot))
