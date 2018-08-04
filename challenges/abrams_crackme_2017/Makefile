all: abrams_crackme_2017.decr abrams_crackme_2017.cracked

abrams_crackme_2017: abrams_crackme_2017.tar.gz
	tar -xvzf $^

abrams_crackme_2017.fix: abrams_crackme_2017
	cp $^ $@ && r2 -q -n -w -i load0.segment-size.patch.r2 $@ && r2 -q -n -w -i eh_frame.section-size.patch.r2 $@

abrams_crackme_2017.decr: abrams_crackme_2017.fix
	python decryptor.py -i $^ -o $@ && chmod +x $@

abrams_crackme_2017.cracked: abrams_crackme_2017
	cp $^ $@ && r2 -q -n -w -i crack-patch.r2 $@

clean:
	rm -f abrams_crackme_2017 abrams_crackme_2017.fix abrams_crackme_2017.decr abrams_crackme_2017.cracked

.PHONY: clean all