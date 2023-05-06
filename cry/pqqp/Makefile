.PHONY: build test

SHELL = /bin/bash
FLAG = "FLAG{p_q_p_q_521d0bd0c28300f}"

build:
	FLAG=$(FLAG) python src/chall.py | tee src/output.txt
	cp src/output.txt file/output.txt

test:
	@echo Output: $(shell python solver/solve.py)
	@echo Answer: $(FLAG)
	
