from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index2.html')

@socketio.on('connect')
def handle_connect():
    print(f'Client {request.sid} connected')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client {request.sid} disconnected')

@socketio.on('join')
def on_join(data):
    if isinstance(data, dict):
        username = data.get('username')
        room = data.get('room')
        join_room(room)
        print(f'{username} has joined the room {room}')
        emit('message', f'{username} has entered the Chat.', room=room)
    else:
        print("Join event data is not a dictionary")

@socketio.on('leave')
def on_leave(data):
    if isinstance(data, dict):
        username = data.get('username')
        room = data.get('room')
        leave_room(room)
        print(f'{username} has left the room {room}')
        emit('message', f'{username} has left the room.', room=room)
    else:
        print("Leave event data is not a dictionary")

@socketio.on('message')
def handle_message(data):
    if isinstance(data, dict):
        room = data.get('room')
        msg = data.get('msg')
        print(f'Message in {room}: {msg}')
        emit('message', msg, room=room)
    else:
        print("Message event data is not a dictionary")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')