import re

from .utils import replacement_suite, option_re, find, inner_markup, flatten, LauvinkoError
from .kasanic import PKLemma, PKForm, stem_categories
from .kasanic_descendant import KasanicDescendantForm, KasanicDescendantLemma

BT_ONSS = ['m', 'p', 't', 'z', 'c', 'k',
           'M', 'P', 'T', 'Z', 'C', 'K',
           'b', 'd',
           'v', 'l', 'r', 'y',
           's', 'L', 'S', 'h']
BT_GLDS = ['Y', 'W']
BT_VOWS = ['a', 'i', 'u', 'e', 'o']


class BotharuForm(KasanicDescendantForm):
    def syllabify(s):
        sylls = re.findall('[mptzqckMPTZQCKbdwvlrysLSh]?[YW]?[aeiou]~?´?\-?', s)
        structure = [BotharuForm.parsesyll(syll) for syll in sylls]
        if ''.join(flatten(structure)) != s:
            raise ValueError(f"Not al letters captured: {s} {sylls}")
        return structure

    def parsesyll(syll):
        onset = find('^[mptzqckMPTZQCKbdwvlrysSLh]', syll)
        glide = find('[YW]', syll)
        vowel = find('[aeiou]', syll)
        nasalization = find('~', syll)
        accent = find('´', syll)
        length = find('-', syll)
        return [onset, glide, vowel, nasalization, accent, length]

    def transcribe(self):
        return ''.join(BotharuForm.transcribe_syll(syll) for syll in self.structure)

    @staticmethod
    def transcribe_syll(syll):
        out = ''

        onset_transcriptions = {'M': 'mh', 'P': 'ph', 'T': 'th', 'Z': 'tsh', 'z': 'ts', 'Q': 'tlh', 'q': 'tl',
                                'C': 'chh', 'c': 'ch', 'K': 'kh', 'L': 'lh', 'S': 'sh'}
        out += onset_transcriptions.get(syll[0], syll[0])
        out += syll[1].lower()

        ogoneks = {'a': 'ą', 'e': 'ę', 'i': 'į', 'o': 'ǫ', 'u': 'ų'}
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

    @staticmethod
    def from_pk(pkform, showprogress=False):
        word = ''.join(flatten(pkform.structure))
        replacements_pre = [('Y', 'āi'), ('W', 'āu'), ('a', 'ə'), ('ā', 'a'), ('v', 'w'), ('c', 'z'), ('!', '')]
        word = replacement_suite(replacements_pre, word)

        if showprogress:
            print(word)

        replacements_800s = [('n', 'l'), ('([aəeiou]|^)p', r'\1h'), ('s', 'h'), ('h([aəeiou])', r'h\1#'),
                             ('([aəeiou])h', r'\1#h'), ('h', ''),
                             ('([aəeiou])#([aəeiou])(?!#)', r'\1#\2#'), ('([aəeiou])([aəeiou])#', r'\1#\2#')]
        replacements_800s += replacements_800s[-2:]  # a blunt way to ensure compliance
        word = replacement_suite(replacements_800s, word)

        if showprogress:
            print(word)

        replacements_1000s = [('ṅ([aəeiou]#?)', r'ṅ\1~'), ('([aəeiou]#?)ṅ', r'\1~ṅ'), ('ṅ', ''),
                              ('G([aəeiou]#?)', r'G\1~'), ('([aəeiou]#?)G', r'\1~G'), ('G', 'w'),
                              ('([aəeiou]#?)M', r'\1~'), ('M', ''), ('m([aəeiou]#?)', r'm\1~'),
                              ('([aəeiou]#?)~([aəeiou]#?)(?![~#])', r'\1~\2~'),
                              ('([aəeiou]#?)([aəeiou]#?)~', r'\1~\2~'),
                              ('~#', '#~'), ('#+', '#'), ('~+', '~')]
        replacements_1000s += replacements_1000s[-2:]  # a blunt way to ensure compliance
        word = replacement_suite(replacements_1000s, word)

        if showprogress:
            print(word)

        replacements_1100s = [('([mñptzkKryhlw]|^)([ei])', r'\1Y\2'), ('([mñptzkKryhlw]|^)([ou])', r'\1W\2'),
                              ('wW', 'w'), ('yW', 'w'), ('yY', 'y'), ('^Y', 'y'), ('^W', 'w'),
                              ('KW', 'kW'), ('KY', 'kY'), ('K', 'kW'), ('ñY', 'lY'), ('ñW', 'lW'), ('ñ', 'lY')]
        word = replacement_suite(replacements_1100s, word)

        if showprogress:
            print(word)

        replacements_1200s = [('([əiu]#?~?-?)([aəeiou]#?~?)', r'\2-'), ('([aeo]#?~?)-?([aə])(#?~?)', r'a\3-'),
                              ('([aeo]#?~?)-?([ei])(#?~?)', r'e\3-'), ('([aeo]#?~?)-?([ou])(#?~?)', r'o\3-'),
                              ('-+', '-')]
        replacements_1200s = replacements_1200s * 3  # a blunt way to ensure compliance
        word = replacement_suite(replacements_1200s, word)

        if showprogress:
            print(word)

        replacements_1300s = [('zY', 'c'), ('tY', 'c'), ('kY', 'c'), ('hY', 'sY'), ('zW', 'q'), ('wY', 'v')]
        word = replacement_suite(replacements_1300s, word)

        if showprogress:
            print(word)

        replacements_1400s = [('p([WY]?)([aəeiou]#)', r'P\1\2'), ('t([WY]?)([aəeiou]#)', r'T\1\2'),
                              ('z([WY]?)([aəeiou]#)', r'Z\1\2'),
                              ('q([WY]?)([aəeiou]#)', r'Q\1\2'), ('c([WY]?)([aəeiou]#)', r'C\1\2'),
                              ('k([WY]?)([aəeiou]#)', r'K\1\2'),
                              ('m([WY]?)([aəeiou]#)', r'M\1\2'), ('r([WY]?)([aəeiou]#)', r's\1\2'),
                              ('l([WY]?)([aəeiou]#)', r'L\1\2'),
                              ('LY', 'sY'), ('y([aəeiou]#)', r'sY\1'), ('^([aəeiou]#)', r'h\1'), ('#', ''),
                              ('([aəeiou]~?-?)H', r'\1´H'),
                              ('Hp', 'b'), ('Ht', 'd'), ('H', '')]
        word = replacement_suite(replacements_1400s, word)

        if showprogress:
            print(word)

        replacements_1600s = [('ə~', 'a~'), ('i~', 'e~'), ('u~', 'o~'), ('ə', 'i'), ('sY', 'S'), ('Y([ei])', r'\1'),
                              ('W([ou])', r'\1'), ('-´', '´-')]
        word = replacement_suite(replacements_1600s, word)

        if showprogress:
            print(word)

        return BotharuForm.syllabify(word)


class BotharuLemma(KasanicDescendantLemma):
    FORM_CLASS = BotharuForm

    def update_form(self, primary_aspect, stem):
        if primary_aspect not in stem_categories[self.category]:
            raise ValueError

        form = self.get_form(primary_aspect, [])
        form.structure = BotharuForm.syllabify(stem["phonemic"])
        form.falavay = stem["falavay"]
        self.forms[(primary_aspect, '')] = form

    def to_json(self):
        out = {"definition": self.definition, "forms": {}}
        for primary_aspect in stem_categories[self.category]:
            out["forms"][f"${primary_aspect}$"] = self.get_form(primary_aspect, []).to_json()
        return out
