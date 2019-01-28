from random import randrange

def randwords(POSs):
    wordlist = []
    for letter in POSs:
        if letter == "V":
            wordlist.append(randword("verb"))
        elif letter == "A":
            wordlist.append(randword("adj"))
        elif letter == "N":
            wordlist.append(randword("noun"))

def randword(POS):
    with open("static/text/%ss.txt" % POS,"r") as fh:
        words = fh.readlines()
    return words[randrange(len(words))].strip()
