import re
import logging
import copy
from lxml import etree

def replacement_suite(replacements,word):
    for item, replacement in replacements:
        word = re.sub(item, replacement, word)
    return word

def option_re(l):
    return '[' + ''.join(l) + ']'

def find(regex,s):
    result = re.findall(regex,s)
    if result == []:
        return ''
    else:
        return result[0]

flatten = lambda l: [item for sublist in l for item in sublist]

PK_PRES = ['H','M']
PK_ONSS = ['m','n','ñ','ṅ','G','p','t','c','k','K','v','r','s','y','h']
PK_VOWS = ['ā','a','i','u','e','o','Y','W']

class PKForm:
    prefixes = PK_PRES
    onsets = PK_ONSS
    vows = PK_VOWS
    tail_letter = 'q'
    tail_cons = ['t','k','s','h']
    tail_vows = ['ā','i']
    tail_blocking_vows = ['ā','u','o']
    prefix_re = option_re(PK_PRES)
    onset_re = option_re(PK_ONSS)
    vowel_re = option_re(PK_VOWS)
    accent_re = '!'
    syll_re = prefix_re + '?' + onset_re + '?' + vowel_re + accent_re + '?|&'

    def __init__(self,s,prefix=None):
        self.structure = PKForm.parse(s,prefix)
        self.check_accent()
        
        if 'əi' in self.transcribe() or 'əu' in self.transcribe():
            print("Warning: potentially incorrect root: " + self.transcribe())

    def special_chars(word):
        word = str(word)
        orig = word
        replacements = [('[mn]([ptck])',r'M\1'),('[ptck\']([ptck])',r'H\1'),
                        ('aai','Y'),('aau','W'),('aa','ā'),('ngv','G'),('kv','K'),('ny','ñ'),('ng','ṅ'),('l','r'),
                        #stress resolution
                        ('^(%s?%s?%s)' % (PKForm.prefix_re,PKForm.onset_re,PKForm.vowel_re),r'\1!')]
        word = replacement_suite(replacements,word)
        return word

    def resolve_prefix(prefix,word):
        s = prefix + word
        replacements = [('&(%s?%s%s)' % (PKForm.prefix_re,PKForm.onset_re,PKForm.vowel_re),r'\1\1'),
                        ('&(%s)(!?)(%s?%s)' % (PKForm.vowel_re,PKForm.prefix_re,PKForm.onset_re),r'\1\3\1\2\3'),
                        ('N([ptckK])',r'M\1'),('Nv','m'),('Nr','n'),('Ny','ñ'),('N(%s)' % PKForm.vowel_re,r'n\1'),('N',''),
                        ('F([ptckK])',r'H\1'),('Fs','c'),('F','')]
        return replacement_suite(replacements,s)

    def parse(s,prefix=None):
        prelim = PKForm.special_chars(s)
        if prefix:
            prelim = PKForm.resolve_prefix(prefix,prelim)
        sylls = re.findall(PKForm.syll_re,prelim)
        if ''.join(sylls) != prelim:
            print(sylls)
            print(prelim)
            raise ValueError("Invalid Proto-Kasanic root: " + s)
        return [PKForm.parsesyll(syll) for syll in sylls]

    def parsesyll(syll):
        prefix = find(PKForm.prefix_re,syll)
        onset = find(PKForm.onset_re,syll)
        vowel = find(PKForm.vowel_re,syll)
        accent = find(PKForm.accent_re,syll)
        return [prefix,onset,vowel,accent]

    def check_accent(self):
        if all(syll[3] != '!' for syll in self.structure):
            raise ValueError() #self.structure[0][3] = '!'
        
        for i in range(len(self.structure)):
            if self.structure[i][3] == '!':
                self.accentLocation = copy.copy(i)

    def falavay(self,augment=False):       
        i = 0
        out = ''
        falavay_sylls = [PKForm.falavay_syll(syll,augment=augment) for syll in self.structure]
        return ''.join(falavay_sylls)

    def falavay_syll(syll,augment=False):        
        if syll[1] != '':
            prefix = syll[0]
            out = syll[1]
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
            out = prefix + out + tail
        else:
            out = syll[2].upper()
            tail = PKForm.tail_letter if syll[2] in PKForm.tail_vows else ''
            out += tail

        replacements = [('A','Q'),('ā','a'),('Ā','A'),('K','p'),('G','m'),('ñ','N'),('ṅ','g')]
        out = replacement_suite(replacements,out)

        if syll[3] == '!' and augment:
            out += 'K' + PKForm.tail_letter
    
        return out

    def transcribe(self):
        flattened = ''.join(flatten(self.structure))
        replacements = [('Y','āi'),('W','āu'),('H','\''),('K','kv'),('G','ṅv'),('Mp','mp'),('Mt','nt'),('Mc','ñc'),('Mk','ṅk'),('!',''),
                        ('a','ə'),('ā','a')]
        return replacement_suite(replacements,flattened)

    def alphabetical(self):
        classical = self.transcribe()
        # I'm just using "z" to send digraphs and accented letters to after the related letter, i.e. to send "ā" after "a"
        replacements = [("āi","azy"),("āu","azz"),("ā","azx"),("'p","pz"),("'t","tz"),("'c","cz"),("'k","kz"),
                        ("mp","mz"),("nt","nv"),("ñc","nx"),("ṅk","nz"),("ñ","nw"),("ṅ","ny")]
        return replacement_suite(replacements,classical)

    def generate_lauvinko(self):
        self.lauvinko_form = LauvinkoForm.from_pk(self)

