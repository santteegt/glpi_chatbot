#!/bin/bash

rasa x --data data/train/ --endpoints endpoints.yml --cors '*' --enable-api --port 5005 --rasa-x-port 5002 > rasax.out.logs 2>&1 &
