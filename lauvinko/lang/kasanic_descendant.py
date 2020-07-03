import json

from .utils import flatten, LauvinkoError
from .kasanic import PKLemma, PKForm, citation_forms, stem_categories


class KasanicDescendantForm:
    def __init__(self, source_lemma, primary_aspect, prefix_names, structure=None, falavay=None):
        if structure is None:
            self.source_form = PKForm(source_lemma, primary_aspect, prefix_names)
            self.structure = type(self).from_pk(self.source_form, **(
                {"augmented": self.augmented} if hasattr(self, "augmented") else {}
            ))
        else:
            self.source_form = None
            self.structure = structure
        self.falavay = falavay

    def get_falavay(self):
        return self.falavay or self.source_form.get_falavay(getattr(self, "augmented", None))

    def to_json(self):
        return {"falavay": self.get_falavay(), "transcription": self.transcribe(),
                "phonemic": ''.join(flatten(self.structure))}


class KasanicDescendantLemma:
    FORM_CLASS = None
    HAS_AUGMENT = False

    def __init__(self, category, source_lemma, definition):
        self.category = category
        self.source_lemma = source_lemma
        self.definition = definition
        self.forms = {}

    def get_form(self, primary_aspect, prefix_names=None, augmented=False):
        key = (primary_aspect, '-'.join(prefix_names), augmented)
        if key not in self.forms:
            self.generate_form(primary_aspect, prefix_names, augmented)
        return self.forms[key]

    def generate_form(self, primary_aspect, prefix_names=None, augmented=False):
        self.forms[(
            primary_aspect,
            '-'.join(prefix_names),
            augmented
        )] = type(self).FORM_CLASS(self.source_lemma, primary_aspect, prefix_names,
                                   *([augmented] if type(self).HAS_AUGMENT else []))

    def get_citation_form(self):
        self.get_form(citation_forms[self.category])

    @classmethod
    def generate_from_json(cls, d, source_lemma, category="uninflected"):
        if set(d["forms"].keys()) != set(cls.all_forms(category)):
            raise LauvinkoError(f"Not all forms for {category} given: {json.dumps(d['forms'])}")

        out = cls(category, source_lemma, definition=(d.get("definition") or source_lemma.definition))
        for form_name in d["forms"]:
            if cls.HAS_AUGMENT:
                primary_aspect, augment_label = form_name.split(".")
                augmented = augment_label == "au"
            else:
                primary_aspect, augmented = form_name, False
            out.forms[(
                primary_aspect,
                '-'.join([]),
                augmented
            )] = cls.FORM_CLASS(source_lemma, primary_aspect, [],
                                structure=cls.FORM_CLASS.syllabify(d["forms"][form_name]["phonemic"]),
                                falavay=d["forms"][form_name]["falavay"],
                                **({"augmented": augmented} if cls.HAS_AUGMENT else {}))
        return out

    @staticmethod
    def all_forms(category):
        return stem_categories[category]

    def update_from_json(self, d):
        if "definition" in d:
            self.definition = d["definition"]

        if "forms" in d:
            for label, stem in d["forms"].items():
                self.update_form(label, stem)

    def update_form(self, label, stem):
        raise NotImplementedError

    @classmethod
    def from_pk(cls, pklemma: PKLemma):
        return cls(pklemma.category, pklemma, pklemma.definition)
