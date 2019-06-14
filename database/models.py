from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Session(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String)
    meta_data = db.Column(db.String)

    def __repr__(self):
        return '<Session ID %r>' % self.session_id

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.String, primary_key=True)
    #session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    num_shards = db.Column(db.Integer)

    def __repr__(self):
        return '<File ID %r>' % self.id

class Shard(db.Model):
    __tablename__ = 'shard'
    id = db.Column(db.String, primary_key=True)
    #file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    shard_index = db.Column(db.Integer)
    data = db.Column(db.LargeBinary, unique=True, nullable=False)

    def __repr__(self):
        return '<Shard ID %r>' % self.id