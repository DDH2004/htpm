#!/bin/sh

mkdir -p /dev/net/
mknod /dev/net/tun c 10 200
chmod 600 /dev/net/tun
openvpn /etc/openvpn/client/inst2\@t2-htpm-t0.ovpn &
service ssh restart
python3 /scorebot/main.py &
socat \
	-T 60 \
	TCP-LISTEN:2981,reuseaddr,fork \
	EXEC:"./scadaos"
