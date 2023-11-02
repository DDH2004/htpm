#!/bin/bash

echo ":: Copying VPN files to their appropriate targets."
cp "vpn/t0/inst0@t0-htpm-t0.ovpn" ../challenges/0_Smart-Home/t0/
cp "vpn/t0/inst0@t0-htpm-d0.ovpn" ../challenges/0_Smart-Home/d0/
cp "vpn/t0/inst0@t0-htpm-d1.ovpn" ../challenges/0_Smart-Home/d1/
cp "vpn/t0/inst0@t0-htpm-d2.ovpn" ../challenges/0_Smart-Home/d2/
