def dep_count(dep):
    """
    Counts frequency of a dep
    """
    dep_count = 0
    for tree in parsed:
        for word in tree:
            if word[7] == dep:
                dep_count +=1
    return dep_count

dep_count("xcomp")
