from database import models

def store_shard(session_id,file_id,shard_data):
    new_shard = models.Shard(data=shard_data)
    models.db.session.add(new_shard)
    models.db.session.commit()