def find_head(word, tree):
    head_id = word[6]
    if head_id == "0":
        return None
    for w in tree:
        if w[0] == head_id:
            return w

count = 0
for tree in parsed:
    for word in tree:
        head = find_head(word, tree)
        if head is not None and head[3] == "VERB":
            count += 1
count
