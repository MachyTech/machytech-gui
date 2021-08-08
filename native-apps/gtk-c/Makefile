SHELL = /bin/sh

.SUFFIXES:
.SUFFIXES: .c .o .h

CC = gcc
OBJS = src/main.c
CFLAGS = -g -Wall -Imachy-api/ `pkg-config --cflags gtk4`
LDFLAGS = `pkg-config --libs gtk4`

app: ${OBJ}
	${CC} ${CFLAGS} ${OBJS} -o $@ ${LDFLAGS}
clean:
	${RM} app