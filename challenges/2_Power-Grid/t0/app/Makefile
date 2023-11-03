CFLAGS=-no-pie -std=c99 -Wno-deprecated-declarations -fno-stack-protector -Wno-format-security

all:
	gcc main.c -o scadaos ${CFLAGS} -D SECRET_LOCATION=\"/scadaos/secret\"
debug:
	gcc main.c -o scadaos ${CFLAGS} -D SECRET_LOCATION=\"./secret\"
clean:
	rm scadaos
