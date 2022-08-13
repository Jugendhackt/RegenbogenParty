const URL = window.location.href;
const ROOM_ID = URL.split('?')[0].split('/').pop()


// TODO: Error Handling

// LightFuncs

function colorWheelCanvas(lightFuncParams) {
  return function(lightScreen, frameCount) {
    let prevFillStyle = lightScreen.canvasCTX.fillStyle;

    lightScreen.canvasCTX.fillStyle = `hsl(${frameCount%360}, 100%, 50%)`;
    lightScreen.canvasCTX.fillRect(0, 0, lightScreen.canvas.width, lightScreen.canvas.height);

    lightScreen.canvasCTX.fillStyle = prevFillStyle;
  }
}

function constantColorCanvas(lightFuncParams) {
  return function(lightScreen, frameCount) {
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

let temp = 0;



class LightScreen {
  constructor(identifier, sendRequests) {
    this.identifier = identifier
    
    // Canvas Stuff
    this.canvas = null;
    this.canvasCTX = null;

    this.localFrameCount = 0;
    this.lightFunc = null;
    this.FPS = 60;
    this.frameIntervall = 1000/this.FPS;

    
    // WebSocket
    this.socket = this.getWebsocket();
    this.sendRequests = sendRequests;

  }

  registerCanvas(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.canvasCTX =this.canvas.getContext("2d");

    this.canvas.width = window.innerWidth
    this.canvas.height = window.innerHeight
  }

  getWebsocket() {
    // TODO: Construct URL for WebSocket
    let socket = new WebSocket('ws://localhost:8080');
    socket.addEventListener('message', this.onServerMessage.bind(this));

    return socket;
  }

  requestCurrentState() {
    // TODO: Send message to server requesting current light source state
  }

  onServerMessage(event) {
    // TODO: React to server message
    console.log(event.data);
    
    const msgTypeMap = {
      'update': this.onServerUpdate
    }

    msgTypeMap[event.data.msgType](event);

  }

  onServerUpdate(event) {
    const updateInfo = event.config();

    this.localFrameCount = updateInfo.frameCount;
    this.lightFunc = getLightFunc(updateInfo.lightFuncData);
  }



  requestCurrentState() {
    // TODO: Request current frameCount and lightFuncData from Server
  }

  draw(){
    this.lightFunc(this, this.localFrameCount)
  }

  startSynchronosAnimation() {
    requestAnimationFrame(this.animateSynchronos.bind(this))
  }

  animateSynchronos() {
    let currentState = this.requestCurrentState();

    
    this.draw()
    requestAnimationFrame(this.animateSynchronos.bind(this))
  }

}



let screen = new LightScreen(ROOM_ID)
screen.registerCanvas('canvas')
screen.startSynchronosAnimation()
