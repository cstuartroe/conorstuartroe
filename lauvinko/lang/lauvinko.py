from .utils import replacement_suite, option_re, find, inner_markup, flatten, LauvinkoError
from .kasanic import PKForm, PKWord

LF_ONSS = ['m', 'n', 'ñ', 'ṅ', 'B', 'D', 'G', 'p', 't', 'c', 'k', 'P', 'T', 'C', 'K', 'v', 'l', 's', 'y', 'h']
LF_VOWS = ['a', 'ə', 'i', 'u', 'e', 'o']
LF_CODS = ['Y', 'U', 'A', 'R', 'M', 'S', 'H']


class LauvinkoForm:
    onsets = LF_ONSS
    vows = LF_VOWS
    codas = LF_CODS
    onset_re = option_re(LF_ONSS)
    vowel_re = option_re(LF_VOWS) + '[`´]?'
    coda_re = option_re(LF_CODS)
    final_subs = {'l': 'R', 'y': 'Y', 'v': 'U', 'm': 'M', 'n': 'M', 'ṅ': 'M', 'p': 'H', 't': 'H', 'k': 'H', 'c': 'S',
                  's': 'S'}
    final_subs_reverse = {'Y': 'y', 'U': 'v', 'A': '@'}
    types = {'augmented': 0, 'nonaugmented': 1}

    def __init__(self, augmented, nonaugmented):
        self.words = (LauvinkoForm.syllabify(augmented), LauvinkoForm.syllabify(nonaugmented))

    def syllabify(s):
        if s[-1] in LauvinkoForm.final_subs:
            final = s[-1]
            s = s[:-1] + LauvinkoForm.final_subs[final]
        elif s[-1] in LauvinkoForm.final_subs_reverse:
            final = LauvinkoForm.final_subs_reverse[s[-1]]
        else:
            final = '@'

        sylls = re.findall('[mnṅBDGptckPTCKvlysh]?[aeio][`´]?[YUARMSH]?', s)
        structure = [LauvinkoForm.parsesyll(syll) for syll in sylls]
        return structure, final

    def parsesyll(syll):
        onset = find('[mnṅBDGptckPTCKvlysh]', syll)
        vowel = find('[aeio]', syll)
        accent = find('[`´]', syll)
        coda = find('[YUARMSH]', syll)
        return [onset, vowel, accent, coda]

    def falavay(self, augment=False):
        if augment:
            return self.falavay_forms[0]
        else:
            return self.falavay_forms[1]

    def transcribe(self, type_name="both"):
        if type_name == "both":
            return self.transcribe("augmented") + ", " + self.transcribe("nonaugmented")
        structure = self.words[LauvinkoForm.types[type_name]][0]
        return LauvinkoForm.to_string(structure)

    def to_string(structure):
        word = ''.join(flatten(structure))
        replacements = [('B', 'm'), ('D', 'n'), ('G', 'ṅ'), ('P', 'p'), ('T', 't'), ('C', 'c'), ('K', 'k'), ('ṅ', 'ng'),
                        ('a´', 'á'), ('e´', 'é'), ('i´', 'í'), ('o´', 'ó'), ('a`', 'à'), ('e`', 'è'), ('i`', 'ì'),
                        ('o`', 'ò'),
                        ('Y', 'y'), ('U', 'u'), ('A', 'a'), ('Rl', 'll'), ('R', 'r'), ('S', 's'),
                        ('H([ptcks])', r'\1\1'), ('H', 'h'),
                        ('M([pmv])', r'm\1'), ('M$', 'ng'), ('M', 'n')]
        return replacement_suite(replacements, word)

    def from_pk(pkform, showprogress=False):
        word = ''.join(flatten(pkform.structure))
        replacements_pre = [('Y!', 'ā!i'), ('W!', 'ā!u'), ('Y', 'āi'), ('W', 'āu'), ('a', 'ə'), ('ā', 'a'), ('r', 'l')]
        word = replacement_suite(replacements_pre, word)

        if showprogress:
            print(word)

        replacements_800s = [('([ei])h([aəeiou])', r'\1y\2'), ('([ou])h([aəeiou])', r'\1v\2'),
                             ('([aəeiou]!?)h', r'\1'), ('K', 'p'), ('G', 'm')]
        word = replacement_suite(replacements_800s, word)

        replacements_900s_non = [('!(%s?%s)a' % (PKForm.prefix_re, LauvinkoForm.onset_re), r'!\1ə'),
                                 ('!(%s?%s)e' % (PKForm.prefix_re, LauvinkoForm.onset_re), r'!\1i'),
                                 ('!(%s?%s)o' % (PKForm.prefix_re, LauvinkoForm.onset_re), r'!\1u')]
        consonant_system = [['p', 't', 'c', 'k'],
                            ['m', 'n', 'ns', 'ṅ'],
                            ['v', 'l', 's', '']]
        for i in range(4):
            replacements_900s_non.append(('!H' + consonant_system[0][i], '´' + consonant_system[0][i]))
            replacements_900s_non.append(('!M' + consonant_system[0][i], '´' + consonant_system[1][i]))
            replacements_900s_non.append(('!' + consonant_system[0][i], '´' + consonant_system[2][i]))
        replacements_900s_non.append(('!', '`'))
        augmented = word.replace('!', '´')
        nonaugmented = replacement_suite(replacements_900s_non, word)

        if showprogress:
            print(augmented, nonaugmented)

        replacements_1000s = [('([ei])([aəeiou][`´])', r'\1y\2'), ('([ou])([aəeiou][`´])', r'\1v\2'),
                              ('([aə])([aəeiou][`´])', r'\2'),
                              (r'([aəeiou])([`´]?)\1', r'\1\2'), (r'([aəeiou])([`´]?)a', r'\1\2ə'),
                              (r'([aəeiou])([`´]?)e', r'\1\2i'), (r'([aəeiou])([`´]?)o', r'\1\2u'),
                              (r'[əe]([`´]?)i', r'e\1'), (r'[əo]([`´]?)u', r'o\1'), (r'a([`´]?)ə', r'a\1')]
        replacements_1000s *= 3  # a blunt way to ensure compliance
        replacements_1000s.append(('ñ', 'n'))
        augmented = replacement_suite(replacements_1000s, augmented)
        nonaugmented = replacement_suite(replacements_1000s, nonaugmented)

        if showprogress:
            print(augmented, nonaugmented)

        replacements_1200s = [('^Mp', 'B'), ('^Mt', 'D'), ('^Mc', 'anc'), ('^Mk', 'G'),
                              ('^Hp', 'P'), ('^Ht', 'T'), ('^Hc', 'C'), ('^Hk', 'K'),
                              ('([aou][`´]?)i', r'\1Y'), ('([aei][`´]?)u', r'\1U'),
                              ('([ei][`´]?)ə', r'\1A'), ('([ou])([`´]?)ə', r'o\2A'),
                              ('([YUA])([`´])', r'\2\1'),
                              ('([ei][`´]?)A([HM])', r'\1ya\2'), ('([ou][`´]?)A([HM])', r'\1va\2'),
                              ('Y([HM])', r'ye\1'), ('U([HM])', r'vo\1')]
        augmented = replacement_suite(replacements_1200s, augmented)
        nonaugmented = replacement_suite(replacements_1200s, nonaugmented)

        if showprogress:
            print(augmented, nonaugmented)

        replacements_1400s = [('ə([`´])', r'e\1'), ('u([`´])', r'o\1'), ('u', 'ə'), ('[ao]$', 'ə'), ('e$', 'i'),
                              ('(%s%s)ə$' % (LauvinkoForm.vowel_re, LauvinkoForm.onset_re), r'\1'),
                              ('(%s)yi$' % LauvinkoForm.vowel_re, r'\1Y'),
                              ('(%s%s)ə(%s%s)' % (LauvinkoForm.vowel_re, LauvinkoForm.onset_re, LauvinkoForm.onset_re,
                                                  LauvinkoForm.vowel_re), r'\1\2'),
                              ('ə', 'a')]
        augmented = replacement_suite(replacements_1400s, augmented)
        nonaugmented = replacement_suite(replacements_1400s, nonaugmented)

        if showprogress:
            print(augmented, nonaugmented)

        replacements_1500s = [('y(%s)' % LauvinkoForm.onset_re, r'Y\1'),
                              ('v(%s)' % LauvinkoForm.onset_re, r'U\1'),
                              ('l(%s)' % LauvinkoForm.onset_re, r'R\1'),
                              ('[mnṅ](%s)' % LauvinkoForm.onset_re, r'M\1'),
                              ('[ptk](%s)' % LauvinkoForm.onset_re, r'H\1'),
                              ('[cs](%s)' % LauvinkoForm.onset_re, r'S\1'),
                              ('([ei][`´]?)y$', r'\1'), ('(o[`´]?)v$', r'\1'), ]
        augmented = replacement_suite(replacements_1500s, augmented)
        nonaugmented = replacement_suite(replacements_1500s, nonaugmented)

        if showprogress:
            print(augmented, nonaugmented)

        lvform = LauvinkoForm(augmented, nonaugmented)
        lvform.falavay_forms = (pkform.falavay(True), pkform.falavay(False))
        return lvform

    def to_json(self):
        return {"augmented": {"falavay": self.falavay_forms[0], "transcription": self.transcribe("augmented")},
                "nonaugmented": {"falavay": self.falavay_forms[1], "transcription": self.transcribe("nonaugmented")}}


class LauvinkoWord:
    def __init__(self):
        self.category = None
        self.forms = {}
        self.defn = 'Not defined.'

    def set_defn(self, s):
        self.defn = s

    def put_form(self, form_name, lvform):
        self.forms[form_name] = lvform

    def get_citation_form(self):
        return self.forms[self.citation_form]

    def update_from_tag(self, language_tag):
        for subtag in language_tag:
            ##            if subtag.tag == "form":
            ##                word = subtag.text
            ##                form_name = subtag.get("type")
            ##                if form_name == "gn":
            ##                    lemma.set_general(word)
            ##                else:
            ##                    lemma.put_form(form_name,word)
            if subtag.tag == "defn":
                self.set_defn(inner_markup(subtag))
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

    def to_json(self):
        output = {"definition": self.defn, "forms": {}}
        for name, form in self.forms.items():
            output["forms"][name] = form.to_json()
        return output