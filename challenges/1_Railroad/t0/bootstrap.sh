#!/bin/sh

mkdir -p /dev/net/
mknod /dev/net/tun c 10 200
chmod 600 /dev/net/tun
openvpn /etc/openvpn/client/inst1\@t1-htpm-t0.ovpn &
service ssh restart
python3 /scorebot/main.py &
while true; do sleep 1000; done
