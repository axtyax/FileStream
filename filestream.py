from flask import Flask
from flask import render_template
from flask import Response
from flask import request
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from database import models
import os
try:
    os.remove("database/database.db")
except OSError:
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
models.db.app = app
models.db.init_app(app)
models.db.create_all()
models.db.session.commit()

@app.route('/sitemap')
def sitemap():
    return Response(open("templates/sitemap.xml").read(), mimetype="text/xml")

@app.route('/')
def index():
    return render_template("index.html")

import upload

@app.route('/upload/metadata', methods=['POST'])
def process_metadata():
    return upload.store_session_metadata(request.json)

@app.route('/upload/<session_id>/<file_id>', methods=['POST'])
def process_shard(session_id,file_id):
    return upload.store_shard(session_id,file_id,request.data)

if __name__ == '__main__':
    app.run(debug=True)