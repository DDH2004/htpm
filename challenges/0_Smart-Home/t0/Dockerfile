FROM ubuntu:22.04

COPY inst0@t0-htpm-t0.ovpn /etc/openvpn/client/
RUN apt-get update && apt-get install -y \
	openvpn openssh-server \
	python3-pip python3-venv
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

WORKDIR /app/
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY app/ /app/
RUN pip install -Ur requirements.txt

COPY bootstrap.sh .
CMD ./bootstrap.sh
