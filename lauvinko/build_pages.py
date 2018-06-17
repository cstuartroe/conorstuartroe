from lxml import etree
import lxml.sax
from xml.sax.handler import ContentHandler
from bs4 import BeautifulSoup as bs
import os
from pathlib import Path
from copy import copy

from utils import *

structure = etree.parse('src/structure.xml')

def pprint(tree):
    print(etree.tostring(tree,encoding='utf-8').decode('utf-8'))

def join_nums(numlist,join_char='_'):
    return join_char.join([str(n) for n in numlist])

class LauvinkoPage:
    def __init__(self,location,name,title,pages):
        self.location = location
        self.id = join_nums(location)
        self.name = name
        self.title = title
        self.pages = pages
        self.section_heirarchy = [pages[join_nums(self.location[:i])].name for i in range(1,len(self.location))]
        self.filename = self.name + '.xml'
        self.containing_dir = os.path.join(*(['src','pages'] + self.section_heirarchy))
        full_path = os.path.join(self.containing_dir, self.filename)

        if os.path.isfile(full_path):
            with open(full_path,'r') as fh:
                self.xml = fh.read()
        else:
            if not os.path.exists(self.containing_dir):
                os.makedirs(self.containing_dir)
            open(full_path,'a').close()
            self.xml = ''

    def generate_HTML(self):
        self.html = self.xml
        self.html = '''{% extends 'lauvinko/base.html' %}
{% block content %}
''' + '<h1>%s %s</h1>\n' % (join_nums(self.location,'.'),self.title) + self.html + '''
{% endblock %}'''
        with open(os.path.join('templates','lauvinko',join_nums(self.location) + '.html'),'w') as fh:
            fh.write(self.html)

    def __repr__(self):
        return 'LauvinkoPage(%s,%s,%s,%s)' % (str(self.location),self.name,self.title,str(self.pages))
    
class MyContentHandler(ContentHandler):
    def __init__(self):
        self.location = []
        self.just_closed = False
        self.pages = {}
        self.names = {}

    def startElementNS(self, name, qname, attributes):
        if self.just_closed:
            self.location[-1] += 1
        else:
            self.location.append(1)
        self.just_closed = False

        pagename = attributes[(None,'name')]
        pagetitle = attributes[(None,'title')]
        self.pages[join_nums(self.location)] = LauvinkoPage(copy(self.location),pagename,pagetitle,self.pages)
        self.names[pagename] = join_nums(self.location)

    def endElementNS(self, name, qname):
        if self.just_closed:
            del self.location[-1]
        else:
            pass
        self.just_closed = True

handler = MyContentHandler()
lxml.sax.saxify(structure, handler)
with open('pagenames.py','w') as fh:
    fh.write('pagenames = ' + str(handler.names))
for page in handler.pages.values():
    page.generate_HTML()
