
import discord
from discord.ext import commands
import random
import asyncio
import config.database

bard = commands.Bot(command_prefix="rd.")
shared = discord.AutoShardedClient(shard_count=config.database.shard_count, shard_ids=config.database.shard_ids)
bard.remove_command('help')


@bard.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bard.user.name))
    print("ID: {}".format(bard.user.id))
    await bard.change_presence(activity = discord.Game(name="Exclusivo New Dev's"))
    while True:
       await onlinestuff()



async def onlinestuff():
     global server, channnel1, person, message1, roles, message2, superseasnail, alerts
     person = bard.get_user(499321522578522112)
     server = bard.get_guild(498011182620475412)

     channel = discord.utils.get(server.channels, id=523490486401499157)
     py_role = discord.utils.get(server.roles, name="</Python-Discord.py>")
     py_emoji = discord.utils.get(server.emojis, name="python")     
     #js
     js_role = discord.utils.get(server.roles, name="</Javascript-Discord.js>")
     js_emoji = discord.utils.get(server.emojis, name="js")   
     #js
     jv_role = discord.utils.get(server.roles, name="</Java-Discord.jda>")
     jv_emoji = discord.utils.get(server.emojis, name="java")
     #kt
     kt_role = discord.utils.get(server.roles, name="</Kotlin-Discord.kt>")
     kt_emoji = discord.utils.get(server.emojis, name="kt")
     #go
     go_role = discord.utils.get(server.roles, name="</Golang-Discord.go>")
     go_emoji = discord.utils.get(server.emojis, name="go")
     #rb
     rb_role = discord.utils.get(server.roles, name="</Ruby-Discord.rb>")
     rb_emoji = discord.utils.get(server.emojis, name="ruby")   
     #up
     up_role = discord.utils.get(server.roles, name="</Atualizações>")
     up_emoji = discord.utils.get(server.emojis, name="update")   
     #dmb
     dmb_role = discord.utils.get(server.roles, name="</DBM-Discord bot maker>")
     dmb_emoji = discord.utils.get(server.emojis, name="dmb")    
     #yt
     yt_role = discord.utils.get(server.roles, name="</Inscrito>")
     yt_emoji = discord.utils.get(server.emojis, name="youtube")    
     #dsg
     dsg_role = discord.utils.get(server.roles, name="</Designer>")
     dsg_emoji = discord.utils.get(server.emojis, name="designer")   
     #esp
     esp_role = discord.utils.get(server.roles, name="</Espectador>")
     esp_emoji = discord.utils.get(server.emojis, name="tametirando")   
     #cor
     cor_role = discord.utils.get(server.roles, name="</Cobol-Discord.cb>")
     cor_emoji = discord.utils.get(server.emojis, name="berinjela")   
     #windows
     wn_role = discord.utils.get(server.roles, name="</Windows>")
     wn_emoji = discord.utils.get(server.emojis, name="windows")   
     #linux
     ln_role = discord.utils.get(server.roles, name="</Linux>")
     ln_emoji = discord.utils.get(server.emojis, name="linux")   
     #Mac
     mc_role = discord.utils.get(server.roles, name="</MacOS>")
     mc_emoji = discord.utils.get(server.emojis, name="mac")   
     #Mac
     ht_role = discord.utils.get(server.roles, name="</HTML-CSS>")
     ht_emoji = discord.utils.get(server.emojis, name="htcs")   
     
     php_role = discord.utils.get(server.roles, name="</Php-Discord.php>")
     php_emoji = discord.utils.get(server.emojis, name="php")   

     message_1 = await channel.get_message(523511092920451098)
     roles_1 = {py_emoji:py_role, js_emoji:js_role, jv_emoji:jv_role, kt_emoji:kt_role, go_emoji:go_role}
     message_2 = await channel.get_message(523511105113423884)
     roles_2 = {rb_emoji:rb_role, cor_emoji:cor_role, php_emoji:php_role, ht_emoji:ht_role, up_emoji:up_role}
     message_3 = await channel.get_message(523511110683459594)
     roles_3 = {dmb_emoji:dmb_role, yt_emoji:yt_role, dsg_emoji:dsg_role, esp_emoji:esp_role, ln_emoji:ln_role}
     message_4 = await channel.get_message(523511114387030017)
     roles_4 = {mc_emoji:mc_role, wn_emoji:wn_role}

     await reactioncheck1(message_1, roles_1)
     await reactioncheck1(message_2, roles_2)
     await reactioncheck1(message_3, roles_3)
     await reactioncheck1(message_4, roles_4)

async def reactioncheck1(message, roles):
   try:
    channel = discord.utils.get(server.channels, id=511285296772677672)
    a = []
    for x in server.members:
        a.append([x])
    reactions = message.reactions
    for reaction in reactions:
            role = roles[reaction.emoji]
            users = await reaction.users().flatten()
            for user in users:
                    for p in a:
                        if p[0] == user:
                            p.append(role)
                    pass
            pass
    for c in a:
        for e in roles:
                if roles[e] in c:
                    if roles[e] not in c[0].roles:
                        await c[0].add_roles(roles[e])  
                else:
                    if roles[e] in c[0].roles:
                        await c[0].remove_roles(roles[e])
    pass
   except Exception as e:
      pass

if __name__ == '__main__':
 try:
   f = open('data/module.txt', 'r')
   for name in f.readlines():
     if len(name.strip())>0:
        bard.load_extension(name.strip())
     f.close()
 except Exception as e :
    print('[Erro] : {} {}'.format(name,e))


bard.run("NTAxMTc5NTMzMTk0NjkwNTgz.D1h1Ww.vHN-NUzXL5vNRekuh8kf5Sp4aLM")




