from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app, cors_allowed_origins="rainbow.jamo.app")

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

    if not scheduler.running:
        scheduler.start()

    emit('update', toSend)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


temp = 0
def test_emit():
    global temp

    toSend = {
        'frameCount': temp,
        'lightFuncData': {
            'identifier': 'constantColorCanvas',
            'params': {
                'color': 'hsl('+str(temp%360)+',100%, 50%)'
            }
        }
    }

    socketio.emit('update', toSend)


    temp += 20

scheduler = BackgroundScheduler()
job = scheduler.add_job(test_emit, 'interval', seconds=1)

if __name__ == '__main__':
    socketio.run(app, port=8080, host="0.0.0.0")