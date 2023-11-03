FROM ubuntu:23.04

COPY inst2@t2-htpm-t0.ovpn /etc/openvpn/client/
RUN apt-get update && apt-get install -y \
	openvpn openssh-server \
	gcc make socat
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

COPY app/* /scadaos/
WORKDIR /scadaos/
RUN make
RUN echo -n "0" > /scadaos/shutdown.state

COPY scorebot/ /scorebot/

COPY bootstrap.sh .
CMD ./bootstrap.sh
