from database import models
from flask import jsonify

def store_session_metadata(metadata):
    print(metadata['shard_tree'])
    #new_session = models.Session(id=metadata['session_id'],shard_tree=metadata['shard_tree'])
    new_session = models.Session(session_id=metadata['session_id'],shard_tree="123")
    models.db.session.add(new_session)
    models.db.session.commit()
    resp = jsonify(success=True)
    return resp

def store_shard(session_id,file_id,shard_data):
    new_shard = models.Shard(data=shard_data)
    models.db.session.add(new_shard)
    models.db.session.commit()
    resp = jsonify(success=True)
    return resp