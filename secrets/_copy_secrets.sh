#!/bin/bash

echo ":: Copying VPN files to their appropriate targets."
cp "vpn/t0/inst0@t0-htpm-t0.ovpn" ../challenges/0_Smart-Home/t0/
cp "vpn/t0/inst0@t0-htpm-d0.ovpn" ../challenges/0_Smart-Home/d0/
cp "vpn/t0/inst0@t0-htpm-d1.ovpn" ../challenges/0_Smart-Home/d1/
cp "vpn/t0/inst0@t0-htpm-d2.ovpn" ../challenges/0_Smart-Home/d2/
cp "vpn/t0/inst0@t0-htpm-t0.ovpn" ../challenges/0_Smart-Home/t0/
cp "vpn/t1/inst1@t1-htpm-d0.ovpn" ../challenges/1_Railroad/d0/
cp "vpn/t1/inst1@t1-htpm-t0.ovpn" ../challenges/1_Railroad/t0/
cp "vpn/t2/inst2@t2-htpm-t0.ovpn" ../challenges/2_Power-Grid/t0/
cp "vpn/t2/inst2@t2-htpm-d0.ovpn" ../challenges/2_Power-Grid/d0/
cp "vpn/t2/inst2@t2-htpm-d1.ovpn" ../challenges/2_Power-Grid/d1/
cp "vpn/t2/inst2@t2-htpm-d2.ovpn" ../challenges/2_Power-Grid/d2/

echo ":: Copying target WAP secrets."
cp wap/t0-config.h ../challenges/0_Smart-Home/_firmware/wap/config.h
cp wap/t2-config.h ../challenges/2_Power-Grid/_firmware/wap/config.h

echo ":: Copying scorebot config secrets."
cp scorebot/secrets.py ../software/scorebot/secrets.py
cp scorebot/t0-secrets.py ../challenges/0_Smart-Home/t0/scorebot/secrets.py
cp scorebot/t2-secrets.py ../challenges/2_Power-Grid/t0/scorebot/secrets.py

echo ":: Copying power grid login secret."
cp login/t2-secret ../challenges/2_Power-Grid/t0/app/secret

echo ":: Copying public SSH key to railroad."
cp login/t1-pubkey ../challenges/1_Railroad/t0/authorized_hosts