##    def __str__(self):
##        return ''.join(s[0]+s[1]+s[2] + ('!' if s[3] == 'high' else '') for s in self.l)

class PKWord:
    categories = {"fientive":["im-np","im-pt","pf","in","fq-np","fq-pt","ex"],"punctual":["np","pt","fq-np","fq-pt","ex"],
                  "stative":["gn","pt","in","ex"],"uninflected":["gn"]}
    citation_forms = {"fientive":"im-np","punctual":"np","stative":"gn","uninflected":"gn"}
    low_ablauts = {"np":"e","pt":"o","im-np":"aa","im-pt":"o","pf":"e","in":"aa","fq-np":"e","fq-pt":"o","ex":"o"}
    high_ablauts = {"np":"i","pt":"u","im-np":"a","im-pt":"u","pf":"i","in":"a","fq-np":"i","fq-pt":"u","ex":"u"}
    prefixes = {"in":"iN","fq-np":"&","fq-pt":"&","ex":"rāF"}

    def __init__(self, category):
        if category in PKWord.categories:
            self.category = category
        else:
            raise ValueError("Invalid word category: " + category)
        self.forms = {}
        self.citation_form = PKWord.citation_forms[self.category]
        self.defn = 'Not defined.'

    def set_defn(self,s):
        self.defn = s

    def set_general(self,word):
        if self.category in ['fientive','punctual']:
            try:
                assert('@' in word or '~' in word)
            except AssertionError:
                raise ValueError("%s general form must include ablaut vowel: %s" % (self.category.title(), word))
        
        for form_name in PKWord.categories[self.category]:
            if form_name in self.forms:
                raise ValueError("Please declare general forms first.")
            self.put_form(form_name,word)

    def put_form(self,form_name,word):
        if "@" in word:
            word_form = word.replace("@",PKWord.low_ablauts[form_name])
        elif "~" in word:
            word_form = word.replace("~",PKWord.high_ablauts[form_name])
        else:
            word_form = word
        prefix = PKWord.prefixes.get(form_name,"")
        form_obj = PKForm(word_form,prefix=prefix)
        self.forms[form_name] = form_obj

    def get_citation_form(self):
        return self.forms[self.citation_form]

    def from_tag(language_tag, category):
        lemma = PKWord(category)
        for subtag in language_tag:
            if subtag.tag == "form":
                word = subtag.text
                form_name = subtag.get("type")
                if form_name == "gn":
                    lemma.set_general(word)
                else:
                    lemma.put_form(form_name,word)
            elif subtag.tag == "defn":
                lemma.set_defn(subtag.text)
            else:
                raise ValueError("Invalid tag: " + subtag.tag)
        if lemma.defn == 'Not defined.':
            raise ValueError("AAAAAHHH")
        return lemma

