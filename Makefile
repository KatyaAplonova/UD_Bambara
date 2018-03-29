# SETUP CREDENTIALS
HOST=corpora
# CHROOTS
TESTING=testing
PRODUCTION=production
ROLLBACK=rollback
TESTPORT=8098
PRODPORT=8099
RSYNC=rsync -avP --stats -e ssh

corpusfiles := $(wildcard conllu/*.conllu)
vertfiles := $(patsubst conllu/%.conllu,vert/%.vert,$(corpusfiles))
rawfiles := $(filter-out $(patsubst conllu/%,raw/%,$(corpusfiles)), $(patsubst html/%.html,raw/%.conllu,$(wildcard html/*.html)))

vert/%.vert: conllu/%.conllu scripts/conllu2vert
	gawk -f scripts/conllu2vert $< > $@

print-%:
	$(info $*=$($*))

raw/%.conllu: html/%.html
	python3 scripts/proc-bambara.py $< > $@

corbama-ud.vert: $(vertfiles) 
	mkdir -p vert/
	cat $(vertfiles) > $@

convert: 
compile: corbama-ud.vert config/corbama-ud
	rm -rf export/data/corbama-ud
	rm -f export/registry/corbama-ud
	mkdir -p export/data/corbama-ud
	encodevert -c ./config/corbama-ud -p export/data/corbama-ud corbama-ud.vert
	mkdir -p export/registry
	cp config/corbama-ud export/registry/
	bash -c "pushd export ; tar cJvf corbama-ud.tar.xz --mode='a+r' * ; popd"

get-remote-scripts:
	mkdir -p remote
	wget -P remote https://raw.githubusercontent.com/maslinych/corbama-build/master/remote/create-hsh.sh
	wget -P remote https://raw.githubusercontent.com/maslinych/corbama-build/master/remote/setup-bonito.sh
	wget -P remote https://raw.githubusercontent.com/maslinych/corbama-build/master/remote/setup-corpus-environment.sh
	wget -P remote https://raw.githubusercontent.com/maslinych/corbama-build/master/remote/testing2production.sh


create-testing:
	ssh $(HOST) 'test -d $(TESTING) || mkdir $(TESTING)'
	$(RSYNC) remote/*.sh $(HOST):
	ssh $(HOST) sh -x create-hsh.sh $(TESTING) $(TESTPORT)

setup-bonito:
	ssh $(HOST) hsh-run --rooter $(TESTING) -- 'sh setup-bonito.sh corbama corbama-ud' 

install-testing: 
	$(RSYNC) export/corbama-ud.tar.xz $(HOST):$(TESTING)/chroot/.in/
	ssh $(HOST) hsh-run --rooter $(TESTING) -- 'rm -rf /var/lib/manatee/{data,registry,vert}/corbama-ud*'
	ssh $(HOST) hsh-run --rooter $(TESTING) -- 'tar --no-same-permissions --no-same-owner -xJvf corbama-ud.tar.xz --directory /var/lib/manatee'

start-%:
	ssh $(HOST) tmux new-session -d -s $* \"export share_network=1 \; hsh-shell --root --mount=/proc $*\"
	sleep 5
	ssh $(HOST) tmux send-keys -t $*:0 \"service httpd2 start\" Enter

stop-%:
	ssh $(HOST) tmux send-keys -t $*:0 \"service httpd2 stop\" Enter
	ssh $(HOST) tmux kill-session -t $*

production: stop-production stop-testing
	$(RSYNC) remote/testing2production.sh $(HOST):$(TESTING)/chroot/.in/
	ssh $(HOST) hsh-run --rooter $(TESTING) -- 'sh testing2production.sh $(TESTPORT) $(PRODPORT)'
	ssh $(HOST) sh -c 'test -d $(ROLLBACK)/chroot && hsh --clean $(ROLLBACK) || echo empty rollback'
	ssh $(HOST) rm -rf $(ROLLBACK)
	ssh $(HOST) mv $(PRODUCTION) $(ROLLBACK)
	ssh $(HOST) mv $(TESTING) $(PRODUCTION)

rollback: stop-production
	$(RSYNC) remote/testing2production.sh $(HOST):$(PRODUCTION)/chroot/.in/
	ssh $(HOST) hsh-run --rooter $(PRODUCTION) -- 'sh testing2production.sh $(PRODPORT) $(TESTPORT)'
	ssh $(HOST) sh -c 'test -d $(TESTING)/chroot && hsh --clean $(TESTING)'
	ssh $(HOST) rm -rf $(TESTING)
	ssh $(HOST) mv $(PRODUCTION) $(TESTING)
	ssh $(HOST) mv $(ROLLBACK) $(PRODUCTION)

update-corpus:
	make compile
	make stop-testing
	make install-testing
	make start-testing
