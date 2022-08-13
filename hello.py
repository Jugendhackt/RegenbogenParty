from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@app.route("/")
def hello_world():
    return render_template("index.html")

@sock.route('/room/<string:roomname>')
def echo(ws, roomname):
    while True:
        data = ws.receive()
        ws.send(roomname)

app.run(host='0.0.0.0', port=2022)