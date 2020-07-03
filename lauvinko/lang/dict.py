import json
from copy import deepcopy

from .utils import LauvinkoError
from .kasanic import PKLemma, PKForm, stem_categories, citation_forms
from .lauvinko import LauvinkoLemma, LauvinkoForm, case_augments
from .botharu import BotharuForm, BotharuLemma
from .loanwords import LoanSource

DICTIONARY_FILENAME = 'lauvinko/dictionary.json'

PRONOUN_LABELS = {"$1excl$", "$1incl$", "$2fam$", "$2fml$", "$2hon$", "$3rd$",
                  "$hea$", "$bra$", "$lea$", "$rck$", "$sea$"}

IRREGULAR_PRONOUNS = {
    ("$1excl$.$sg$", "$dat$"): {"falavay": "OGqni", "structure": [['', 'o', '´', ''], ['n', 'i', '', '']]},
    ("$1incl$.$pl$", "$dat$"): {"falavay": "paGqni", "structure": [['p', 'a', '´', ''], ['n', 'i', '', '']]},
    ("$2fam$.$sg$", "$dat$"): {"falavay": "elXGq", "structure": [['l', 'i', '´', '']]},
    ("$2fml$.$pl$", "$dat$"): {"falavay": "yuGqQi", "structure": [['y', 'o', '´', ''], ['v', 'i', '', '']]},
    ("$2hon$", "$dat$"): {"falavay": "naGqMIq", "structure": [['n', 'a', '´', 'y']]},
    ("$3rd$.$sg$", "$dat$"): {"falavay": "liGqn", "structure": [['l', 'i', '´', 'n']]},
    ("$3rd$.$pl$", "$dat$"): {"falavay": "luGqQi", "structure": [['l', 'o', '´', ''], ['v', 'i', '', '']]},
    ("$bra$.$sg$", "$ins$"): {"falavay": "Iqkq", "structure": [['', 'i', '´', 'k']]},
    ("$bra$.$pl$", "$ins$"): {"falavay": "Okq", "structure": [['', 'o', '´', 'k']]},
    ("$lea$.$sg$", "$abl$"): {"falavay": "OtaU", "structure": [['', 'o', '´', ''], ['v', 'o', '', '']]},
}

ORIGIN_LANGUAGES = {
    "kasanic": "pk",
    "sanskrit": "sa",
    "malay": "ms",
    "arabic": "ar",
    "tamil": "ta",
    "hokkien": "hk",
    "portuguese": "pt",
    "dutch": "nl",
    "english": "en"
}


class DictEntry:
    def __init__(self, ident, json_entry):
        self.languages = {}
        self.ident = ident

        if json_entry["category"] in stem_categories:
            self.category = json_entry["category"]
        else:
            raise LauvinkoError("Invalid word category: " + str(json_entry["category"]))

        if json_entry["origin"] in ORIGIN_LANGUAGES:
            self.origin = json_entry["origin"]
        else:
            raise ValueError("Invalid word origin: " + json_entry["origin"])

        if self.origin != "kasanic":
            lang = ORIGIN_LANGUAGES[self.origin]
            loan_lemma = LoanSource(lang, **json_entry["languages"][lang])
            self.languages[lang] = loan_lemma
        else:
            loan_lemma = None

        if "pk" in json_entry["languages"]:
            self.languages["pk"] = PKLemma.from_json(json_entry["languages"]["pk"], self.category)
            self.languages["lv"] = LauvinkoLemma.from_pk(self.languages["pk"])
            self.languages["bt"] = BotharuLemma.from_pk(self.languages["pk"])
            if "lv" in json_entry["languages"]:
                self.languages["lv"].update_from_json(json_entry["languages"]["lv"])
            if "bt" in json_entry["languages"]:
                self.languages["bt"].update_from_json(json_entry["languages"]["bt"])
        else:
            if "lv" in json_entry["languages"]:
                self.languages["lv"] = LauvinkoLemma.generate_from_json(json_entry["languages"]["lv"], loan_lemma,
                                                                        json_entry["category"])
            if "bt" in json_entry["languages"]:
                self.languages["bt"] = LauvinkoLemma.generate_from_json(json_entry["languages"]["bt"], loan_lemma,
                                                                        json_entry["category"])

    def to_json(self):
        output = {"category": self.category, "languages": {}, "origin": self.origin}
        for language in self.languages:
            output["languages"][language] = self.languages[language].to_json()
        output["citation_form"] = f"${citation_forms[self.category]}$"
        return output


class KasanicDictionary:
    def __init__(self):
        self.entries = {}
        with open(DICTIONARY_FILENAME, "r") as fh:
            dictionary_json = json.load(fh)
        for ident, entry in dictionary_json.items():
            self.entries[ident] = DictEntry(ident, entry)

    def lookup_lemma(self, ident):
        if ident in self.entries:
            return self.entries[ident]
        else:
            raise LauvinkoError("No stem called " + ident)

    def to_json(self):
        out = {}
        for ident, entry in self.entries.items():
            out[ident] = entry.to_json()
        return out


TheDictionary = KasanicDictionary()


