#!/bin/bash
cd /home/jamo/rainbow/RegenbogenParty && git pull -r && cd .. && docker-compose build && docker-compose up -d