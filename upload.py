from database import models
from flask import jsonify
import json

def store_session_metadata(metadata):
    print(metadata)
    new_session = models.Session(session_id=metadata['session_id'],meta_data=json.dumps(metadata))
    models.db.session.add(new_session)
    models.db.session.commit()
    resp = jsonify(success=True)
    return resp

def store_shard(session_id,file_id,shard_id,shard_data):
    new_shard = models.Shard(id=shard_id,data=shard_data)
    models.db.session.add(new_shard)
    models.db.session.commit()
    resp = jsonify(success=True)
    return resp