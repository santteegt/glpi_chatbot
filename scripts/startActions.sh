#!/bin/bash

rasa run actions --actions actions -p 5055 > actions.out.logs 2>&1 &
