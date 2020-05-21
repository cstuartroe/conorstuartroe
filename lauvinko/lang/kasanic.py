from .utils import replacement_suite, option_re, find, inner_markup, flatten, LauvinkoError


class PKForm:
    PK_PRES = ['H', 'M']
    PK_ONSS = ['m', 'n', 'ñ', 'ṅ', 'G', 'p', 't', 'c', 'k', 'K', 'v', 'r', 's', 'y', 'h']
    PK_VOWS = ['ā', 'a', 'i', 'u', 'e', 'o', 'Y', 'W']

    tail_letter = 'q'
    tail_cons = ['t', 'k', 's', 'h']
    wide_cons = ['m', 'G', 't', 'k', 's', 'h', 'r', 'y']
    tail_vows = ['ā', 'i']
    tail_blocking_vows = ['ā', 'u', 'o']
    wide_vows = {'i': 'X', 'u': 'Z'}

    prefix_re = option_re(PK_PRES)
    onset_re = option_re(PK_ONSS)
    vowel_re = option_re(PK_VOWS)

    accent_re = '!'
    syll_re = prefix_re + '?' + onset_re + '?' + vowel_re + accent_re + '?|&'

    modal_prefixes = {"if": "HtiL", "in.order": "kiL", 'thus': 'ivoF', 'after': 'gigi', '$swrf$': 'oN',
                      "not": "hāra", "again": "tere", "want": "eva", "like": "mik", "can": "soN", "must": "nosaL",
                      "very": "kora", "but": "cā"}

    tertiary_aspect_prefixes = {"$pro$": "Mpi", "$exp$": "rāF"}
    topic_agreement_prefixes = {"1.$sg$": "na", "1.$pl$": "ta", "2.$sg$": "iF", "2.$pl$": "eF",
                                "3.$anm$.$sg": "", "3.$anm$.$pl$": "ā", "3.$inm$.$sg$": "sa", "3.$inm$.$pl$": "āsa"}
    topic_case_prefixes = {"$vol$": "", "$dat$": "paN", "$loc$": "posa", "$nltpc$": "eta"}
    secondary_aspect_prefixes = {"in": "iN", "fqnp": "&", "fqpt": "&", "ex": "rāF"}

    all_glossing_prefixes = list(modal_prefixes.keys()) + list(tertiary_aspect_prefixes.keys()) + \
                            list(topic_agreement_prefixes.keys()) + list(topic_case_prefixes.keys())

    def __init__(self, s, secondary_aspect_prefix, other_prefixes=[]):
        self.s = s
        self.secondary_aspect_prefix = secondary_aspect_prefix
        self.set_prefixes(other_prefixes)

    def set_prefixes(self, prefixes):
        self.prefixes = []
        i = 0
        while (i < len(prefixes)) and (prefixes[i] in PKForm.modal_prefixes):
            self.prefixes.append(PKForm.modal_prefixes[prefixes[i]])
            i += 1
        if (i < len(prefixes)) and (prefixes[i] in PKForm.tertiary_aspect_prefixes):
            self.prefixes.append(PKForm.tertiary_aspect_prefixes[prefixes[i]])
            i += 1
        if (i < len(prefixes)) and (prefixes[i] in PKForm.topic_agreement_prefixes):
            self.prefixes.append(PKForm.topic_agreement_prefixes[prefixes[i]])
            i += 1
        if (i < len(prefixes)) and (prefixes[i] in PKForm.topic_case_prefixes):
            self.prefixes.append(PKForm.topic_case_prefixes[prefixes[i]])
            i += 1
        if i != len(prefixes):
            raise ValueError("Invalid or out of order prefix: " + self.prefixes[i])

        self.prefixes.append(self.secondary_aspect_prefix)
        self.build_structure()
        self.check_accent()

        if 'əi' in self.transcribe() or 'əu' in self.transcribe():
            print("Warning: potentially incorrect root: " + self.transcribe())

    @staticmethod
    def special_chars(word):
        word = str(word)
        orig = word
        replacements = [('[mn]([ptck])', r'M\1'), ('[ptck\']([ptck])', r'H\1'),
                        ('aai', 'Y'), ('aau', 'W'), ('aa', 'ā'), ('ngv', 'G'), ('kv', 'K'), ('ny', 'ñ'), ('ng', 'ṅ'),
                        ('l', 'r'),
                        # stress resolution
                        ('^(%s?%s?%s)' % (PKForm.prefix_re, PKForm.onset_re, PKForm.vowel_re), r'\1!')]
        word = replacement_suite(replacements, word)
        return word

    @staticmethod
    def resolve_prefixes(prefixes, word):
        s = ''.join(prefixes) + word
        replacements = [('&(%s?%s%s)' % (PKForm.prefix_re, PKForm.onset_re, PKForm.vowel_re), r'\1\1'),
                        ('&(%s)(!?)(%s?%s)' % (PKForm.vowel_re, PKForm.prefix_re, PKForm.onset_re), r'\1\3\1\2\3'),
                        ('N([ptckK])', r'M\1'), ('Nv', 'm'), ('Nr', 'n'), ('Ny', 'ñ'),
                        ('N(%s)' % PKForm.vowel_re, r'n\1'), ('N', ''),
                        ('F([ptckK])', r'H\1'), ('Fs', 'c'), ('F', ''),
                        ('LMp', 'm'), ('LMt', 'n'), ('LMc', 's'), ('LMk', 'g'), ('LMK', 'G'),
                        ('Lp', 'v'), ('Lt', 'r'), ('Lc', 's'), ('Lk', 'h'), ('LK', 'v'), ('L', '')]
        return replacement_suite(replacements, s)

    def build_structure(self):
        prelim = PKForm.special_chars(self.s)
        prelim = PKForm.resolve_prefixes(self.prefixes, prelim)
        sylls = re.findall(PKForm.syll_re, prelim)
        if ''.join(sylls) != prelim:
            print(sylls)
            print(prelim)
            raise ValueError("Invalid Proto-Kasanic root: " + s)
        self.structure = [PKForm.parsesyll(syll) for syll in sylls]

    @staticmethod
    def parsesyll(syll):
        prefix = find(PKForm.prefix_re, syll)
        onset = find(PKForm.onset_re, syll)
        vowel = find(PKForm.vowel_re, syll)
        accent = find(PKForm.accent_re, syll)
        return [prefix, onset, vowel, accent]

    def check_accent(self):
        if all(syll[3] != '!' for syll in self.structure):
            raise ValueError()  # self.structure[0][3] = '!'

        for i in range(len(self.structure)):
            if self.structure[i][3] == '!':
                self.accentLocation = copy.copy(i)

    def falavay(self, augment=False):
        falavay_sylls = [PKForm.falavay_syll(syll, augment=augment) for syll in self.structure]
        return ''.join(falavay_sylls)

    @staticmethod
    def falavay_syll(syll, augment=False):
        if syll[1] != '':
            prefix = syll[0]
            out = syll[1]
            tail = PKForm.tail_letter if (
                        syll[1] in PKForm.tail_cons and syll[2] not in PKForm.tail_blocking_vows) else ''
            if syll[2] == 'a':
                pass
            elif syll[2] == 'e':
                out = 'e' + out
            elif syll[2] == 'o':
                out = 'e' + out + 'o'
            elif syll[2] in ['Y', 'W']:
                out = out + tail + syll[2]
                tail = ''
            elif syll[2] in PKForm.wide_vows and syll[1] in PKForm.wide_cons:
                out = out + PKForm.wide_vows[syll[2]]
            else:
                out = out + syll[2]
            out = prefix + out + tail
        else:
            out = syll[2].upper()
            tail = PKForm.tail_letter if syll[2] in PKForm.tail_vows else ''
            out += tail

        replacements = [('A', 'Q'), ('ā', 'a'), ('Ā', 'A'), ('K', 'p'), ('G', 'm'), ('ñ', 'N'), ('ṅ', 'g')]
        out = replacement_suite(replacements, out)

        if syll[3] == '!' and augment:
            out += 'K' + PKForm.tail_letter

        return out

    def transcribe(self):
        flattened = ''.join(flatten(self.structure))
        replacements = [('Y', 'āi'), ('W', 'āu'), ('H', '\''), ('K', 'kv'), ('G', 'ṅv'), ('Mp', 'mp'), ('Mt', 'nt'),
                        ('Mc', 'ñc'), ('Mk', 'ṅk'), ('!', ''), ('a', 'ə'), ('ā', 'a')]
        return replacement_suite(replacements, flattened)

    def alphabetical(self):
        classical = self.transcribe()
        # I'm using "z" to send digraphs and accented letters to after the related letter, e.g. to send "ā" after "a"
        replacements = [("āi", "azy"), ("āu", "azz"), ("ā", "azx"), ("'p", "pz"), ("'t", "tz"), ("'c", "cz"),
                        ("'k", "kz"), ("mp", "mz"), ("nt", "nv"), ("ñc", "nx"), ("ṅk", "nz"), ("ñ", "nw"), ("ṅ", "ny")]
        return replacement_suite(replacements, classical)

    def generate_lauvinko(self):
        self.lauvinko_form = LauvinkoForm.from_pk(self)

    def to_json(self):
        return {"falavay": self.falavay(), "transcription": self.transcribe()}


