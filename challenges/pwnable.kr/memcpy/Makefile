all: memcpy

memcpy_32b: memcpy.c
	gcc -o $@ $^ -lm -m32 -malign-data=abi -no-pie

memcpy: memcpy.c
	gcc -o $@ $^ -lm -no-pie

clean:
	rm memcpy

.PHONY: clean all
