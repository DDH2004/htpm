#!/bin/sh

socat \
	-T 60 \
	TCP-LISTEN:2981,reuseaddr,fork \
	EXEC:"./scadaos"
