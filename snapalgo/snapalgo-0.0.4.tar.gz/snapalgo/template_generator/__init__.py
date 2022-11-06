import pyperclip

def union_find():
    union_find_code = ""
    with open('./union_find.py', 'r') as f:
        union_find_code = f.read()

    f.close()
    pyperclip.copy(union_find_code)
    return union_find_code


def trie():
    trie_code = ""
    with open('./trie.py', 'r') as f:
        trie_code = f.read()

    f.close()
    pyperclip.copy(trie_code)
    return trie_code


