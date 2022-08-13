# RegenbogenParty
## Docker deployment
### Docker Build & Run
``docker build -t rainbow . && docker run -p 2022:2022 rainbow``
## Manual installation
### Setup
``pip install -r requirements.txt``
### Run
`` flask --app hello run``

## For DEVS
### Create a python env
``python -m venv ./env``
``source env/bin/activate`` 
### Setup
``pip3 install -r requirements.txt``

## Install on Server
``apt-get install nginx certbot docker.io docker-compose``
- obtain certificate
- Use nginx.conf as site config and adapt URL
- paste into crontab ``* * * * * sh /root/update.sh``