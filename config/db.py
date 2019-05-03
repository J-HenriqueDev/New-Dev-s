import json
from pymongo import MongoClient
import pymongo
import config.database

def servidor(ids,name):
   mongo = MongoClient(config.database.database)
   bard = mongo['bard']
   guild = bard['guild']
   serv ={
   "_id": str(ids),
   "nome": str(name),
   "id": str(ids),
   "canal-entrada-id": 0,
   "canal-saida-id": 0,
   "canal-saida-status":"off",
   "canal-entrada-status":"off",
   "canal-entrada-mensagem": "?",
   "canal-saida-mensagem": "?",
   "canal-entrada-tipo": "0",
   "canal-moderacao-id": 0,
   "canal-moderacao-status":"off",
   "canal-saida-tipo":0,
   "auto-role": 0,
   "auto-role-status":"off",
   "atualizado-por": "System(sistema)",
   "idioma": "pt-br",
   "prefixo":"rd.",
   "status-servidor": 0,
   "canais-bloqueados":"?",
   "usuarios-bloqueado": "?",
   "canal-sugestao-id": 0,
   "canal-sugestao-status":"off"}
   bard.guild.insert_one(serv).inserted_id

def ficha_criminal(ids, name):
   mongo = MongoClient(config.database.database)
   bard = mongo['bard']
   users = bard['users']
   serv ={
   "_id": str(ids),
   "nome": str(name),
   "id": str(ids),
   "foi_mute":"Não",
   "vezes_mute":"0",
   "foi_devhelper":"Não",
   "vezes_reportado":"0",
   "reputação":"0",
   "level":"0",
   "exp":"0",
   "historico":"Sem punições",
   "bots":["SD"],
   }
   bard.users.insert_one(serv).inserted_id

def get(ids,info):
    mongo = MongoClient(config.database.database)
    bard = mongo['bard']
    guild = bard['guild']
    guild = bard.guild.find_one({"_id": str(ids)})
    return guild[info]

def update(ids,name,info):
   mongo = MongoClient(config.database.database)
   bard = mongo['bard']
   guild = bard['guild']
   bard.guild.update_many({'_id': str(ids)}, {'$set': {name: str(info)}})
