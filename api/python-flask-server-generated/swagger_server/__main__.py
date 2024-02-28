#!/usr/bin/env python3

import connexion
from swagger_server import encoder

from pymongo import MongoClient
# from flask_socketio import SocketIO
from flask import send_from_directory

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'kb-indexer API'}, pythonic_params=True)
    
    
    @app.route('/')
    def root():
        return send_from_directory('./frontend', 'index.html')
    app.run(port=8080)

    # socketio = SocketIO(app.app)
    # socketio.run(app.app, port=8080)


if __name__ == '__main__':
    main()
