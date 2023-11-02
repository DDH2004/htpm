# Dockerfile, Image, Container
FROM ubuntu:22.04

WORKDIR /app/

RUN apt-get update && apt-get install -y python3-pip python3-venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY target/ /app/
RUN pip install -Ur /app/requirements.txt

WORKDIR /app/

EXPOSE 8080
CMD [ "python", "main.py", "0.0.0.0", "8080"]