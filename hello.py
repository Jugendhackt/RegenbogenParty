from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')\

@app.route('/rainbow/<string:roomName>')
def rainbow(roomName):
    return render_template('rainbow.html')

@app.route('/room/<string:roomName>')
def room(roomName):
    print(roomName)
    return render_template('index.html')

from flask_socketio import join_room, leave_room

@socketio.on('join')
def on_join(data):
#    username = data['username']
    room = data['room']
    join_room(room)
    send("someone" + ' has entered the room.', to=room)
    emit("change", to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)

@socketio.on('connect')
def test_connect():
    toSend = {
        'frameCount': 0,
        'lightFuncData': {
            'identifier': 'constantColorCanvas',
            'params': {
                'color': '#FF80FF'
            }
        }
    }

    emit('update', toSend)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('change')
def lol():
    emit('change', to="moin")

if __name__ == '__main__':
    socketio.run(app, port=8080, host="0.0.0.0")