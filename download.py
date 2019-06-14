from database import models
from flask import jsonify

def retrive_session_metadata(session_id):
    metadata = models.Session.query.filter_by(session_id = session_id).first()
    print(metadata)
    if metadata is None:
        return "none"
    return metadata.meta_data

def retrieve_shard(shard_id):
    shard = models.db.query(models.Shard).filter_by(id=shard_id)
    return shard