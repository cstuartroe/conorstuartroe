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

def correct_HTML_encoding(html):
    soup = bs(html,'lxml')
    return soup.prettify()

def django_wrap(html):
    return '''{% extends 'lauvinko_base.html' %}
{% block content %}
''' + html + '''
{% endblock %}'''

def titleize(name):
    return name.replace('_',' ').title()

class LauvinkoPage:
    def __init__(self,location,name,title,pages):
        self.location = location
        self.name = name
        self.title = title
        self.pages = pages
        
        self.section_heirarchy = [pages[join_nums(self.location[:i])].name for i in range(1,len(self.location))]
        self.children = []
        if len(self.location) > 1:
            self.parent = pages[join_nums(self.location[:-1])]
            self.parent.add_child(self)
        else:
            self.parent = None
        
        self.filename = self.name + '.xml'
        self.containing_dir = os.path.join(*(['src','pages'] + self.section_heirarchy))
        full_path = os.path.join(self.containing_dir, self.filename)

        if os.path.isfile(full_path):
            with open(full_path,'r', encoding="utf-8") as fh:
                self.xml = fh.read()
        else:
            if not os.path.exists(self.containing_dir):
                os.makedirs(self.containing_dir)
            open(full_path,'a').close()
            self.xml = ''

    def link(self,leading_text):
        return '<a href="/lauvinko/%s">%s %s %s</a>' % (self.name,leading_text,join_nums(self.location,'.'),self.title)

    def add_child(self,other):
        self.children.append(other)

    def generate_HTML(self):
        self.html = self.xml

        if self.parent:
            go_up = '<p class="go-up">%s</p>' % self.parent.link('Go up to ')
        else:
            go_up = '<p class="go-up"><a href="/lauvinko">Go up to index page</a></p>'
        self.html = go_up + self.html
        
        header = '<h1>%s %s</h1>\n' % (join_nums(self.location,'.'),self.title)
        self.html = header + self.html

        if len(self.children) > 0:
            go_down = '<div class="row">\n'
            col_sizes = {1:(12,12),2:(6,6),3:(4,4),4:(6,3),5:(4,4),6:(4,4)}
            for child in self.children:
                go_down += '<div class="go-down col-xs-%d col-md-%d"><h3>' % (col_sizes[len(self.children)][0],col_sizes[len(self.children)][1])
                go_down += child.link('')
                go_down += '</h3></div>\n'
            go_down += '</div>\n'
            self.html += go_down
        
        self.html = django_wrap(self.html)
        with open(os.path.join('templates','lauvinko',self.name + '.html'),'w',encoding="utf-8") as fh:
            fh.write(self.html)

    def __repr__(self):
        return 'LauvinkoPage(%s,%s,%s)' % (str(self.location),self.name,self.title)
    
class MyContentHandler(ContentHandler):
    def __init__(self):
        self.location = []
        self.just_closed = False
        self.pages = {}
        self.pages_in_order = []
        self.content_ul = ''

    def startElementNS(self, name, qname, attributes):
        if qname=="section":
            if self.just_closed:
                self.location[-1] += 1
            else:
                self.content_ul += '\t'*len(self.location) + '<ul>\n'
                self.location.append(1)
            self.just_closed = False

            pagename = attributes[(None,'name')]
            try:
                pagetitle = attributes[(None,'title')]
            except KeyError:
                pagetitle = titleize(pagename)

            newpage = LauvinkoPage(copy(self.location),pagename,pagetitle,self.pages)
            self.pages[join_nums(self.location)] = newpage
            self.pages_in_order.append(newpage)
            
            self.content_ul += '\t'*len(self.location) + '<li><a href="/lauvinko/%s">%s %s</a></li>\n' % (pagename,join_nums(self.location,'.'),pagetitle)
        else:
            assert(qname=="xml" and self.location==[])

    def endElementNS(self, name, qname):
        if qname=="section":
            if self.just_closed:
                del self.location[-1]
                self.content_ul += '\t'*len(self.location) + '</ul>\n'
            else:
                pass
            self.just_closed = True
        else:
            assert(qname=="xml" and len(self.location)==1)
            self.content_ul += '</ul>'

    def finish_up(self):
        for page in self.pages.values():
            page.generate_HTML()

        with open('src/lauvinko_index.xml','r',encoding="utf-8") as fh:
            self.index_page = fh.read()
        self.index_page = self.index_page.replace('<contents/>',self.content_ul)
        self.index_page = django_wrap(self.index_page)
        with open('templates/lauvinko_index.html','w',encoding="utf-8") as fh:
            fh.write(self.index_page)

handler = MyContentHandler()
lxml.sax.saxify(structure, handler)
handler.finish_up()
with open('templates/lauvinko_index.html','rb') as fh:
    b = fh.read()
