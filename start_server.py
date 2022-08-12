from flask import Flask

app = Flask('RegenbogenParty')

@app.route('/')
def index():
    return 'Web App with Python Flask!'

app.run(host='192.168.21.145', port=8080)