LF_ONSS = ['m','n','ñ','ṅ','B','D','G','p','t','c','k','P','T','C','K','v','l','s','y','h']
LF_VOWS = ['a','ə','i','u','e','o']
LF_CODS = ['Y','U','A','R','M','S','H']

class LauvinkoForm:
    onsets = LF_ONSS
    vows = LF_VOWS
    codas = LF_CODS
    onset_re = option_re(LF_ONSS)
    vowel_re = option_re(LF_VOWS) + '[`´]?'
    coda_re = option_re(LF_CODS)
    final_subs = {'l':'R','y':'Y','v':'U','m':'M','n':'M','ṅ':'M','p':'H','t':'H','k':'H','c':'S','s':'S'}
    final_subs_reverse = {'Y':'y','U':'v','A':'@'}
    types = {'augmented':0,'nonaugmented':1}

    def __init__(self,augmented,nonaugmented):
        self.words = (LauvinkoForm.syllabify(augmented), LauvinkoForm.syllabify(nonaugmented))

    def syllabify(s):        
        if s[-1] in LauvinkoForm.final_subs:
            final = s[-1]
            s = s[:-1] + LauvinkoForm.final_subs[final]
        elif s[-1] in LauvinkoForm.final_subs_reverse:
            final = LauvinkoForm.final_subs_reverse[s[-1]]
        else:
            final = '@'
            
        sylls = re.findall('[mnṅBDGptckPTCKvlysh]?[aeio][`´]?[YUARMSH]?',s)
        structure = [LauvinkoForm.parsesyll(syll) for syll in sylls]
        return structure,final

    def parsesyll(syll):
        onset = find('[mnṅBDGptckPTCKvlysh]',syll)
        vowel = find('[aeio]',syll)
        accent = find('[`´]',syll)
        coda = find('[YUARMSH]',syll)
        return [onset,vowel,accent,coda]

    def falavay(self,augment=False):
        if augment:
            return self.falavay_forms[0]
        else:
            return self.falavay_forms[1]

    def transcribe(self,type_name="both"):
        if type_name == "both":
            return self.transcribe("augmented") + ", " + self.transcribe("nonaugmented")
        structure = self.words[LauvinkoForm.types[type_name]][0]
        return LauvinkoForm.to_string(structure)

    def to_string(structure):
        word = ''.join(flatten(structure))
        replacements = [('B','m'),('D','n'),('G','ṅ'),('P','p'),('T','t'),('C','c'),('K','k'),('ṅ','ng'),
                        ('a´','á'),('e´','é'),('i´','í'),('o´','ó'),('a`','à'),('e`','è'),('i`','ì'),('o`','ò'),
                        ('Y','y'),('U','u'),('A','a'),('Rl','ll'),('R','r'),('S','s'),
                        ('H([ptcks])',r'\1\1'),('H','h'),
                        ('M([pmv])',r'm\1'),('M$','ng'),('M','n')]
        return replacement_suite(replacements,word)
    
    def from_pk(pkform,showprogress=False):
        word = ''.join(flatten(pkform.structure))        
        replacements_pre = [('Y','āi'),('W','āu'),('a','ə'),('ā','a'),('r','l')]
        word = replacement_suite(replacements_pre, word)

        if showprogress:
            print(word)
        
        replacements_800s = [('([aəeiou]!?)h',r'\1'),('K','p'),('G','m')] #maybe readd ('([ei]!?)h([aəeiou])',r'\1y\2'),('([ou]!?)h([aəeiou])',r'\1v\2'),
        word = replacement_suite(replacements_800s, word)
        
        replacements_900s_non = [('!(%s?%s)a' % (PKForm.prefix_re,LauvinkoForm.onset_re),r'!\1ə'),
                                 ('!(%s?%s)e' % (PKForm.prefix_re,LauvinkoForm.onset_re),r'!\1i'),
                                 ('!(%s?%s)o' % (PKForm.prefix_re,LauvinkoForm.onset_re),r'!\1u')]
        consonant_system = [['p','t','c','k'],
                            ['m','n','ns','ṅ'],
                            ['v','l','s','']]
        for i in range(4):
            replacements_900s_non.append(('!H' + consonant_system[0][i],'´' + consonant_system[0][i]))
            replacements_900s_non.append(('!M' + consonant_system[0][i],'´' + consonant_system[1][i]))
            replacements_900s_non.append(('!' + consonant_system[0][i],'´' + consonant_system[2][i]))
        replacements_900s_non.append(('!','`'))
        augmented = word.replace('!','´')
        nonaugmented = replacement_suite(replacements_900s_non, word)

        if showprogress:
            print(augmented,nonaugmented)
        
        replacements_1000s = [('([ei])([aəeiou][`´])',r'\1y\2'),('([ou])([aəeiou][`´])',r'\1v\2'),('([aə])([aəeiou][`´])',r'\2'),
                             (r'([aəeiou])([`´]?)\1',r'\1\2'),(r'([aəeiou])([`´]?)a',r'\1\2ə'),
                             (r'([aəeiou])([`´]?)e',r'\1\2i'),(r'([aəeiou])([`´]?)o',r'\1\2u'),
                             (r'[əe]([`´]?)i',r'e\1'),(r'[əo]([`´]?)u',r'o\1'),(r'a([`´]?)ə',r'a\1')]
        replacements_1000s *= 3 # a blunt way to ensure compliance
        replacements_1000s.append(('ñ','n'))
        augmented = replacement_suite(replacements_1000s,augmented)
        nonaugmented = replacement_suite(replacements_1000s,nonaugmented)

        if showprogress:
            print(augmented,nonaugmented)

        replacements_1200s = [('^Mp','B'),('^Mt','D'),('^Mc','anc'),('^Mk','G'),
                              ('^Hp','P'),('^Ht','T'),('^Hc','C'),('^Hk','K'),
                              ('([aou][`´]?)i',r'\1Y'),('([aei][`´]?)u',r'\1U'),
                              ('([ei][`´]?)ə',r'\1A'),('([ou])([`´]?)ə',r'o\2A'),
                              ('([YUA])([`´])',r'\2\1'),
                              ('([ei][`´]?)A([HM])',r'\1ya\2'),('([ou][`´]?)A([HM])',r'\1va\2'),
                              ('Y([HM])',r'ye\1'),('U([HM])',r'vo\1')]
        augmented = replacement_suite(replacements_1200s,augmented)
        nonaugmented = replacement_suite(replacements_1200s,nonaugmented)

        if showprogress:
            print(augmented,nonaugmented)
        
        replacements_1400s = [('ə([`´])',r'e\1'),('u([`´])',r'o\1'),('u','ə'),('[ao]$','ə'),('e$','i'),
                              ('(%s%s)ə$' % (LauvinkoForm.vowel_re,LauvinkoForm.onset_re),r'\1'),
                              ('(%s)yi$' % LauvinkoForm.vowel_re,r'\1Y'),
                              ('(%s%s)ə(%s%s)' % (LauvinkoForm.vowel_re,LauvinkoForm.onset_re,LauvinkoForm.onset_re,LauvinkoForm.vowel_re),r'\1\2'),
                              ('ə','a')]
        augmented = replacement_suite(replacements_1400s,augmented)
        nonaugmented = replacement_suite(replacements_1400s,nonaugmented)

        if showprogress:
            print(augmented,nonaugmented)

        replacements_1500s = [('y(%s)' % LauvinkoForm.onset_re, r'Y\1'),
                              ('v(%s)' % LauvinkoForm.onset_re, r'U\1'),
                              ('l(%s)' % LauvinkoForm.onset_re, r'R\1'),
                              ('[mnṅ](%s)' % LauvinkoForm.onset_re, r'M\1'),
                              ('[ptk](%s)' % LauvinkoForm.onset_re, r'H\1'),
                              ('[cs](%s)' % LauvinkoForm.onset_re, r'S\1'),
                              ('([ei][`´]?)y$',r'\1'),('(o[`´]?)v$',r'\1'),]
        augmented = replacement_suite(replacements_1500s,augmented)
        nonaugmented = replacement_suite(replacements_1500s,nonaugmented)

        if showprogress:
            print(augmented,nonaugmented)

        lvform = LauvinkoForm(augmented,nonaugmented)
        lvform.falavay_forms = (pkform.falavay(True),pkform.falavay(False))
        return lvform

