#!/bin/bash
echo "--- Installing system packages and Python dependencies ---"
sudo apt-get update && sudo apt-get install -y python3-pip python3-tk libappindicator3-1
pip3 install -r requirements.txt
echo "--- To run the application, use the following command: ---"
echo "--- GEMINI_API_KEY=\"AIzaSyA4KmRpgNMTv_-t88kbViC-u9opf2iJoeQ\" python3 main.py ---"
