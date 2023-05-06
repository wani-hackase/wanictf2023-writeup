CC = gcc
SRCS = main.c
OBJS = chall
CFLAGS = -Wall -O0

.PHONY: clean

$(OBJS): $(SRCS)
	$(CC) $< -o $@ $(CFLAGS)
	
clean: 
	rm $(OBJS)
	