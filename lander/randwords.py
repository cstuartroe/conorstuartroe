from random import randrange

def clearseed():
    for i in range(100,200):
        randrange(i)

def genwords(pattern):
    words = ""
    for letter in pattern:
        if letter == "V":
            words += genword("verb")
        elif letter == "A":
            words += genword("adj")
        elif letter == "N":
            words += genword("noun")
        elif letter == "L":
            words += genword("loc")
        elif letter == "P":
            words += genword("person")
        elif letter == "_":
            words += " "
        else:
            words += letter
    return words

def genword(POS):
    with open("static/text/%ss.txt" % POS,"r") as fh:
        words = fh.readlines()
    return words[randrange(len(words))].strip()

PATTERNS = ["V_the_N",
            "the_A_N",
            "the_A_N",
            "V_the_A_N",
            "V_the_N_with_P",
            "V_the_N_in_L",
            "V_the_A_N_in_L",
            "N_N",
            "N,_N,_and_N",
            "P_and_the_N",
            "P_and_the_A_N"]

def randpattern():
    return PATTERNS[randrange(len(PATTERNS))]
