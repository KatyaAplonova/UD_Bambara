def pos_count(pos):
    """
    Counts frequency of a POS
    """
    pos_count = 0
    for tree in parsed:
        for word in tree:
            if word[3] == pos:
                pos_count +=1
    return pos_count

pos_count("SCONJ")
