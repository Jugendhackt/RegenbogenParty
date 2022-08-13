from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
#app.debug = True
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def index1():
    return render_template('demo.html')

@app.route('/demo_client')
def index2():
    return render_template('demo_client.html')

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
    room = data['room']
    join_room(room)
    send("someone" + ' has entered the room.', to=room)
    emit("change", to=room)

@socketio.on('newColor')
def newColor(data):
    emit("newColor", {"color":data["color"]}, to=data['room'])

@socketio.on('connect')
def test_connect():
    emit("moin")

if __name__ == '__main__':
    socketio.run(app, port=8080, host="0.0.0.0")