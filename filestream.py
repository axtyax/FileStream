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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
models.db.app = app
models.db.init_app(app)
models.db.create_all()
models.db.session.commit()

shard_requests = {}

@app.route('/sitemap')
def sitemap():
    return Response(open("templates/sitemap.xml").read(), mimetype="text/xml")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

import upload

@app.route('/upload/metadata', methods=['POST'])
def process_metadata():
    if request.json["session_id"] in shard_requests.keys():
        shard_requests[request.json["session_id"]] = []
    return upload.store_session_metadata(request.json)

@app.route('/store_shard/<session_id>/<file_id>/<shard_id>', methods=['POST'])
def process_shard(session_id,file_id,shard_id):
    return upload.store_shard(session_id,file_id,shard_id,request.data)

@app.route('/check_shard_request/<session_id>', methods=['GET'])
def check_shard_request(session_id):
    if session_id in shard_requests.keys() and len(shard_requests[session_id]) > 0:
        req = shard_requests[session_id][0]
        print("SHARD REQUESTED %s" % req[1])
        del shard_requests[session_id][0]
        return req[1]
    else:
        return "null"

import download
import html
import json

@app.route('/d/<session_id>',methods=['GET'])
def download_page(session_id):
    metadata = download.retrive_session_metadata(session_id)
    return render_template("download.html",stream_metadata=json.loads(metadata))

@app.route('/request_shard/<session_id>/<file_id>/<shard_id>')
def request_shard(session_id,file_id,shard_id):
    shard = download.retrieve_shard(shard_id)
    #print(shard)
    if shard is None:
        if not session_id in shard_requests:
            shard_requests[session_id] = []
        shard_requests[session_id].append([file_id,shard_id])
        #print(shard_requests)
        return "null"
    else:
        data = shard.data
        download.delete_shard(shard_id)
        return data

if __name__ == '__main__':
    app.run(debug=True)

#Uploader sends metadata to server
#downloader gets metadata with the download page
#downloader requests shards from the server
#uploader sends requested shards to the server
#downloader pulls buffered shards from the server