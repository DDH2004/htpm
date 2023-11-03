#!/bin/sh

mkdir -p /dev/net/
mknod /dev/net/tun c 10 200
chmod 600 /dev/net/tun
openvpn /etc/openvpn/client/inst2\@t2-htpm-d2.ovpn &
service ssh restart
while true; do sleep 1000; done
