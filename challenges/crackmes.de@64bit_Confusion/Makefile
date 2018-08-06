all: key.txt

64bit_Confusion: 64bit_Confusion.tar.gz
	tar -xvzf $^

64bit_Confusion.patched: 64bit_Confusion
	cp $^ $@ && r2 -n -w -q -i patch.r2 $@ && chmod +x $@

key.txt: 64bit_Confusion.patched
	gdb -q -x ./debug.gdb $^

clean:
	rm -f 64bit_Confusion 64bit_Confusion.patched 64_bit_README key.txt

.PHONY: clean all exec