class Gloss:
    def __init__(self, outline, language="lv"):
        self.language = language
        self.falavay = []
        self.transcription = []
        # self.morphemes = []
        self.outline = outline

        if self.language == "lv":
            self.gloss_lv_sentence()
        elif self.language == "pk":
            self.gloss_pk_sentence()

    def gloss_pk_sentence(self):
        for compound in self.outline.split(" "):
            caps = compound.startswith("^")
            if caps:
                compound = compound[1:]

            words = [Gloss.gloss_pk_word(word) for word in compound.split("=")]
            self.falavay.append(''.join(word.get_falavay() for word in words))
            transcription = '-'.join(word.transcribe() for word in words)
            self.transcription.append(transcription.title() if caps else transcription)

    @staticmethod
    def gloss_pk_word(word):
        morphemes = word.split("-")
        prefix_names = []
        i = 0
        while i < len(morphemes) and morphemes[i] in PKForm.all_glossing_prefixes:
            prefix_names.append(morphemes[i])
            i += 1

        if i == len(morphemes):
            raise LauvinkoError("Cannot locate primary stem: " + word)

        stem = morphemes[i]
        stem_parts = stem.split(".")
        if stem_parts[0] in PRONOUN_LABELS and stem_parts[1] in ["$sg$", "$du$", "$pl$"]:
            stem_parts = [f"{stem_parts[0]}.{stem_parts[1]}"] + stem_parts[2:]

        if len(stem_parts) == 1:
            lemma_id = stem_parts[0]
            primary_aspect = "gn"
        elif len(stem_parts) == 2:
            lemma_id, primary_aspect = stem_parts
            if primary_aspect[-1] != '$' or primary_aspect[0] != '$':
                raise LauvinkoError("Primary aspect must be wrapped in $$: " + primary_aspect)
            else:
                primary_aspect = primary_aspect[1:-1]
        else:
            primary_aspect = None
            raise LauvinkoError("Invalid stem: " + stem)

        pk_lemma = TheDictionary.lookup_lemma(lemma_id).languages['pk']

        if primary_aspect not in stem_categories[pk_lemma.category]:
            raise LauvinkoError(f"Lemma {lemma_id} has no {primary_aspect} form.")

        pk_form = pk_lemma.generate_form(primary_aspect, prefix_names)

        if i + 1 != len(morphemes):
            raise LauvinkoError("Uninterpretable suffixes: " + '-'.join(morphemes[i:]))

        return pk_form

    def gloss_lv_sentence(self):
        for compound in self.outline.split(" "):
            caps = compound.startswith("^")
            if caps:
                compound = compound[1:]

            words = [Gloss.gloss_lv_word(word) for word in compound.split("=")]
            if len(words) == 1:
                form = words[0]
            else:
                if any(compound.split("=")[-1].startswith(pr) for pr in PRONOUN_LABELS):
                    stress = len(compound.split("=")) - 2
                else:
                    stress = len(compound.split("=")) - 1

                form = LauvinkoForm.join_clitics(*words, stress=stress)

            self.falavay.append(form.get_falavay())
            self.transcription.append(form.transcribe().title() if caps else form.transcribe())

    @staticmethod
    def gloss_lv_word(word):
        morphemes = word.split("-")
        prefix_names = []
        i = 0
        while i < len(morphemes) and morphemes[i] in PKForm.all_glossing_prefixes:
            prefix_names.append(morphemes[i])
            i += 1

        if i == len(morphemes):
            raise LauvinkoError("Cannot locate primary stem: " + word)

        stem = morphemes[i]
        stem_parts = stem.split(".")
        if stem_parts[0] in PRONOUN_LABELS and stem_parts[1] in ["$sg$", "$du$", "$pl$"]:
            stem_parts = [f"{stem_parts[0]}.{stem_parts[1]}"] + stem_parts[2:]

        if len(stem_parts) == 1 and stem_parts[0] in case_augments:
            lemma_id = stem_parts[0]
            augment, primary_aspect = "$na$", "gn"
        elif len(stem_parts) == 2:
            lemma_id, augment = stem_parts
            primary_aspect = "gn"
        elif len(stem_parts) == 3:
            lemma_id, primary_aspect, augment = stem_parts
            if primary_aspect[-1] != '$' or primary_aspect[0] != '$':
                raise LauvinkoError("Primary aspect must be wrapped in $$: " + primary_aspect)
            else:
                primary_aspect = primary_aspect[1:-1]
        else:
            primary_aspect = None
            raise LauvinkoError("Invalid stem: " + stem)

        lv_lemma = TheDictionary.lookup_lemma(lemma_id).languages['lv']

        if augment == "$au$":
            augment = True
            prefix = False
        elif augment == "$na$":
            augment = False
            prefix = False
        elif augment == "$pre$":
            augment = False
            prefix = True
        else:
            raise LauvinkoError("Invalid augment: " + augment)

        if primary_aspect not in stem_categories[lv_lemma.category]:
            raise LauvinkoError(f"Lemma {lemma_id} has no {primary_aspect} form.")

        lv_form = lv_lemma.get_form(primary_aspect, prefix_names, augment)

        i += 1
        if i == len(morphemes):
            final_form = deepcopy(lv_form)
        elif i + 1 == len(morphemes) and morphemes[i] in case_augments:
            if (lemma_id, morphemes[i]) in IRREGULAR_PRONOUNS:
                new_form = deepcopy(lv_form)
                new_form.structure = IRREGULAR_PRONOUNS[(lemma_id, morphemes[i])]["structure"]
                new_form.falavay = IRREGULAR_PRONOUNS[(lemma_id, morphemes[i])]["falavay"]
                final_form = new_form
            else:
                final_form = lv_form.apply_case(morphemes[i])
        else:
            raise LauvinkoError("Uninterpretable suffixes: " + '-'.join(morphemes[i:]))

        if prefix:
            LauvinkoForm.destress(final_form.structure)

        return final_form

    def to_json(self):
        return {
            "language": self.language,
            "falavay": self.falavay,
            "transcription": self.transcription,
            "outline": self.outline
        }
