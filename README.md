# RegenbogenParty
## Docker deployment
### Docker Build
``docker build -t rainbow .``
### Docker Run
``docker run -p 2022:2022 rainbow``
## Manual installation
### Setup
``pip install -r requirements.txt``
### Run
`` flask --app hello run``

## For DEVS
### Create a python env
``python -m venv .``
``source myvenv/bin/activate`` 
### Setup
``pip install -r requirements.txt``
