

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


class web():
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    async def id(self, ctx, *, texto):
       mongo = MongoClient(config.database.database)
       bard = mongo['bard']
       users = bard['users']
       serv ={"_id": str(texto),"nome": "Não definido","id": str(texto),"foi_mute":"Não","vezes_mute":"0","foi_devhelper":"Não","vezes_reportado":"0","reputação":"0","level":"0","exp":"0","aceito_por":"499321522578522112","historico":"Sem punições","bots":["SD"]}
       bard.users.insert_one(serv).inserted_id
       print("OK")


def setup(client):
    print("[Server] : Cmd (web) ")
    client.add_cog(web(client))
