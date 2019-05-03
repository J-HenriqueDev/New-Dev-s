import json

with open('data/database.json', encoding='utf-8') as f:
    data = json.load(f)
    prefix = data['prefix']
    token = data['token']
    status = data['status']
    admin = data['admin']
    database = data['database']
    shard_count = data['shard_count']
    shard_ids = data['shard_ids']
    canais = data['canais']

