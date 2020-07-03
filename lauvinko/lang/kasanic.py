import re
from copy import deepcopy

from .utils import replacement_suite, option_re, find, flatten, LauvinkoError

PK_PRES = ['H', 'M']
PK_ONSS = ['m', 'n', 'ñ', 'ṅ', 'G', 'p', 't', 'c', 'k', 'K', 'v', 'r', 's', 'y', 'h']
PK_VOWS = ['ā', 'a', 'i', 'u', 'e', 'o', 'Y', 'W', '@', '~']

tail_letter = 'q'
tail_cons = ['t', 'k', 's', 'h']
wide_cons = ['m', 'G', 't', 'k', 's', 'h', 'r', 'y']
tail_vows = ['ā', 'i']
tail_blocking_vows = ['ā', 'u', 'o']
wide_vows = {'i': 'X', 'u': 'Z'}

preonset_re = option_re(PK_PRES)
onset_re = option_re(PK_ONSS)
vowel_re = option_re(PK_VOWS)

accent_re = '!'
syll_re = preonset_re + '?' + onset_re + '?' + vowel_re + accent_re + '?|&'

stem_categories = {
    "fientive": ["imnp", "impt", "pf", "inc", "fqnp", "fqpt"],
    "punctual": ["np", "pt", "fqnp", "fqpt"],
    "stative": ["gn", "pt", "inc"],
    "uninflected": ["gn"]
}

citation_forms = {
    "fientive": "imnp",
    "punctual": "np",
    "stative": "gn",
    "uninflected": "gn"
}

low_ablauts = {
    "np": "e",
    "pt": "o",
    "imnp": "ā",
    "impt": "o",
    "pf": "e",
    "inc": "ā",
    "fqnp": "e",
    "fqpt": "o"
}

high_ablauts = {
    "np": "i",
    "pt": "u",
    "imnp": "a",
    "impt": "u",
    "pf": "i",
    "inc": "a",
    "fqnp": "i",
    "fqpt": "u"
}


def informal2formal_transcription(stem):
    replacements = [('[mn]([ptck])', r'M\1'), ('[ptck\']([ptck])', r'H\1'),
                    ('aai', 'Y'), ('aau', 'W'), ('aa', 'ā'), ('ngv', 'G'), ('kv', 'K'), ('ny', 'ñ'), ('ng', 'ṅ'),
                    ('l', 'r')]
    return replacement_suite(replacements, stem)


def parsesyll(syll):
    preonset = find(preonset_re, syll)
    onset = find(onset_re, syll)
    vowel = find(vowel_re, syll)
    accent = find(accent_re, syll)
    return [preonset, onset, vowel, accent]


def build_structure(stem, add_accent=True):
    formal_transcription = informal2formal_transcription(stem)

    sylls = re.findall(syll_re, formal_transcription)
    if ''.join(sylls) != formal_transcription:
        print(sylls)
        print(formal_transcription)
        raise ValueError("Invalid Proto-Kasanic root: " + stem)

    sylls = [parsesyll(syll) for syll in sylls]

    if add_accent:
        sylls[0][3] = "!"

    return sylls


class PKPrefix:
    MUTATIONS = {
        "F": {
            ('', 's'): ['', 'c'],
        },
        "L": {
            ('M', 'p'): ['', 'm'],
            ('M', 't'): ['', 'n'],
            ('M', 'c'): ['', 's'],
            ('M', 'k'): ['', 'g'],
            ('M', 'K'): ['', 'G'],
            ('', 'p'): ['', 'v'],
            ('', 't'): ['', 'r'],
            ('', 'c'): ['', 's'],
            ('', 'k'): ['', 'h'],
            ('', 'K'): ['', 'v'],
        },
        "N": {
            ('', 'v'): ('', 'm'),
            ('', 'r'): ('', 'n'),
            ('', 'y'): ('', 'ñ'),
            ('', ''): ('', 'n'),
        }
    }

    def __init__(self, s, mutation=None):
        self.mutation = mutation
        self.structure = build_structure(s, add_accent=False)


for stop in ['p', 't', 'c', 'k', 'K']:
    PKPrefix.MUTATIONS["F"][('', stop)] = ['H', stop]
    PKPrefix.MUTATIONS["N"][('', stop)] = ["M", stop]


