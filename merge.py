import sys
#open files and read in
f1 = open(sys.argv[1], 'r') # vert file
f2 = open(sys.argv[2], 'r') # conllu file
text1 = {} # text1 is a dict -> list of lines mapped by sentence id
text2 = {} # text2 is a dict -> list of lines mapped by sentence id
#go through every line 
sentence_id = 0
for line in f1: # for each of the lines in the vert file
    if line.count('<s>'): # if the line contains a <s> it's a new sentence
        sentence_id += 1 
    if sentence_id not in text1: # if we haven't seen the sentence before
        text1[sentence_id] = []
    text1[sentence_id].append(line.strip('\n')) # append the line to the lines for that sentence
    

for line in f2:
    if line.count('sent_id'):
        # extract the numerical id from the sent_id comment line in the conllu
        sentence_id = int(line.split(':')[-1])
    if sentence_id not in text2:
        text2[sentence_id] = []
    text2[sentence_id].append(line.strip('\n'))
f1.close()
f2.close()

#count max tabs
def max_tabs(text):
    current_max = 0
    for line in text:
        line_length = len(line.split('\t'))
        if line_length > current_max:
            current_max = len(line.split('\t'))
            current_max -= 1
    return current_max

for sentence in text1:
    if sentence in text2:
        # -2 for skipping length incl. comments, 2 for getting the first word in the sentece 
        print('<!--',len(text2[sentence])-2,text2[sentence][2],'-->')
    for line in text1[sentence]:
        print(line)
   
