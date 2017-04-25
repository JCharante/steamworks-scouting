#!/usr/bin/env bash
echo "Attempting to open http://0.0.0.0:8000/ in your browser"
xdg-open http://0.0.0.0:8000/ &
python3 -m http.server 8000
