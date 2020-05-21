from .utils import replacement_suite, option_re, find, inner_markup, flatten, LauvinkoError
from .kasanic import PKForm, PKWord
from .lauvinko import LauvinkoForm, LauvinkoWord
from .botharu import BotharuForm, BotharuWord
from .dict import DictEntry, KasanicDictionary, Gloss


def run_tests(suite, function, name='Test Suite'):
    errors = 0
    suite_size = len(suite.keys())
    print(name + ':')
    for test in suite:
        desired = suite[test]
        actual = function(test)
        print(test, actual)
        if desired != actual:
            print('Failure!')
            errors += 1
    passed = suite_size - errors
    print('%d of %d tests passed.' % (passed, suite_size))
    print()


falavay_tests = {'maakina': ('makinə', 'maKqkiqn', 'makiqn'),
                 'oi': ('oi', 'OKqIq', 'OIq'),
                 'aai': ('ai', 'YKq', 'Y'),
                 'naatami': ('natəmi', 'naKqtqmi', 'natqmi'),
                 "ku'kuta": ("ku'kutə", 'kuKqHkutq', 'kuHkutq'),
                 'kanka': ('kəṅkə', 'kqKqMkq', 'kqMkq'),
                 "e'kungi": ("e'kuṅi", 'EKqHkugi', 'EHkugi'),
                 'aakaaye':('akaye','AqKqkaey','Aqkaey'),
                 'kvaau':('kvau','pWKq','pW')}

botharu_tests = {'ekaaye':'yekaye','sehaanaa':'shaala','roapinku':'swęęku',"co'kvine":'tlóchile','kunkaai':'kǫkee',"maato'ce":'mątóche',
                 'raseki':'seechi','haavingaa':'havąą','Mpaainta':'pęęti','kasaavi':'khaavi','mohettu':'mhwę́ę́du','saampa':'hąpi'}


def alltests(word):
    pk = PKForm(word)
   # return pk.transcribe(), pk.falavay(True), pk.falavay(False)
    return BotharuForm.from_pk(pk).transcribe()


if __name__ == "__main__":
    run_tests(botharu_tests, alltests, 'Botharu Tests')
