FROM ubuntu:22.04

COPY inst1@t1-htpm-t0.ovpn /etc/openvpn/client/
RUN apt-get update && apt-get install -y openvpn openssh-server
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo "AuthorizedKeysFile .ssh/authorized_keys" >> /etc/ssh/sshd_config
COPY authorized_keys /root/.ssh/

COPY scorebot /scorebot/

COPY bootstrap.sh .
CMD ./bootstrap.sh
