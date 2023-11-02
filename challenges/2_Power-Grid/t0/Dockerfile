FROM ubuntu:23.04

RUN apt-get update && apt-get install -y gcc make socat

COPY . /scadaos/
WORKDIR /scadaos/
RUN make

CMD /scadaos/serve.sh
