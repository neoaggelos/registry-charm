#!/bin/bash

# Install Charmcraft
sudo snap install charmcraft --classic

# Install LXD
sudo snap install lxd
sudo lxd init --auto
sudo usermod -a -G lxd $USER
