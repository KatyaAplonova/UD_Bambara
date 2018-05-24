import sys;

nlc = 0;
first = True;
line = sys.stdin.readline();
while line:
	if line.strip() == '': #{
		nlc = nlc + 1;
	#}

	if line.strip() != '': #{
		nlc = 0;
	#}

	if line.strip() == '' and nlc > 1: #{
		first = False;
		line = sys.stdin.readline()
		continue;
	elif line.strip() == '' and first: #{
		first = False;
		line = sys.stdin.readline()
		continue;
	else: #{
		sys.stdout.write(line);
	#}
	first = False;
	line = sys.stdin.readline()
#}
