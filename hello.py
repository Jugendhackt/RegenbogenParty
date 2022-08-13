from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from apscheduler.schedulers.background import BackgroundScheduler

import ntplib
from time import ctime



app = Flask(__name__)
#app.debug = True
socketio = SocketIO(app, cors_allowed_origins="*")

ntp = ntplib.NTPClient()
roomStartTimes = dict()

def getRoomStartTime(roomID):
    if roomID in roomStartTimes:
        return roomStartTimes[roomID]

    response = ntp.request('europe.pool.ntp.org', version=3)
    roomStartTimes[roomID] = response.tx_time


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
    print("new user")

@socketio.on('newColor')
def newColor(data):
    emit("newColor", {"color":data["color"]}, to=data['room'])

@socketio.on('connect')
def test_connect():
    startTime = getRoomStartTime('123')
    print(startTime)

    toSend = {
        'startTime': getRoomStartTime('123'),
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

@socketio.on('ntp_server')
def test_connect():
    recvTime = time.time()

    toSend = {
        'recvTime': recvTime,
        'sendTime':  time.time()
    }

    emit('ntp_client', toSend)

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
    socketio.run(app, host='0.0.0.0')
    

    