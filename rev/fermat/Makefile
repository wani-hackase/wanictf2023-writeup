.PHONY: clean
all: chall


SHELL = /bin/bash
FLAG = "FLAG{you_need_a_lot_of_time_and_effort_to_solve_reversing_208b47bd66c2cd8}"
CC = gcc
CFLAGS = -o src/fermat

chall: src/chall.c
	$(CC) $(CFLAGS) $<
	chmod -x src/fermat
	cp src/fermat file/fermat

clean: 
	rm src/fermat file/fermat
