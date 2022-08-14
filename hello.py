from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from flask_socketio import join_room, leave_room

import time



app = Flask(__name__)
#app.debug = True
socketio = SocketIO(app, cors_allowed_origins="*")

roomStartTimes = dict()
availableRooms = set()

def getRoomStartTime(roomID):
    if roomID in roomStartTimes:
        return roomStartTimes[roomID]

    roomStartTimes[roomID] = time.time()*1000

def roomExists(roomID):
    return roomID in availableRooms

def createRoom(roomID):
    print("Hello")
    if roomExists(roomID):
        print("Tried to create already existing room")
    else:
        print("Hell2")
        availableRooms.add(roomID)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roomJoin')
def roomJoin():
    return render_template('roomJoin.html')

@app.route('/roomCreate')
def roomCreate():
    return render_template('roomCreate.html')

@app.route('/demo')
def index1():
    return render_template('demo.html')

@app.route('/demo_client')
def index2():
    return render_template('demo_client.html')

@app.route('/rainbow/<string:roomName>')
def rainbow(roomName):
    return render_template('rainbow.html')

"""
@app.route('/room/<string:roomName>')
def room(roomName):
    print(roomName)
    return render_template('index.html')
"""


@socketio.on('join')
def on_join(data):
    roomID = data['room']
    print(roomID)
    print(availableRooms)

    if not roomExists(roomID):
        emit('error', {'msg':'Room does not exist'})
    
    else:
        join_room(roomID)
        toSend = {
            'startTime': getRoomStartTime(roomID),
            'frameCount': 0,
            'lightFuncData': {
                'identifier': 'cycleColorCanvas',
                'params': {
                    'colors': ['#FF0000', '#00FF00', '#0000FF', '#FF00FF'] 
                }
            }
        }

        emit('update', toSend)
        print("new user")



@socketio.on('newColor')
def newColor(data):
    emit("newColor", {"color":data["color"]}, to=data['room'])

"""
@socketio.on('connect')
def on_client_connect():
    print(data)
    roomID = 123;#data['room']

    print("Hello")
    toSend = {
        'startTime': getRoomStartTime(roomID),
        'frameCount': 0,
        'lightFuncData': {
            'identifier': 'cycleColorCanvas',
            'params': {
                'colors': ['#FF0000', '#00FF00', '#0000FF', '#FF00FF'] 
            }
        }
    }

    emit('update', toSend)
"""

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('ntp_server')
def on_ntp_server():
    recvTime = time.time()*1000

    toSend = {
        'recvTime': recvTime,
        'sendTime':  time.time()*1000
    }

    emit('ntp_client', toSend)


createRoom('123')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
    

    