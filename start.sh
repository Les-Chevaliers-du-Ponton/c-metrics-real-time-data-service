#!/bin/bash

src/redis-cli -h cmetrics-cache-w3yveh.serverless.use1.cache.amazonaws.com --tls -p 6379 &
python3 /app/main.py