secondary_aspect_prefixes = {
    "inc": PKPrefix("i", "N"),
    "fqnp": "&",
    "fqpt": "&"
}


class PKLemma:
    def __init__(self, category, stem, definition, irregular_forms=None):
        if category not in stem_categories:
            raise ValueError("Invalid stem category: " + category)

        self.category = category
        self.structure = build_structure(stem)
        self.definition = definition

        if self.category in ['fientive', 'punctual']:
            if self.structure[0][2] not in '@~':
                raise LauvinkoError("%s general form must include ablaut vowel: %s" % (self.category.title(), stem))

    def generate_form(self, primary_aspect, prefix_names):
        return PKForm(self, primary_aspect, prefix_names)

    def generate_structure(self, primary_aspect):
        assert(primary_aspect in stem_categories[self.category])
        form_structure = deepcopy(self.structure)
        if form_structure[0][2] == "@":
            form_structure[0][2] = low_ablauts[primary_aspect]
        elif form_structure[0][2] == '~':
            form_structure[0][2] = high_ablauts[primary_aspect]
        elif self.category == "stative" and primary_aspect != "gn":
            if form_structure[0][2] in ['a', 'i', 'u']:
                form_structure[0][2] = high_ablauts[primary_aspect]
            else:
                form_structure[0][2] = low_ablauts[primary_aspect]

        secondary_aspect_prefix = secondary_aspect_prefixes.get(primary_aspect, None)
        if secondary_aspect_prefix == "&":
            redup = deepcopy(form_structure[0])
            redup[3] = ''
            if form_structure[0][1] == '':
                form_structure[0][1] = form_structure[1][1]
                form_structure[0][0] = form_structure[1][0]
            form_structure = [redup] + form_structure
        elif secondary_aspect_prefix is not None:
            form_structure = PKForm.resolve_prefix(secondary_aspect_prefix, form_structure)

        return form_structure

    def generate_citation_form(self):
        return PKLemma.generate_form(self, citation_forms[self.category], [])

    @staticmethod
    def from_json(entry, category):
        return PKLemma(category, entry["forms"]["gn"], entry["definition"])

    def to_json(self):
        out = {"definition": self.definition, "forms": {}}
        for primary_aspect in stem_categories[self.category]:
            form = self.generate_form(primary_aspect, [])
            out["forms"][f"${primary_aspect}$"] = form.to_json()
        return out


modal_prefixes = {
    "if": PKPrefix("Hti", "L"),
    "in.order": PKPrefix("ki", "L"),
    "thus": PKPrefix('ivo', 'F'),
    'after': PKPrefix('ṅiṅi'),
    '$swrf$': PKPrefix('o', 'N'),
    'after.$swrf': PKPrefix('ṅio', 'N'),
    "not": PKPrefix("āra"),
    "again": PKPrefix("tere"),
    "want": PKPrefix("eva"),
    "like": PKPrefix("mika"),
    "can": PKPrefix("so", "N"),
    "must": PKPrefix("nosa", "L"),
    "very": PKPrefix("kora"),
    "but": PKPrefix("cā")
}

tertiary_aspect_prefixes = {
    "$pro$": PKPrefix("Mpi"),
    "$exp$": PKPrefix("rā", "F")
}

topic_agreement_prefixes = {
    "$1st$.$sg$": PKPrefix("na"),
    "$1st$.$pl$": PKPrefix("ta"),
    "$2nd$.$sg$": PKPrefix("i", "F"),
    "$2nd$.$pl$": PKPrefix("e", "F"),
    "$3anm$.$sg$": PKPrefix(""),
    "$3anm$.$pl$": PKPrefix("ā"),
    "$3inm$.$sg$": PKPrefix("sa"),
    "$3inm$.$pl$": PKPrefix("āsa")
}

topic_case_prefixes = {
    "$volt$": PKPrefix(""),
    "$datt$": PKPrefix("pa", "N"),
    "$loct$": PKPrefix("posa"),
    "$dep$": PKPrefix("eta")
}