class LauvinkoWord:
    def __init__(self):
        self.category = None
        self.forms = {}
        self.defn = 'Not defined.'

    def set_defn(self,s):
        self.defn = s

    def put_form(self,form_name,lvform):
        self.forms[form_name] = lvform

    def get_citation_form(self):
        return self.forms[self.citation_form]

    def update_from_tag(self,language_tag):
        for subtag in language_tag:
##            if subtag.tag == "form":
##                word = subtag.text
##                form_name = subtag.get("type")
##                if form_name == "gn":
##                    lemma.set_general(word)
##                else:
##                    lemma.put_form(form_name,word)
            if subtag.tag == "defn":
                self.set_defn(subtag.text)
            else:
                raise ValueError("Invalid tag: " + subtag.tag)
        if self.defn == 'Not defined.':
            raise ValueError("AAAAAHHH")

    def from_pk(pkword):
        lvword = LauvinkoWord()
        lvword.category = pkword.category
        for form_name, word_form in pkword.forms.items():
            lvword.forms[form_name] = LauvinkoForm.from_pk(word_form)
        lvword.citation_form = PKWord.citation_forms[lvword.category]
        lvword.set_defn(pkword.defn)
        return lvword

BT_ONSS = ['m','p','t','z','c','k',
           'M','P','T','Z','C','K',
           'b','d',
           'v','l','r','y',
           's','L','S','h']
