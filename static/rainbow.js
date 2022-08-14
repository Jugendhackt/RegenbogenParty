const URL = window.location.href;
const ROOM_ID = URL.split('?')[0].split('/').pop()
const MODI = sessionStorage.getItem('modi')


function getNTPTime() {
    var clientTimestamp = (new Date()).valueOf();
    $.getJSON('http://europe.pool.ntp.org/getdatetimejson/?ct='+clientTimestamp, function( data ) {
    var nowTimeStamp = (new Date()).valueOf();
    var serverClientRequestDiffTime = data.diff;
    var serverTimestamp = data.serverTimestamp;
    var serverClientResponseDiffTime = nowTimeStamp - serverTimestamp;
    var responseTime = (serverClientRequestDiffTime - nowTimeStamp + clientTimestamp - serverClientResponseDiffTime )/2

    var syncedServerTime = new Date((new Date()).valueOf() + (serverClientResponseDiffTime - responseTime));
    console.log(syncedServerTime);
    alert(syncedServerTime);
    });

    console.log(clientTimestamp);
}


// TODO: Error Handling

// LightFuncs

function colorWheelCanvas(lightFuncParams) {
    return function (lightScreen, frameCount) {
        let prevFillStyle = lightScreen.canvasCTX.fillStyle;

        lightScreen.canvasCTX.fillStyle = `hsl(${frameCount % 360}, 100%, 50%)`;
        lightScreen.canvasCTX.fillRect(0, 0, lightScreen.canvas.width, lightScreen.canvas.height);

        lightScreen.canvasCTX.fillStyle = prevFillStyle;
    }
}

function cycleColorCanvas(lightFuncParams) {
    return function (lightScreen, frameCount) {
        let prevFillStyle = lightScreen.canvasCTX.fillStyle;

        lightScreen.canvasCTX.fillStyle = lightFuncParams.colors[frameCount%lightFuncParams.colors.length];
        lightScreen.canvasCTX.fillRect(0, 0, lightScreen.canvas.width, lightScreen.canvas.height);

        lightScreen.canvasCTX.fillStyle = prevFillStyle;
    }
}

function constantColorCanvas(lightFuncParams) {
    return function (lightScreen, frameCount) {
        let prevFillStyle = lightScreen.canvasCTX.fillStyle;

        lightScreen.canvasCTX.fillStyle = lightFuncParams.color;
        lightScreen.canvasCTX.fillRect(0, 0, lightScreen.canvas.width, lightScreen.canvas.height);

        lightScreen.canvasCTX.fillStyle = prevFillStyle;
    }
}

function getLightFunc(lightFuncData) {
    const lightFuncMap = {
        'constantColorCanvas': constantColorCanvas,
        'colorWheelCanvas': colorWheelCanvas,
        'cycleColorCanvas': cycleColorCanvas
    }

    return lightFuncMap[lightFuncData.identifier](lightFuncData.params)
}

class LightScreen {
    constructor(identifier, sendRequests) {
        this.identifier = identifier

        // Canvas Stuff
        this.canvas = null;
        this.canvasCTX = null;

        this.animationStart = 0;
        this.localFrameCount = 0;
        this.lightFunc = null;
        this.FPS = 2.75;
        this.frameInterval = 1000 / this.FPS;

        // WebSocket
        this.socket = this.getWebsocket();
        this.sendRequests = sendRequests;

        // NTP
        this.NTP_TIMES = {
            client_send_time: 0,
            server_recv_time: 0,
            server_send_time: 0,
            client_recv_time: 0
        }

        this.offsets = []
        this.offsetN = 5
        this.sendNTPRequest()
    }

    registerCanvas(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.canvasCTX = this.canvas.getContext("2d");

        this.canvas.width = window.innerWidth
        this.canvas.height = window.innerHeight
    }

    getWebsocket() {
        // TODO: Construct URL for WebSocket
        this.socket = io();
        this.socket.on('connect',
            function (id, socket) {
                return function () {
                    socket.emit("join", {"room": id});
                }
            }(this.identifier, this.socket));
        
        this.socket.on('update', this.onServerUpdate.bind(this))

        this.socket.on('ntp_client', this.onNTPClient.bind(this))

        this.socket.on('error', function(data){
            console.log(data.msg);
        })

        return this.socket;
    }

    request_update(mode) {
        data = get_json_for_mode(mode)
        this.socket.emit('update_room', data)
    }

    get_json_for_mode(modi) {
        if (modi == 1) {
            return {
                'startTime': ROOM_ID,
                'frameCount': 0,
                'lightFuncData': {
                    'identifier': 'SI',
                    'params': {
                        'colors': ['#FF0000', '#00FF00', '#0000FF', '#FF00FF'] 
                    }
                }
            }
        

        }
    }

    onServerUpdate(data) {
        this.animationStart = data.startTime;
        this.localFrameCount = data.frameCount;
        this.lightFunc = getLightFunc(data.lightFuncData);
    }

    
    sendNTPRequest() {
        this.NTP_TIMES.client_send_time = Date.now()
        this.socket.emit('ntp_server')
    }

    onNTPClient(data) {
        this.NTP_TIMES.client_recv_time = Date.now()
        this.NTP_TIMES.server_recv_time = data.recvTime;
        this.NTP_TIMES.server_send_time = data.sendTime; 
    
        this.offsets.push(((this.NTP_TIMES.server_recv_time - this.NTP_TIMES.client_send_time)+(this.NTP_TIMES.server_send_time - this.NTP_TIMES.client_recv_time))/2);


        this.offsetN--;
        if(this.offsetN <= 0){
            // Remove first to connections (outliers)
            this.offsets.shift()
            this.offsets.shift()

            this.offset = 0
            for (let i = 0; i < this.offsets.length; i++) {
                this.offset += this.offsets[i];
            }
            this.offset /= this.offsets.length
            console.log(this.offset);
        }
        else{
            this.sendNTPRequest()
        }
    }



    draw() {
        this.lightFunc(this, this.localFrameCount)
    }

    startSynchronosAnimation() {
        requestAnimationFrame(this.animateSynchronos.bind(this))
    }

    animateSynchronos() {
        requestAnimationFrame(this.animateSynchronos.bind(this))

        if(this.lightFunc == null) return

        let curr_server_time = Date.now()+this.offset;
        this.localFrameCount = Math.floor((curr_server_time - this.animationStart)/this.frameInterval);

        this.draw()
    }

}


let screen = new LightScreen(ROOM_ID)
screen.request_update(MODI)
screen.registerCanvas('canvas')
screen.startSynchronosAnimation()
