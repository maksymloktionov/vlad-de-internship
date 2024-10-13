#!/bin/bash

docker compose up -d --build

docker exec -it python-container bash