#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse


def get_columns(sent, columns=None):
    for token in sent:
        fields = token.split('\t')
        if columns:
            try:
                yield '\t'.join([fields[i] for i in columns])
            except  IndexError:
                print("ERR LINE:", fields)
        else:
            yield token

def tokens_match(t1, t2, compareby):
    f1 = t1.split('\t')
    f2 = t2.split('\t')
    return f1[compareby[0]] == f2[compareby[1]]


def main():
    def parse_arguments():
        parser = argparse.ArgumentParser(
            description = 'Merge vertical fiɛs from BRC with CONLLU')
        parser.add_argument('-b',  '--brc', help="BRC vertical file")
        parser.add_argument('-c',  '--conllu', help="CONLLU file")
        parser.add_argument('-o',  '--output', help="merged file")
        return parser.parse_args()
    args = parse_arguments()

    f1 = open(args.brc, 'r') # vert file
    f2 = open(args.conllu, 'r') # conllu file
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
        if not line.startswith('#') and len(line.split('\t'))>6:
            text2[sentence_id].append(line.strip('\n'))
    f1.close()
    f2.close()

    for sentence in range(1, sentence_id):
        if sentence in text2:
            # -2 for skipping length incl. comments, 2 for getting the first word in the sentece
            #print('<!--',len(text2[sentence])-2,text2[sentence][2],'-->')
            for t1, t2 in zip(get_columns(text1[sentence], columns=None), get_columns(text2[sentence], columns=(3,5,6))):
                if t1.startswith('<'):
                    print('\t'.join([t1, '\t'.join(['','',''])]))
                else:
                    if not tokens_match(t1, t2, compareby=(5,1)):
                        print('\t'.join([t1, t2]))
                    else:
                        print('ACHTUNG!!', t1, t2)


if __name__ == '__main__':
    main()
