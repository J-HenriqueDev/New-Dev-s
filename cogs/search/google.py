
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
import re
import urllib
import urllib.request
from urllib.parse import quote, unquote

def imagem(args):
    try:
      nargs = args
      args = quote(args)
      args = args.replace(" ", "+")
      headers = {}
      headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
      requesting = urllib.request.Request("https://www.google.com/search?q="+args+"&source=lmns&tbm=isch&sa=X&ved=0ahUKEwi1i9f-w4fYAhXMh7QKHR69CD8Q_AUICygC&biw=1280&bih=614", headers = headers)
      opened = urllib.request.urlopen(requesting).read().decode("utf-8")
      find = re.findall('<div class="rg_meta notranslate">(.*?)</div>', opened)
      get = 0
      got = []
      final = []
      img = [".png", ".jpg", ".gif"]
      for x in find:
        try:
          found = json.loads(x)
          if found["ou"].endswith(tuple(img)):
            got.append(found["ou"])
          else:
            pass
        except:
          pass
      for x in range(1):
        pick = random.choice(got)
        get += 1
        final.append("%s" % (pick))
      return " ".join(final)
    except Exception as error:
      print(error)
      return "tive um erro."

def search(args):
    try:
      nargs = args
      args = quote(args)
      args = args.replace(" ", "+")
      headers = {}
      headers["User-Agent"] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
      requesting = urllib.request.Request("https://www.google.com/search?q="+args, headers = headers)
      opened = urllib.request.urlopen(requesting).read().decode("utf-8")
      titles = re.findall('<h3 class="LC20lb">(.*?)</h3>', opened)
      links = re.findall('<cite class="iUh30">(.*?)</cite>', opened)
      got = []
      final = []
      amount = 0
      for x in range(3):
        z = random.randint(0, 4)
        if links[z].startswith("http"):
          got.append(titles[z]+": "+links[z])
        else:
          got.append(titles[z]+": http://"+links[z])
      for x in got:
        amount += 1
        final.append("(%s). %s" % (amount, x))
      return "Resultados de %s:\n\n%s" % (nargs.title(), "\n".join(final))
    except Exception as error:
      print(error)
      return "tive um erro."
class google():
    def __init__(self, bard):
        self.bard = bard


    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def img(self,ctx, *, word=None):
        if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:518624535742906371")
           return

        img = imagem(word)
        embed = discord.Embed(color=0x7BCDE8)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def link(self,ctx, *, word=None):
        if not str(ctx.channel.id) in config.database.canais and not str(ctx.message.author.id) in config.database.admin:
           await ctx.message.add_reaction(":incorreto:518624535742906371")
           return

        img = search(word)
        embed = discord.Embed(description=img,color=0x7BCDE8)
        await ctx.send(embed=embed)

def setup(bard):
    print("[Bot] : Cmd (google) ")
    bard.add_cog(google(bard))
