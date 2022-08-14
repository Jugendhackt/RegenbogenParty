from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
from flask_socketio import join_room, leave_room

import time



app = Flask(__name__)
#app.debug = True
socketio = SocketIO(app, cors_allowed_origins="*")

availableRooms = set()
roomStartTimes = dict()
roomLightFunc = dict()

userRoomMap = dict()

def getRoomStartTime(roomID):
    if roomID in roomStartTimes:
        return roomStartTimes[roomID]

    roomStartTimes[roomID] = time.time()*1000

def getRoomLightFunc(roomID):
    if roomID in roomLightFunc:
        return roomLightFunc[roomID]
    
    return {
       'identifier': 'constantColorCanvas',
        'params': {
            'color': '#FF0000'
        }
    }

def updateRoomLightFunc(roomID, newLightFunc):
    if roomExists(roomID):
        roomLightFunc[roomID] = newLightFunc
        roomStartTimes[roomID] = time.time()*1000
        return True
    return False

def roomExists(roomID):
    return roomID in availableRooms

def createRoom(roomID):
    availableRooms.add(roomID)

def userSwitchRoom(username, roomID):
    ret = None if username not in userRoomMap else userRoomMap[username]

    if username in userRoomMap and roomID is None:
        del userRoomMap[username]
    else:
        userRoomMap[username] = roomID

    return ret

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
    username = request.sid
    roomID = data['room']

    if not roomExists(roomID):
        emit('error', {'msg':'Room does not exist'})
    
    else:
        to_leave = userSwitchRoom(username,roomID)
        if to_leave is not None:
            leave_room(to_leave)
            print(str(username) + " left room "+str(to_leave))
        
        join_room(roomID)
        print(str(username) + " joined room "+str(roomID))

        toSend = {
            'startTime': getRoomStartTime(roomID),
            'frameCount': 0,
            'lightFuncData': getRoomLightFunc(roomID)
        }
        emit('update', toSend)



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
    username = request.sid
    to_leave = userSwitchRoom(username,None)
    if to_leave is not None:
        leave_room(to_leave)
        print(str(username) + " left room "+str(to_leave))
    print('Client disconnected')

@socketio.on('ntp_server')
def on_ntp_server():
    recvTime = time.time()*1000

    toSend = {
        'recvTime': recvTime,
        'sendTime':  time.time()*1000
    }

    emit('ntp_client', toSend)


@socketio.on('update_room')
def on_update_room(data):
    roomID = data['room']
    if not roomExists(roomID):
        createRoom(roomID)
    
    updateRoomLightFunc(roomID, data['lightFuncData'])

    toSend = {
        'startTime': getRoomStartTime(roomID),
        'frameCount': 0,
        'lightFuncData': getRoomLightFunc(roomID)
    }

    socketio.emit('update', toSend, to=roomID)
    
    emit('roomAvailable')



createRoom('123')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
    

    