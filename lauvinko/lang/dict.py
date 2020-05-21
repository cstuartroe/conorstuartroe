from .utils import replacement_suite, option_re, find, inner_markup, flatten, LauvinkoError
from .kasanic import PKForm, PKWord
from .lauvinko import LauvinkoForm, LauvinkoWord
from .botharu import BotharuForm, BotharuWord


class DictEntry:
    origins = ["kasanic", "sanskrit", "malay", "tamil", "hokkien", "arabic", "portuguese", "dutch", "english"]

    def __init__(self, category, ident, origin):
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

    def new_language(self, language_tag):
        if language_tag.tag == "pk":
            assert (self.origin == "kasanic")
            self.languages["pk"] = PKWord.from_tag(language_tag, self.category)
            self.languages["lv"] = LauvinkoWord.from_pk(self.languages["pk"])
            self.languages["bt"] = BotharuWord.from_pk(self.languages["pk"])
        elif language_tag.tag == "lv":
            self.languages["lv"].update_from_tag(language_tag)
        elif language_tag.tag == "bt":
            self.languages["bt"].update_from_tag(language_tag)

    def from_xml(entry):
        category = entry.get("category")
        ident = entry.get("id")
        origin = entry.get("origin")
        try:
            de = DictEntry(category, ident, origin)
        except ValueError:
            raise ValueError("Fucked up dictionary entry:\n" + etree.tostring(entry, pretty_print=True).decode('utf-8'))
        for language_tag in entry:
            de.new_language(language_tag)
        return de

    def to_json(self):
        output = {"ident": self.ident, "category": self.category, "languages": {}}
        for language in self.languages:
            output["languages"][language] = self.languages[language].to_json()
        return output


class KasanicDictionary:
    def __init__(self):
        self.entries = {}
        dict_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src/dictionary.xml')
        entries_xml = etree.parse(dict_filename).getroot()
        for entry in entries_xml:
            de = DictEntry.from_xml(entry)
            if de.ident in self.entries:
                raise KeyError('Root "%s" has multiple definitions.' % de.ident)
            self.entries[de.ident] = de

    def lookup_stem(self, stem_id):
        if stem_id in self.entries:
            return self.entries[stem_id]
        else:
            raise LauvinkoError("No stem called " + stem_id)


class Gloss:
    def __init__(self, _outline, dictionary, _language="lv"):
        self.outline = _outline
        self.language = _language

        if self.language == "lv":
            self.gloss_lv(dictionary)

    def gloss_lv(self, dictionary):
        self.fields = {"falavay": [], "transcription": [], "morphemes": [], "analysis": []}
        self.fields["analysis"] = self.outline.split(" ")
        self.length = len(self.fields["analysis"])

        for word in self.fields["analysis"]:
            word_falavay = ""
            word_transcription = ""

            morphemes = word.split("-")
            prefixes = []
            i = 0
            while (i < len(morphemes)) and (morphemes[i] in PKForm.all_glossing_prefixes):
                prefixes.append(morphemes[i])
                i += 1

            stem = morphemes[i]
            stem_parts = stem.split(".")
            if len(stem_parts) == 2:
                stem_id, augment = stem_parts
                form = None
            elif len(stem_parts) == 3:
                stem_id, form, augment = stem_parts
                if form[-1] != '$' or form[0] != '$':
                    raise LauvinkoError("Invalid form: " + form)
                else:
                    form = form[1:-1]
            else:
                raise LauvinkoError("Invalid stem: " + stem)

            pk_word = dictionary.lookup_stem(stem_id).languages['pk']

            if augment == "$au$":
                augment = "augmented"
            elif augment == "$na$":
                augment = "nonaugmented"
            else:
                raise LauvinkoError("Invalid augment: " + augment)

            if form is None:
                if pk_word.category == "uninflected":
                    form = "gn"
                else:
                    raise LauvinkoError(stem_id + " is an inflected stem - please provide stem form.")
            else:
                if form not in pk_word.forms:
                    raise LauvinkoError("Stem " + stem_id + " has forms " + ",".join(pk_word.forms.keys()))

            pk_form = pk_word.forms[form]
            pk_form.set_prefixes(prefixes)
            lv_form = LauvinkoForm.from_pk(pk_form)

            word_transcription += lv_form.transcribe(augment)
            word_falavay += lv_form.falavay(augment)

            self.fields['transcription'].append(word_transcription)
            self.fields['falavay'].append(word_falavay)