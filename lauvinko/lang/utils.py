import re
import copy
import os
from lxml import etree


def replacement_suite(replacements,word):
    for item, replacement in replacements:
        word = re.sub(item, replacement, word)
    return word


def option_re(l):
    return '[' + ''.join(l) + ']'


def find(regex, s):
    result = re.findall(regex, s)
    if result == []:
        return ''
    else:
        return result[0]


def inner_markup(tag):
    whole = etree.tostring(tag).decode('utf-8')
    chop = len(tag.tag) + 2
    inner = whole.strip()[chop:-chop-1]
    return inner


flatten = lambda l: [item for sublist in l for item in sublist]

class LauvinkoError(ValueError):
    def __init__(self, *args, **kwargs):
        super(LauvinkoError, self).__init__(*args, **kwargs)