BT_GLDS = ['Y','W']
BT_VOWS = ['a','i','u','e','o']

class BotharuForm:
    def __init__(self,s):
        self.structure = BotharuForm.syllabify(s)

    def syllabify(s):
        sylls = re.findall('[mptzqckMPTZQCKbdwvlrysLSh]?[YW]?[aeiou]~?´?\-?',s)
        structure = [BotharuForm.parsesyll(syll) for syll in sylls]
        if ''.join(flatten(structure)) != s:
            print(structure)
            print(s)
            raise ValueError("Invalid Botharu root: " + s)
        return structure

    def parsesyll(syll):
        onset = find('[mptzqckMPTZQCKbdwvlrysSLh]',syll)
        glide = find('[YW]',syll)
        vowel = find('[aeiou]',syll)
        nasalization = find('~',syll)
        accent = find('´',syll)
        length = find('-',syll)
        return [onset,glide,vowel,nasalization,accent,length]        

    def transcribe(self):
        return ''.join(BotharuForm.transcribe_syll(syll) for syll in self.structure)

    def transcribe_syll(syll):
        out = ''
        
        onset_transcriptions = {'M':'mh','P':'ph','T':'th','Z':'tsh','z':'ts','Q':'tlh','q':'tl','C':'chh','c':'ch','K':'kh','L':'lh','S':'sh'}
        out += onset_transcriptions.get(syll[0],syll[0])
        out += syll[1].lower()

        ogoneks = {'a':'ą','e':'ę','i':'į','o':'ǫ','u':'ų'}
        if syll[3] == '~':
            vow = ogoneks[syll[2]]
        else:
            vow = syll[2]
        if syll[4] == '´':
            vow += '́'
        if syll[5] == '-':
            vow += vow
        out += vow

