FROM ubuntu:22.04

COPY inst2@t2-htpm-d1.ovpn /etc/openvpn/client/
RUN apt-get update && apt-get install -y openvpn openssh-server

COPY bootstrap.sh .
CMD ./bootstrap.sh
