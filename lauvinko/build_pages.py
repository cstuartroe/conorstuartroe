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
        
        self.section_heirarchy = []
        for i in range(1,len(self.location)):
            ancestor = pages[join_nums(self.location[:i])]
            self.section_heirarchy.append(ancestor.name)
        self.section_heirarchy.append(self.name)
        
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

        if self.xml == '':
            self.xml = '<p>Unfortunately, this page still hasn\'t been written :(</p>'

    def link(self,leading_text):
        return '<a href="/lauvinko/%s">%s %s %s</a>' % (self.name,leading_text,join_nums(self.location,'.'),self.title)

    def add_child(self,other):
        self.children.append(other)

    def generate_HTML(self):
        self.html = self.xml

        if self.parent:
            go_up = '<p class="go-up">%s</p>\n' % self.parent.link('Go up to ')
        else:
            go_up = '<p class="go-up"><a href="/lauvinko">Go up to index page</a></p>\n'
        self.html = go_up + self.html
        
        header = '<h1>%s %s</h1>\n' % (join_nums(self.location,'.'),self.title)
        self.html = header + self.html

        if len(self.children) > 0:
            go_down = '<div class="row">\n'
            col_sizes = {1:(12,12),2:(6,6),3:(4,4),4:(6,3),5:(4,4),6:(4,4)}
            for child in self.children:
                go_down += '<a href="/lauvinko/%s">' % child.name
                go_down += '<div class="go-down col-xs-%d col-md-%d">' % (col_sizes[len(self.children)][0],col_sizes[len(self.children)][1])
                go_down += '<div><h3>' 
                go_down += '%s %s' % (join_nums(child.location,'.'),child.title)
                go_down += '</h3></div></div></a>\n'
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
        self.build_dictionary()

    def startElementNS(self, name, qname, attributes):
        if qname=="section":
            pagename = attributes[(None,'name')]
            try:
                pagetitle = attributes[(None,'title')]
            except KeyError:
                pagetitle = titleize(pagename)

            self.add_page(pagename, pagetitle)
        else:
            assert(qname=="xml" and self.location==[])

    def add_page(self,pagename,pagetitle,self_closing = False):
        if self.just_closed:
            self.location[-1] += 1
        else:
            self.content_ul += '\t'*len(self.location) + '<ul>\n'
            self.location.append(1)
        self.just_closed = False

        newpage = LauvinkoPage(copy.copy(self.location),pagename,pagetitle,self.pages)
        self.pages[join_nums(self.location)] = newpage
        self.pages_in_order.append(newpage)
            
        self.content_ul += '\t'*len(self.location) + '<a href="/lauvinko/%s"><li>%s %s</li></a>\n' % (pagename,join_nums(self.location,'.'),pagetitle)

        if self_closing:
            self.close_page()

    def endElementNS(self, name, qname):
        if qname=="section":
            self.close_page()
        else:
            assert(qname=="xml" and len(self.location)==1)
            self.content_ul += '</ul>'

    def close_page(self):
        if self.just_closed:
            del self.location[-1]
            self.content_ul += '\t'*len(self.location) + '</ul>\n'
        else:
            pass
        self.just_closed = True

    def build_dictionary(self):
        self.dict_entries = {}
        dictionary = etree.parse('src/dictionary.xml').getroot()
        for entry in dictionary:
            de = DictEntry.from_entry(entry)
            if de.ident in self.dict_entries:
                raise KeyError('Root "%s" has multiple definitions.' % de.ident)
            self.dict_entries[de.ident] = de

        entries_alphabetized = list(self.dict_entries.values())
        entries_alphabetized.sort(key = lambda x: x.languages['pk'].get_citation_form().alphabetical())

        dictionary_text = ''

        dictionary_text += '<p>This dictionary has %d entries!</p>\n' % len(entries_alphabetized)
        dictionary_text += """<script>
function toggleshown(table_toggler) {
    var table = $(table_toggler).parent().parent().parent().parent()
    table.toggleClass("notshown")
    if(table_toggler.innerHTML == "Show") {
        table_toggler.innerHTML = "Hide";
    } else {
        table_toggler.innerHTML = "Show";
    }
}
</script>
"""
        
        for entry in entries_alphabetized:
            cf = entry.languages['pk'].get_citation_form()
            dictionary_text += '<div class="entry" id="%s">\n' % entry.ident
            dictionary_text += '<h2 class="lauvinko">%s</h2>\n' % cf.falavay(False)
            dictionary_text += '<h3><span style="font-style:italic;">%s</span>' % cf.classical()
            dictionary_text += ' - %s (%s)</h3>\n' % (cf.defn, entry.category)
            if entry.category != 'uninflected':
                dictionary_text += MyContentHandler.pkform_table(entry)
            dictionary_text += '</div>\n<hr/>\n'
            
        with open('src/pages/dictionary/kasanic_dictionary/kasanic_dictionary.xml','w',encoding='utf-8') as fh:
            fh.write(dictionary_text)

    def pkform_table(entry):
        pkforms = entry.languages['pk'].forms
        out = '<table class="notshown">\n'
        out += '<thead><tr><th colspan="3">Classical Kasanic Inflection - <a onclick="toggleshown(this)">Show</a></th></tr></thead><tbody>\n'
        #tense header
        out += '<tr><td></td><td>Nonpast</td><td>Past</td></tr>\n'
        if entry.category in ['fientive','punctual','stative']:
            #two-tense row
            out += '<tr><td>%s</td>' % ('Perfective' if entry.category == 'punctual' else 'Imperfective')
            if entry.category == 'fientive':
                np = pkforms['im-np']
                pt = pkforms['im-pt']
            elif entry.category == 'punctual':
                np = pkforms['np']
                pt = pkforms['pt']
            elif entry.category == 'stative':
                np = pkforms['gn']
                pt = pkforms['pt']
            out += '<td><span class="lauvinko">%s</span><br/><span style="font-style:italic;">%s</span></td>' % (np.falavay(),np.classical())
            out += '<td><span class="lauvinko">%s</span><br/><span style="font-style:italic;">%s</span></td>' % (pt.falavay(),pt.classical())
            out += '</tr>\n'
        if entry.category == 'fientive':
            #one-tense perfective row
            out += '<tr><td>Perfective</td>'
            out += '<td colspan="2"><span class="lauvinko">%s</span><br/><span style="font-style:italic;">%s</span></td>' % (pkforms['pf'].falavay(),pkforms['pf'].classical())
            out += '</tr>\n'
        if entry.category in ['fientive','punctual']:
            #frequentative row
            out += '<tr><td>Frequentative</td>'
            out += '<td><span class="lauvinko">%s</span><br/><span style="font-style:italic;">%s</span></td>' % (pkforms['fq-np'].falavay(),pkforms['fq-np'].classical())
            out += '<td><span class="lauvinko">%s</span><br/><span style="font-style:italic;">%s</span></td>' % (pkforms['fq-pt'].falavay(),pkforms['fq-pt'].classical())
            out += '</tr>\n'
        if entry.category in ['fientive','stative']:
            #inceptive row
            out += '<tr><td>Inceptive</td>'
            out += '<td colspan="2"><span class="lauvinko">%s</span><br/><span style="font-style:italic;">%s</span></td>' % (pkforms['in'].falavay(),pkforms['in'].classical())
            out += '</tr>\n'
        out += '</tbody></table>\n'
        return out

    def finish_up(self):        
        #build content pages
        for page in self.pages.values():
            page.generate_HTML()

        #build index page
        with open('src/lauvinko_index.xml','r',encoding="utf-8") as fh:
            self.index_page = fh.read()
        self.index_page = self.index_page.replace('<contents/>',self.content_ul)
        self.index_page = django_wrap(self.index_page)
        with open('templates/lauvinko_index.html','w',encoding="utf-8") as fh:
            fh.write(self.index_page)

handler = MyContentHandler()
lxml.sax.saxify(structure, handler)
handler.finish_up()
