#!/bin/bash
python server.py >> log/server.log 2>&1 &
echo $! > pids/server.pid
