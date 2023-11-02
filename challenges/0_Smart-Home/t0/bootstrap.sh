#!/bin/sh

mkdir -p /dev/net/
mknod /dev/net/tun c 10 200
chmod 600 /dev/net/tun
openvpn /etc/openvpn/client/inst0\@t0-htpm-t0.ovpn &
service ssh restart
python3 main.py 0.0.0.0 80
