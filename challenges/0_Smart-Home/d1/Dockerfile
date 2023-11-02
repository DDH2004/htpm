FROM ubuntu:22.04

COPY inst0@t0-htpm-d1.ovpn /etc/openvpn/client/
RUN apt-get update && apt-get install -y openvpn openssh-server

COPY bootstrap.sh .
CMD ./bootstrap.sh
