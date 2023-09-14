from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", allow_multiple_connections=True)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@socketio.on("connect")
def handle_connection():
    print(f"Client connected:{request.sid}")

@socketio.on("disconnect")
def handle_connection():
    print(f"Client disconnected:{request.sid}")

@socketio.on('my_event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@app.route("/")
def index():
    return jsonify("asdf;asdf")

if __name__ == '__main__':
    socketio.run(app, debug=True)