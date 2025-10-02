#!/bin/bash

echo "--- Disabling CD-ROM repository to fix installation issues ---"
sudo sed -i -e '/^deb cdrom:/s/^/#/' /etc/apt/sources.list

echo "--- Installing system packages ---"
sudo apt-get update
sudo apt-get install -y python3-pip python3-tk libappindicator3-1

echo "--- Installing Python packages ---"
pip3 install -r requirements.txt

echo "--- Installation complete! ---"
echo "--- You can now run the application. ---"