##        replacements = [('wy','v')]
##        out = replacement_suite(replacements,out)
        
        return out

    def falavay(self):
        return self.falavay_form

    def from_pk(pkform, showprogress=False):
        word = ''.join(flatten(pkform.structure))        
        replacements_pre = [('Y','āi'),('W','āu'),('a','ə'),('ā','a'),('v','w'),('c','z'),('!','')]
        word = replacement_suite(replacements_pre, word)

        if showprogress:
            print(word)

        replacements_800s = [('n','l'),('([aəeiou]|^)p',r'\1h'),('s','h'),('h([aəeiou])',r'h\1#'),('([aəeiou])h',r'\1#h'),('h',''),
                             ('([aəeiou])#([aəeiou])(?!#)',r'\1#\2#'),('([aəeiou])([aəeiou])#',r'\1#\2#')]
        replacements_800s += replacements_800s[-2:] # a blunt way to ensure compliance
        word = replacement_suite(replacements_800s,word)

        if showprogress:
            print(word)

        replacements_1000s = [('ṅ([aəeiou]#?)',r'ṅ\1~'),('([aəeiou]#?)ṅ',r'\1~ṅ'),('ṅ',''),
                              ('G([aəeiou]#?)',r'G\1~'),('([aəeiou]#?)G',r'\1~G'),('G','w'),
                              ('([aəeiou]#?)M',r'\1~'),('M',''),('m([aəeiou]#?)',r'm\1~'),
                             ('([aəeiou]#?)~([aəeiou]#?)(?![~#])',r'\1~\2~'),('([aəeiou]#?)([aəeiou]#?)~',r'\1~\2~'),
                              ('~#','#~'),('#+','#'),('~+','~')]
        replacements_1000s += replacements_1000s[-2:] # a blunt way to ensure compliance
        word = replacement_suite(replacements_1000s,word)

        if showprogress:
            print(word)

        replacements_1100s = [('([mñptzkKryhlw]|^)([ei])',r'\1Y\2'),('([mñptzkKryhlw]|^)([ou])',r'\1W\2'),
                              ('wW','w'),('yW','w'),('yY','y'),('^Y','y'),('^W','w'),
                              ('KW','kW'),('KY','kY'),('K','kW'),('ñY','lY'),('ñW','lW'),('ñ','lY')]
        word = replacement_suite(replacements_1100s,word)

        if showprogress:
            print(word)

        replacements_1200s = [('([əiu]#?~?-?)([aəeiou]#?~?)',r'\2-'),('([aeo]#?~?)-?([aə])(#?~?)',r'a\3-'),
                              ('([aeo]#?~?)-?([ei])(#?~?)',r'e\3-'),('([aeo]#?~?)-?([ou])(#?~?)',r'o\3-'),('-+','-')]
        replacements_1200s = replacements_1200s * 3 # a blunt way to ensure compliance
        word = replacement_suite(replacements_1200s,word)

        if showprogress:
            print(word)

        replacements_1300s = [('zY','c'),('tY','c'),('kY','c'),('hY','sY'),('zW','q'),('wY','v')]
        word = replacement_suite(replacements_1300s,word)

        if showprogress:
            print(word)

        replacements_1400s = [('p([WY]?)([aəeiou]#)',r'P\1\2'),('t([WY]?)([aəeiou]#)',r'T\1\2'),('z([WY]?)([aəeiou]#)',r'Z\1\2'),
                              ('q([WY]?)([aəeiou]#)',r'Q\1\2'),('c([WY]?)([aəeiou]#)',r'C\1\2'),('k([WY]?)([aəeiou]#)',r'K\1\2'),
                              ('m([WY]?)([aəeiou]#)',r'M\1\2'),('r([WY]?)([aəeiou]#)',r's\1\2'),('l([WY]?)([aəeiou]#)',r'L\1\2'),
                              ('LY','sY'),('y([aəeiou]#)',r'sY\1'),('^([aəeiou]#)',r'h\1'),('#',''),('([aəeiou]~?-?)H',r'\1´H'),
                              ('Hp','b'),('Ht','d'),('H','')]
        word = replacement_suite(replacements_1400s,word)

        if showprogress:
            print(word)

        replacements_1600s = [('ə~','a~'),('i~','e~'),('u~','o~'),('ə','i'),('sY','S'),('Y([ei])',r'\1'),('W([ou])',r'\1'),('-´','´-')]
        word = replacement_suite(replacements_1600s,word)

        if showprogress:
            print(word)

        try:
            btform = BotharuForm(word)
        except ValueError:
            print(pkform.transcribe())
            raise ValueError("fuck.")
        btform.falavay_form = pkform.falavay(False)
        return btform

