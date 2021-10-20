#!/bin/bash

# Install MicroK8s
sudo snap install microk8s --classic
sudo microk8s status --wait-ready
sudo microk8s enable storage dns ingress
sudo usermod -a -G microk8s $USER

# Install Juju
sudo snap install juju --classic
sg microk8s -c 'juju bootstrap microk8s'
