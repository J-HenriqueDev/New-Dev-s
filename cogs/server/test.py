import discord
from discord.ext import commands
from pymongo import MongoClient
import pymongo

url = "Tem coisa a haver com isso"

class logs():
  def __init__(self,client):
    self.client = client

    async def on_message_delete(self, message):
       try:
         if message.author.bot == False:
           mongo = MongoClient(url)
           seila = mongo["seila"]
           logs = seila["logs"]
           logs = seila.logs.find_one({"_id":str(message.guild.id)})
           if not logs is None:            
              embed=discord.Embed(title="👮| Messagem Apagada|👮", description="Nossos Guardas descobriram uma messagem apagada", color=0xff0000)
              embed.add_field(name="Usuario", value=str(message.author.mention), inline=False)
              embed.add_field(name="Menssagem", value=str(message.content[:700]), inline=False)
              embed.add_field(name="Canal", value=str(message.channel.mention), inline=False)
              embed.set_footer(text="@Sei La Todos os direitos reservados")
              canal = discord.utils.get(message.guild.channels, id=int(logs["canal-logs"]))
              await canal.send(embed=embed)
       except:
           pass

    async def on_message_edit(self, before, afther):
      try:
        if before.author.bot == False:
           mongo = MongoClient(url)
           seila = mongo("seila")
           logs = seila["logs"]
           logs = seila.logs.find_one({"_id":str(ctx.guild.id)})
           if not logs is None:
             embed=discord.Embed(title="👮| Messagem Editada|👮", description="Nossos Guardas descobriram uma messagem Editada", color=0xff0000)
             embed.set_thumbnail(url="asfydhdjsifsufiodufhsjjjod0587759rhdd.gg.discord.bvfd.com")
             embed.add_field(name="Usuario", value=str(before.author)+" ("+str(before.author.mention)+")", inline=False)
             embed.add_field(name="Menssagem Editada", value=str(before.content[:700]), inline=False)
             embed.add_field(name="Menssagem Agora", value=str(afther.content[:700]), inline=False)
             embed.add_field(name="Canal", value=str(before.channel.mention), inline=False)
             embed.set_footer(text="@Sei La Todos os direitos reservados")
             canal = discord.utils.get(before.guild.channels, id=int(logs["canal-logs"]))
             await canal.send(embed=embed)
      except:
        pass

   async def on_member_join(member):
      try:
        if before.author.bot == False:
          mongo = MongoClient(url)
          seila = mongo("seila")
          logs = seila["logs"]
          logs = seila.logs.find_one({"_id":str(ctx.guild.id)})
          if not logs is None:
            embed=discord.Embed(title="Ben-vindo ao servidor", description=str(ctx.guild), color=0xff0000)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name="Usuario", value=ctx.author.mention, inline=False)
            embed.add_field(name="Nossa Menssagem", value="Obrigado caro amigo por ter entrado no server", inline=False)
            embed.add_field(name="Membros no servidor", value=ctx.guild.member_count, inline=False)
            embed.set_footer(text="@Sei La Todos os direitos reservados")
            canal = discord.utils.get(member.guild.channels, id=int(logs["canal-logs"]))
            await canal.send(embed=embed)
      except:
        pass


  @commands.command()
  async def setlogs(self, ctx, *, word=None):
    if word is None:
      await ctx.send(f"OI vc precisa de por sl!setlogs + id do canal")
      return
    try:
      mongo = MongoClient(url)
      seila = mongo("seila")
      logs = seila["logs"]
      logs = seila.logs.find_one({"_id":str(ctx.guild.id)})
      if logs is None:
         canal = {"_id":str(ctx.guild.id), "canal-logs":int:(word)}
         seila.logs.insert_one(canal).inserted_id
         await ctx.send(f"Canal <#{word}> foi setado")
      else:
        seila.logs.update_one({"_id":str(ctx.author.id)}, {"$set":{"canal-logs":int(word)}})
        await ctx.send(f"Canal <#{word}> foi atualizado")
    except Exception as e:
        await ctx.send(f"[Erro 404] {e}")

def setup(client):
    print("[Comando: logs] Carragando...")
    client.add_cog(logs(client))