class BotharuWord:
    def __init__(self):
        self.category = None
        self.forms = {}
        self.defn = 'Not defined.'

    def set_defn(self,s):
        self.defn = s

    def put_form(self,form_name,btform):
        self.forms[form_name] = btform

    def get_citation_form(self):
        return self.forms[self.citation_form]

    def update_from_tag(self,language_tag):
        for subtag in language_tag:
##            if subtag.tag == "form":
##                word = subtag.text
##                form_name = subtag.get("type")
##                if form_name == "gn":
##                    lemma.set_general(word)
##                else:
##                    lemma.put_form(form_name,word)
            if subtag.tag == "defn":
                self.set_defn(subtag.text)
            else:
                raise ValueError("Invalid tag: " + subtag.tag)
        if self.defn == 'Not defined.':
            raise ValueError("AAAAAHHH")

    def from_pk(pkword):
        btword = BotharuWord()
        btword.category = pkword.category
        for form_name, word_form in pkword.forms.items():
            if form_name in ['im-np','im-pt','np','pt','pf','gn']:
                btword.forms[form_name] = BotharuForm.from_pk(word_form)
        btword.citation_form = PKWord.citation_forms[btword.category]
        btword.set_defn(pkword.defn)
        return btword

class DictEntry:
    origins = ["kasanic","sanskrit","malay","tamil","hokkien","arabic","portuguese","dutch","english"]
    
    def __init__(self,category,ident,origin):
        self.languages = {}
        self.ident = ident
        
        if category in PKWord.categories:
            self.category = category
        else:
            raise ValueError("Invalid word category: " + str(category))
        
        if origin in DictEntry.origins:
            self.origin = origin
        else:
            raise ValueError("Invalid word origin: " + origin)

    def new_language(self,language_tag):
        if language_tag.tag == "pk":
            assert(self.origin == "kasanic")
            self.languages["pk"] = PKWord.from_tag(language_tag, self.category)
            self.languages["lv"] = LauvinkoWord.from_pk(self.languages["pk"])
            self.languages["bt"] = BotharuWord.from_pk(self.languages["pk"])
        elif language_tag.tag == "lv":
            self.languages["lv"].update_from_tag(language_tag)
        elif language_tag.tag == "bt":
            self.languages["bt"].update_from_tag(language_tag)


    def from_entry(entry):
        category = entry.get("category")
        ident = entry.get("id")
        origin = entry.get("origin")
        try:
            de = DictEntry(category,ident,origin)
        except ValueError:
            raise ValueError("Fucked up dictionary entry:\n" + etree.tostring(entry,pretty_print=True).decode('utf-8'))
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

falavay_tests = {'maakina':('makinə','maKqkiqn','makiqn'),
                 'oi':('oi','OKqIq','OIq'),
                 'aai':('ai','YKq','Y'),
                 'naatami':('natəmi','naKqtqmi','natqmi'),
                 'ku\'kuta':('ku\'kutə','kuKqHkutq','kuHkutq'),
                 'kanka':('kəṅkə','kqKqMkq','kqMkq'),
                 'e\'kungi':('e\'kuṅi','EKqHkugi','EHkugi'),
                 'aakaaye':('akaye','AqKqkaey','Aqkaey'),
                 'kvaau':('kvau','pWKq','pW')}

botharu_tests = {'ekaaye':'yekaye','sehaanaa':'shaala','roapinku':'swęęku',"co'kvine":'tlóchile','kunkaai':'kǫkee',"maato'ce":'mątóche',
                 'raseki':'seechi','haavingaa':'havąą','Mpaainta':'pęęti','kasaavi':'khaavi','mohettu':'mhwę́ę́du','saampa':'hąpi'}

def alltests(word):
    pk = PKForm(word)
##    return pk.transcribe(), pk.falavay(True), pk.falavay(False)
    return BotharuForm.from_pk(pk).transcribe()

if __name__ == "__main__":
    run_tests(botharu_tests,alltests,'Botharu Tests')
