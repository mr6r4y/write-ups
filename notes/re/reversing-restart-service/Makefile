CC=gcc
CXX=g++
AS=as

tebpeb64.e: tebpeb64.h
	$(CC) -E -fpreprocessed -P $^ -o $@

all: tebpeb64.e

clean:
	rm tebpeb64.e