all: shellcode shellcode.s shellcode.o shellcode.x shellcode.bin

asm: asm.c
	gcc -o $@ $^ -no-pie

shellcode.s: shellcode.c
	gcc -S -o $@ $^ -nostdlib -fno-stack-protector -std=c99

shellcode.o: shellcode.s
	as -o $@ $^

shellcode.x: shellcode.o
	ld -N -o $@ $^

shellcode.bin: shellcode.x
	objcopy -O binary $^ $@

shellcode: shellcode.c
	gcc -o $@ $^ -nostdlib -fno-stack-protector -std=c99

clean:
	rm -f shellcode shellcode.s shellcode.o shellcode.x shellcode.bin


.PHONY: clean all