class PKForm:
    all_glossing_prefixes = list(modal_prefixes.keys()) + list(tertiary_aspect_prefixes.keys()) + \
                            list(topic_agreement_prefixes.keys()) + list(topic_case_prefixes.keys())

    def __init__(self, lemma: PKLemma, primary_aspect, prefix_names=None):
        prefixless_structure = lemma.generate_structure(primary_aspect)
        self.structure = PKForm.resolve_prefixes(prefixless_structure, prefix_names)
        self.accentLocation = PKForm.locate_accent(self.structure)

        if 'əi' in self.transcribe() or 'əu' in self.transcribe():
            print("Warning: potentially incorrect root: " + self.transcribe())

    @staticmethod
    def get_prefixes(prefix_names):
        i = 0
        prefixes = []
        while (i < len(prefix_names)) and (prefix_names[i] in modal_prefixes):
            prefixes.append(modal_prefixes[prefix_names[i]])
            i += 1
        if (i < len(prefix_names)) and (prefix_names[i] in tertiary_aspect_prefixes):
            prefixes.append(tertiary_aspect_prefixes[prefix_names[i]])
            i += 1
        if (i < len(prefix_names)) and (prefix_names[i] in topic_agreement_prefixes):
            prefixes.append(topic_agreement_prefixes[prefix_names[i]])
            i += 1
        if (i < len(prefix_names)) and (prefix_names[i] in topic_case_prefixes):
            prefixes.append((topic_case_prefixes[prefix_names[i]]))
            i += 1
        if i != len(prefix_names):
            raise LauvinkoError("Invalid or out of order prefix: " + prefix_names[i])
        return prefixes

    @staticmethod
    def resolve_prefixes(structure, prefix_names=None):
        prefixes = PKForm.get_prefixes(prefix_names or [])
        for prefix in prefixes[::-1]:
            structure = PKForm.resolve_prefix(prefix, structure)
        return structure

    @staticmethod
    def resolve_prefix(prefix, structure):
        if prefix.mutation:
            t = (structure[0][0], structure[0][1])
            structure[0][0], structure[0][1] = PKPrefix.MUTATIONS[prefix.mutation].get(t, t)

        return prefix.structure + structure

    @staticmethod
    def locate_accent(structure):
        accents_found = 0
        accent_location = None

        for i in range(len(structure)):
            if structure[i][3] == '!':
                accents_found += 1
                accent_location = i

        if accents_found != 1:
            raise LauvinkoError(f"Word does not have exactly one accent: {structure}")

        return accent_location

    def get_falavay(self, augment=False):
        falavay_sylls = [PKForm.falavay_syll(syll, augment=augment) for syll in self.structure]
        return ''.join(falavay_sylls)

    @staticmethod
    def falavay_syll(syll, augment=False):
        if syll[1] != '':
            prefix = syll[0]
            out = syll[1]
            tail = tail_letter if (syll[1] in tail_cons and syll[2] not in tail_blocking_vows) else ''
            if syll[2] == 'a':
                pass
            elif syll[2] == 'e':
                out = 'e' + out
            elif syll[2] == 'o':
                out = 'e' + out + 'o'
            elif syll[2] in ['Y', 'W']:
                out = out + tail + syll[2]
                tail = ''
            elif syll[2] in wide_vows and syll[1] in wide_cons:
                out = out + wide_vows[syll[2]]
            else:
                out = out + syll[2]
            out = prefix + out + tail
        else:
            out = syll[2].upper()
            tail = tail_letter if syll[2] in tail_vows else ''
            out += tail

        replacements = [('A', 'Q'), ('ā', 'a'), ('Ā', 'A'), ('K', 'p'), ('G', 'm'), ('ñ', 'N'), ('ṅ', 'g'),
                        ('r', 'l'), ('c', 'j'), ('s', 'x')]
        out = replacement_suite(replacements, out)

        if syll[3] == '!' and augment:
            out += 'G' + tail_letter

        return out

    def transcribe(self):
        flattened = ''.join(flatten(self.structure))
        replacements = [('Y', 'āi'), ('W', 'āu'), ('H', '\''), ('K', 'kv'), ('G', 'ṅv'), ('Mp', 'mp'), ('Mt', 'nt'),
                        ('Mc', 'ñc'), ('Mk', 'ṅk'), ('!', ''), ('a', 'ə'), ('ā', 'a')]
        return replacement_suite(replacements, flattened)

    def to_json(self):
        return {"falavay": self.get_falavay(), "transcription": self.transcribe()}
