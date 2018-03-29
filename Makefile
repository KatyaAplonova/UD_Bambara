corpusfiles := $(wildcard conllu/*.conllu)
vertfiles := $(patsubst conllu/%.conllu,vert/%.vert,$(corpusfiles))

vert/%.vert: conllu/%.conllu
	gawk -f scripts/conllu2vert $< > $@

corbama-ud.vert: $(vertfiles)
	mkdir -p vert/
	cat $(vertfiles) > $@

compile: corbama-ud.vert config/corbama-ud
	rm -rf export/data/corbama-ud
	rm -f export/registry/corbama-ud
	mkdir -p export/data/corbama-ud
	encodevert -c ./config/corbama-ud -p export/corbama-ud/data corbama-ud.vert
