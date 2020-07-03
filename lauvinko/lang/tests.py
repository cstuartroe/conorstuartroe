import unittest

# from .utils import replacement_suite, option_re, find, inner_markup, flatten, LauvinkoError
from .kasanic import PKLemma, PKForm
from .lauvinko import LauvinkoLemma
# from .botharu import BotharuForm, BotharuWord
from .dict import DictEntry, KasanicDictionary, Gloss

falavay_tests = {
    'maakina': ('makinə', 'maGqkXqn', 'makXqn'),
    'oi': ('oi', 'OGqIq', 'OIq'),
    'aai': ('ai', 'YGq', 'Y'),
    'naatami': ('natəmi', 'naGqtqmX', 'natqmX'),
    "ku'kuta": ("ku'kutə", 'kZGqHkZtq', 'kZHkZtq'),
    'kanka': ('kəṅkə', 'kqGqMkq', 'kqMkq'),
    "e'kungi": ("e'kuṅi", 'EGqHkZgi', 'EHkZgi'),
    'aakaaye': ('akaye', 'AqGqkaey', 'Aqkaey'),
    'kvaau': ('kvau', 'pWGq', 'pW')
}

botharu_tests = {
    'ekaaye': 'yekaye',
    'sehaanaa': 'shaala',
    'roapinku': 'swęęku',
    "co'kvine": 'tlóchile',
    'kunkaai': 'kǫkee',
    "maato'ce": 'mątóche',
    'raseki': 'seechi',
    'haavingaa': 'havąą',
    'Mpaainta': 'pęęti',
    'kasaavi': 'khaavi',
    'mohettu': 'mhwę́ę́du',
    'saampa': 'hąpi'
}


class KasanicTests(unittest.TestCase):
    def test_lv(self):
        for pk_stem, forms in falavay_tests.items():
            pk_lemma = PKLemma("uninflected", pk_stem, "")
            pk_form = PKForm(pk_lemma, "gn")
            self.assertEqual(forms, (pk_form.transcribe(), pk_form.get_falavay(True), pk_form.get_falavay(False)))


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(KasanicTests)
    unittest.TextTestRunner().run(suite)

    print(Gloss("not-pandan.$au$ if-parent.$pt$.$au$=$2hon$.$au$", "lv").to_json())
