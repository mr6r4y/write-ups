all: memcpy

memcpy: memcpy.c
	gcc -o $@ $^ -m32 -lm -no-pie

memcpy_64b: memcpy.c
	gcc -o $@ $^ -lm -no-pie

clean:
	rm memcpy

.PHONY: clean all
