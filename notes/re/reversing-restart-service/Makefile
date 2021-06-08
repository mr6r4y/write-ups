CC=gcc
CXX=g++
WIN_CXX=x86_64-w64-mingw32-g++-win32
AS=as

tebpeb64.e: tebpeb64.h
	$(CC) -E -fpreprocessed -P $^ -o $@

animals.exe: animals.cpp
	$(WIN_CXX) $^ -o $@ -O2 -std=c++11

all: tebpeb64.e animals.exe

clean:
	rm tebpeb64.e animals.exe