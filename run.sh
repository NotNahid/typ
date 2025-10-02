#!/bin/bash
   2     echo "--- Installing system packages and Python dependencies ---"
   3     sudo apt-get update && sudo apt-get install -y python3-pip python3-tk libappindicator3-1
   4     pip3 install -r requirements.txt
   5     
   6     echo "--- To run the application, use the following command: ---"
   7     echo "--- GEMINI_API_KEY=\"YOUR_API_KEY\" python3 main.py ---"