class PKWord:
    categories = {"fientive": ["imnp", "impt", "pf", "in", "fqnp", "fqpt", "ex"],
                  "punctual": ["np", "pt", "fqnp", "fqpt", "ex"],
                  "stative": ["gn", "pt", "in", "ex"], "uninflected": ["gn"]}
    citation_forms = {"fientive": "imnp", "punctual": "np", "stative": "gn", "uninflected": "gn"}
    low_ablauts = {"np": "e", "pt": "o", "imnp": "aa", "impt": "o", "pf": "e", "in": "aa", "fqnp": "e", "fqpt": "o",
                   "ex": "o"}
    high_ablauts = {"np": "i", "pt": "u", "imnp": "a", "impt": "u", "pf": "i", "in": "a", "fqnp": "i", "fqpt": "u",
                    "ex": "u"}

    def __init__(self, category, prefixes=[]):
        if category in PKWord.categories:
            self.category = category
        else:
            raise ValueError("Invalid word category: " + category)
        self.prefixes = prefixes
        self.forms = {}
        self.citation_form = PKWord.citation_forms[self.category]
        self.defn = 'Not defined.'

    def set_defn(self, s):
        self.defn = s

    def set_general(self, word):
        if self.category in ['fientive', 'punctual']:
            try:
                assert ('@' in word or '~' in word)
            except AssertionError:
                raise ValueError("%s general form must include ablaut vowel: %s" % (self.category.title(), word))

        for form_name in PKWord.categories[self.category]:
            if form_name in self.forms:
                raise ValueError("Please declare general forms first.")
            self.put_form(form_name, word)

    def put_form(self, form_name, word):
        if self.category in ["stative", "uninflected"] and form_name in ["gn", "in"]:
            word_form = re.sub("[@~]", "", word)
        else:
            if re.search("@[aeiuo]{1,3}", word):
                word_form = re.sub("@[aeiuo]{1,3}", PKWord.low_ablauts[form_name], word)
            elif re.search("~[aeiuo]{1,3}", word):
                word_form = re.sub("~[aeiuo]{1,3}", PKWord.high_ablauts[form_name], word)
            elif "@" in word:
                word_form = word.replace("@", PKWord.low_ablauts[form_name])
            elif "~" in word:
                word_form = word.replace("~", PKWord.high_ablauts[form_name])
            else:
                raise ValueError(form_name + " form must have archiphoneme but doesn't: " + word)
        secondary_aspect_prefix = PKForm.secondary_aspect_prefixes.get(form_name, "")
        form_obj = PKForm(word_form, secondary_aspect_prefix=secondary_aspect_prefix, other_prefixes=self.prefixes)
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
                    lemma.put_form(form_name, word)
            elif subtag.tag == "defn":
                lemma.set_defn(inner_markup(subtag))
            else:
                raise ValueError("Invalid tag: " + subtag.tag)
        if lemma.defn == 'Not defined.':
            raise ValueError("AAAAAHHH")
        return lemma

    def to_json(self):
        output = {"definition": self.defn, "forms": {}}
        for name, form in self.forms.items():
            output["forms"][name] = form.to_json()
        return output