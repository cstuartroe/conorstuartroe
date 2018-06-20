import re
import logging
import copy
from lxml import etree

def replacement_suite(replacements,word):
    for replacement_pair in replacements:
        word = word.replace(replacement_pair[0],replacement_pair[1])
    return word

def option_re(l):
    return r'[' + ''.join(l) + ']'

def find(regex,s):
    result = re.findall(regex,s)
    if result == []:
        return ''
    else:
        return result[0]

flatten = lambda l: [item for sublist in l for item in sublist]

class PKForm:
    prefixes = ['H','M']
    onsets = ['m','n','ñ','ṅ','p','t','c','k','v','l','s','y','h']
    vows = ['ā','a','i','u','e','o','Y','W']
    tail_letter = 'q'
    tail_cons = ['t','k','s','h']
    tail_vows = ['ā','i']
    tail_blocking_vows = ['ā','u','o']
    prefix_re = option_re(['H','M'])
    onset_re = option_re(['m','n','ñ','ṅ','p','t','c','k','v','l','s','y','h']) + 'v?'
    vowel_re = option_re(['ā','a','i','u','e','o','Y','W'])
    accent_re = r'!'
    syll_re = r'[HM]?[mnñṅptckvlsyh]?v?[āaiueoYW]!?'
    
##    onsets = ["ṅkv","mp","nt","ñc","ṅk","kv","p","t","c","k","'kv","'p","'t","'c","'k","ṅv","m","n","ñ","ṅ","r","y","v","s","h",'']
##    nuclei = ["āi","āu","ā","a","e","i","o","u"]
##    system = [["mp","nt","ñc","ṅk","ṅkv"],
##              ["p","t","c","k","kv"],
##              ["'p","'t","'c","'k","'kv"],
##              ["m","n","ñ","ṅ","ṅv"],
##              ["v","r","s",'']]
##    vowheights = [["e","o","āi","āu","ā"],
##                  ["i","u","e","o","a"]]

    def __init__(self,s):
        self.structure = PKForm.parse(s)
        self.check_accent()
        
        for i in range(len(self.structure)):
            if self.structure[i][3] == '!':
                self.accentLocation = copy.copy(i)
        #self.non = PKWord.safeEvolve(str(self))
        #self.aug = PKWord.safeEvolve(str(self),False)
        #self.forms = {"Uninflected":self}

        self.defn = ''

    def set_defn(self,s):
        self.defn = s

    def specialChars(word):
        word = str(word)
        replacements = [('aai','Y'),('aau','W'),('aa','ā'),('ny','ñ'),('ng','ṅ'),('l','r')]
        word = replacement_suite(replacements,word)

        nasalized_cons = ['mp','nt','nc','nk']
        for nc in nasalized_cons:
            word = word.replace(nc,'M'+nc[1])

        glottalized_cons = ['pp','tt','cc','kk','\'p','\'t','\'c','\'k']
        for gc in glottalized_cons:
            word = word.replace(gc,'H'+gc[1])

        return word

    def parse(s):
        prelim = PKForm.specialChars(s)
        sylls = re.findall(PKForm.syll_re,prelim)
        return [PKForm.parsesyll(syll) for syll in sylls]

    def parsesyll(syll):
        prefix = find(PKForm.prefix_re,syll)
        onset = find(PKForm.onset_re,syll)
        vowel = find(PKForm.vowel_re,syll)
        accent = find(PKForm.accent_re,syll)
        return [prefix,onset,vowel,accent]

    def check_accent(self):
        if all(syll[3] != '!' for syll in self.structure):
            self.structure[0][3] = '!'

    def falavay(self,augment=False):       
        i = 0
        out = ''
        processed_sylls = [PKForm.process_syll(syll,augment=augment) for syll in self.structure]
        return ''.join(processed_sylls)

    def process_syll(syll,augment=False):        
        if syll[1] != '':
            out = syll[0] + syll[1]
            tail = PKForm.tail_letter if (syll[1] in PKForm.tail_cons and syll[2] not in PKForm.tail_blocking_vows) else ''
            if syll[2] == 'a':
                pass
            elif syll[2] == 'e':
                out = 'e' + out
            elif syll[2] == 'o':
                out = 'e' + out + 'o'
            elif syll[2] in ['Y','W']:
                out = out + tail + syll[2]
                tail = ''
            else:
                out = out + syll[2]
            out += tail
        else:
            out = syll[2].upper()
            tail = PKForm.tail_letter if syll[2] in PKForm.tail_vows else ''
            out += tail

        if syll[3] == '!' and augment:
            out += 'K' + PKForm.tail_letter
    
        replacements = [('A','Q'),('ā','a'),('Ā','A'),('kv','p'),('ṅv','m'),('ñ','N'),('ṅ','g')]
        return replacement_suite(replacements,out)

    def classical(self):
        flattened = ''.join(flatten(self.structure))
        replacements = [('Y','āi'),('W','āu'),('H','\''),('Mp','mp'),('Mt','nt'),('Mc','ñc'),('Mk','ṅk'),('!','')]
        return replacement_suite(replacements,flattened)

    def __str__(self):
        return ''.join(s[0]+s[1]+s[2] + ('!' if s[3] == 'high' else '') for s in self.l)

