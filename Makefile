# SETUP CREDENTIALS
HOST=corpora
# CHROOTS
TESTING=testing
PRODUCTION=production
ROLLBACK=rollback
TESTPORT=8098
PRODPORT=8099
RSYNC=rsync -avP --stats -e ssh
BUILT=built

corpbasename := corbama-ud
corpsite := corbama
corpora := corbama-ud
include remote.mk

corpusfiles := $(wildcard conllu/*.conllu)
vertfiles := $(patsubst conllu/%.conllu,vert/%.vert,$(corpusfiles))
rawfiles := $(filter-out $(patsubst conllu/%,raw/%,$(corpusfiles)), $(patsubst html/%.html,raw/%.conllu,$(wildcard html/*.html)))
conllufiles := $(patsubst raw/%,conllu/%, $(rawfiles))


vert/%.vert: conllu/%.conllu scripts/conllu2vert
	gawk -f scripts/conllu2vert $< > $@

print-%:
	$(info $*=$($*))

raw/%.conllu: html/%.html
	python3 scripts/proc-bambara.py $< > $@

conllu/%.conllu: raw/%.conllu
	cat $< | udpipe --parse bambara.model > $@

corbama-ud.vert: $(vertfiles) 
	mkdir -p vert/
	cat $(vertfiles) > $@

convert: $(rawfiles)

parse: $(corpusfiles)

compile: corbama-ud.vert config/corbama-ud
	rm -rf export/data/corbama-ud
	rm -f export/registry/corbama-ud
	mkdir -p export/data/corbama-ud
	encodevert -c ./config/corbama-ud -p export/data/corbama-ud corbama-ud.vert
	mkdir -p export/registry
	cp config/corbama-ud export/registry/
	bash -c "pushd export ; tar cJvf corbama-ud.tar.xz --mode='a+r' * ; popd"

