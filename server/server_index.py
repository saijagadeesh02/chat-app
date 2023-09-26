from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS

import json
from definitions import EventNames
from db.f_database import ClientConnectionDB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", allow_multiple_connections=True)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@socketio.on("connect")
def handle_connection():
    # ClientConnectionDB.connection_map[room_id].append(request.sid)
    print(f"Client connected:{request.sid} with namespace {request.namespace}")

@socketio.on("disconnect")
def handle_connection():
    print(f"Client disconnected:{request.sid}")

@socketio.on(EventNames.CONNECT_EVENT.value)
def client_pair_connection(data):
    room_id = data["room_id"]
    ClientConnectionDB.connection_map[room_id].append(request.sid)
    print(f"Created an entry for client connection for room_id: {room_id}")


@socketio.on(EventNames.MESSAGE_EVENT.value)
def relay_messages(data):
    room_id = data["room_id"]
    message = data["message"]

    current_id = request.sid
    if len(ClientConnectionDB.connection_map[room_id]) == 2:
        
        for id in ClientConnectionDB.connection_map[room_id]:
            if id == current_id:
                continue
            socketio.emit(EventNames.MESSAGE_EVENT.value, message, to=id)
    else:
        socketio.emit(EventNames.MESSAGE_EVENT.value, "Chat partner did not join yet, Please wait..", to=current_id)
    print('received json: ' + str(data))


@app.route("/send_message/<id>/<msg>")
def send_message(id, msg):
    message_packet = {"sid" : id, "message" : msg}
    socketio.emit(EventNames.MESSAGE_EVENT.value, json.dumps(message_packet))
    return message_packet

@app.route("/")
def index():
    return jsonify("asdf;asdf")

if __name__ == '__main__':
    socketio.run(app, debug=True)