class PKWord:
    categories = {"fientive":["im-np","im-pt","pf","in","fq-np","fq-pt"],"punctual":["np","pt","fq-np","fq-pt"],
                  "stative":["gn","pt","in"],"uninflected":["gn"]}
    low_ablauts = {"np":"e","pt":"o","im-np":"aa","im-pt":"o","pf":"e","in":"aa","fq-np":"e","fq-pt":"o"}
    high_ablauts = {"np":"i","pt":"u","im-np":"a","im-pt":"u","pf":"i","in":"a","fq-np":"i","fq-pt":"u"}
    prefixes = {"in":"in"}

    def __init__(self, category):
        if category in PKWord.categories:
            self.category = category
        else:
            raise ValueError("Invalid word category: " + category)
        self.forms = {}

    def set_general(self,word,defn):
        if word is None:
            raise ValueError("General form declaration must include word.")
        if defn is None:
            raise ValueError("General form declaration must include definition.")
        
        for form_name in PKWord.categories[self.category]:
            if form_name in self.forms:
                raise ValueError("Please declare general forms first.")
            self.put_form(form_name,word,defn)

    def put_form(self,form_name,word=None,defn=None):
        if word:
            if "@" in word:
                word_form = word.replace("@",PKWord.low_ablauts[form_name])
            elif "~" in word:
                word_form = word.replace("~",PKWord.high_ablauts[form_name])
            else:
                word_form = word
            word_form = PKWord.prefixes.get(form_name,"") + word_form
            form_obj = PKForm(word_form)
            self.forms[form_name] = form_obj
        if defn:
            self.forms[form_name].set_defn(defn)

    def from_tag(language_tag, category):
        lemma = PKWord(category)
        for form in language_tag:
            word = None
            defn = None
            for subtag in form:
                if subtag.tag == "word":
                    word = subtag.text
                elif subtag.tag == "defn":
                    defn = subtag.text
                else:
                    raise ValueError("Invalid form tag: " + subtag.tag)
            form_name = form.get("type")
            if form_name == "gn":
                lemma.set_general(word,defn)
            else:
                lemma.put_form(form_name,word,defn)
        return lemma

class DictEntry:
    origins = ["kasanic","sanskrit","malay","tamil","hokkien","arabic","portuguese","dutch","english"]
    
    def __init__(self,category,ident,origin):
        self.languages = {}
        self.ident = ident
        
        if category in PKWord.categories:
            self.category = category
        else:
            raise ValueError("Invalid word category: " + category)
        
        if origin in DictEntry.origins:
            self.origin = origin
        else:
            raise ValueError("Invalid word origin: " + origin)

    def new_language(self,language_tag):
        if language_tag.tag == "pk":
            assert(self.origin == "kasanic")
            self.languages["pk"] = PKWord.from_tag(language_tag, self.category)

    def from_entry(entry):
        category = entry.get("category")
        ident = entry.get("id")
        origin = entry.get("origin")
        de = DictEntry(category,ident,origin)
        for language_tag in entry:
            de.new_language(language_tag)
        return de

# tests be below

def run_tests(suite,function,name='Test Suite'):
    errors = 0
    suite_size = len(suite.keys())
    print(name + ':')
    for test in suite:
        desired = suite[test]
        actual = function(test)
        print(test,actual)
        if desired != actual:
            print('Failure!')
            errors += 1
    passed = suite_size - errors
    print('%d of %d tests passed.' % (passed, suite_size))
    print()

falavay_tests = {'maakina':('mākina','maKqkiqn','makiqn'),
                 'oi':('oi','OKqIq','OIq'),
                 'aai':('āi','YKq','Y'),
                 'naatami':('nātami','naKqtqmi','natqmi'),
                 'ku\'kuta':('ku\'kuta','kuKqHkutq','kuHkutq'),
                 'kanka':('kaṅka','kqKqMkq','kqMkq'),
                 'e\'kungi':('e\'kuṅi','EKqHkugi','EHkugi'),
                 'aakaaye':('ākāye','AqKqkaey','Aqkaey'),
                 'kvaau':('kvāu','pWKq','pW')}

def alltests(word):
    pk = PKForm(word)
    return pk.classical(), pk.falavay(True), pk.falavay(False)

if __name__ == "__main__":
    run_tests(falavay_tests,alltests,'Lauvinko Tests')
