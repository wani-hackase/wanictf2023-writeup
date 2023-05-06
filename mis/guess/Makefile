.PHONY: build test

SHELL = /bin/bash
FLAG = "FLAG{How_did_you_know?_10794fcf171f8b2}"

build:
	FLAG=$(FLAG) python src/chall.py
	cp src/chall.py file/chall.py

test:
	@echo Output: $(shell python solver/solve.py)
	@echo Answer: $(FLAG)
