const URL = window.location.href;
const ROOM_ID = URL.split('?')[0].split('/').pop()


function getNTPTime() {
    $.data = function(success){
        $.get("http://json-time.appspot.com/time.json?callback=?", function(response){
            success(new Date(response.datetime));
        }, "json");
    };
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
        'colorWheelCanvas': colorWheelCanvas
    }

    return lightFuncMap[lightFuncData.identifier](lightFuncData.params)
}

class LightScreen {
    constructor(identifier, sendRequests) {
        this.identifier = identifier

        // Canvas Stuff
        this.canvas = null;
        this.canvasCTX = null;

        this.localFrameCount = 0;
        this.lightFunc = null;
        this.FPS = 60;
        this.frameIntervall = 1000 / this.FPS;


        // WebSocket
        this.socket = this.getWebsocket();
        this.sendRequests = sendRequests;

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

        return this.socket;
    }

    onServerUpdate(data) {
        this.localFrameCount = data.frameCount;
        this.lightFunc = getLightFunc(data.lightFuncData);
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

        this.draw()
        this.localFrameCount++;
    }

}


let screen = new LightScreen(ROOM_ID)
screen.registerCanvas('canvas')
screen.startSynchronosAnimation()
