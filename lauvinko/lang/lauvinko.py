import re
from copy import deepcopy

from .utils import replacement_suite, option_re, find, flatten, LauvinkoError
from .kasanic import PKLemma, PKForm, stem_categories
from .kasanic import preonset_re as pk_preonset_re
from .kasanic_descendant import KasanicDescendantForm, KasanicDescendantLemma


LF_ONSS = ['m', 'n', 'ñ', 'ṅ', 'B', 'D', 'G', 'p', 't', 'c', 'k', 'P', 'T', 'C', 'K', 'v', 'l', 's', 'y', 'h']
LF_VOWS = ['a', 'ə', 'i', 'u', 'e', 'o']
LF_CODS = ['Y', 'U', 'A', 'R', 'M', 'S', 'H']

onset_re = option_re(LF_ONSS)
vowel_re = option_re(LF_VOWS) + '[`´]?'
coda_re = option_re(LF_CODS)
final_subs = {'l': 'R', 'y': 'Y', 'v': 'U', 'm': 'M', 'n': 'M', 'ṅ': 'M', 'p': 'H', 't': 'H', 'k': 'H', 'c': 'Z',
              's': 'S', '': '', 'A': 'a'}
associated_semivowels = {'e': 'y', 'i': 'y', 'o': 'v'}

case_augments = {
    "$vol$": True,
    "$ins$": False,
    "$pat$": False,
    "$dat$": True,
    "$all$": False,
    "$loc$": True,
    "$abl$": False,
    "$prl$": False,
    "$par$": False
}


class LauvinkoForm(KasanicDescendantForm):
    def __init__(self, source_lemma, primary_aspect, prefix_names, augmented=False, structure=None, falavay=None):
        self.augmented = augmented
        KasanicDescendantForm.__init__(self, source_lemma, primary_aspect, prefix_names, structure, falavay)

    @staticmethod
    def syllabify(s):
        sylls = [p[0] for p in
                re.findall('([mnṅBDGptckPTCKvlysh]?[aeio][`´]?([mnṅBDGptckPTCKvlyshA](?=$|[mnṅBDGptckPTCKvlysh]))?)', s)]
        structure = [LauvinkoForm.parsesyll(syll) for syll in sylls]
        if ''.join(flatten(structure)) != s:
            raise ValueError(f"Not al letters captured: {s} {sylls}")
        return structure

    @staticmethod
    def parsesyll(syll):
        onset = find('^[mnṅBDGptckPTCKvlysh]', syll)
        vowel = find('[aeio]', syll)
        accent = find('[`´]', syll)
        coda = find('[mnṅBDGptckPTCKvlyshA]', syll[1:])
        return [onset, vowel, accent, coda]

    def transcribe(self):
        structure_with_codas = []
        for syll in self.structure:
            structure_with_codas.append(syll[:3] + [final_subs[syll[3]]])
        word = ''.join(flatten(structure_with_codas))
        replacements = [('B', 'm'), ('D', 'n'), ('G', 'ṅ'), ('P', 'p'), ('T', 't'), ('C', 'c'), ('K', 'k'), ('ṅ', 'ng'),
                        ('a´', 'á'), ('e´', 'é'), ('i´', 'í'), ('o´', 'ó'), ('a`', 'à'), ('e`', 'è'), ('i`', 'ì'),
                        ('o`', 'ò'),
                        ('Y', 'y'), ('U', 'u'), ('A', 'a'), ('Rl', 'll'), ('R', 'r'), ('S', 's'),
                        ('H([ptcks])', r'\1\1'), ('Hy', 'cy'), ('H', 'h'), ('Zc', 'cc'), ('Z', 's'),
                        ('M([pmv])', r'm\1'), ('M$', 'ng'), ('M', 'n')]
        return replacement_suite(replacements, word)

    @staticmethod
    def from_pk(pkform: PKForm, augmented=False, showprogress=False):
        word = ''.join(flatten(pkform.structure))
        replacements_pre = [('Y!', 'ā!i'), ('W!', 'ā!u'), ('Y', 'āi'), ('W', 'āu'), ('a', 'ə'), ('ā', 'a'), ('r', 'l')]
        word = replacement_suite(replacements_pre, word)

        if showprogress:
            print(word)

        replacements_800s = [('([ei])h([aəeiou])', r'\1y\2'), ('([ou])h([aəeiou])', r'\1v\2'),
                             ('([aəeiou]!?)h', r'\1'), ('K', 'p'), ('G', 'm')]
        word = replacement_suite(replacements_800s, word)

        replacements_900s_non = [('!(%s?%s)a' % (pk_preonset_re, onset_re), r'!\1ə'),
                                 ('!(%s?%s)e' % (pk_preonset_re, onset_re), r'!\1i'),
                                 ('!(%s?%s)o' % (pk_preonset_re, onset_re), r'!\1u')]
        consonant_system = [['p', 't', 'c', 'k'],
                            ['m', 'n', 'ns', 'ṅ'],
                            ['v', 'l', 's', '']]
        for i in range(4):
            replacements_900s_non.append(('!H' + consonant_system[0][i], '´' + consonant_system[0][i]))
            replacements_900s_non.append(('!M' + consonant_system[0][i], '´' + consonant_system[1][i]))
            replacements_900s_non.append(('!' + consonant_system[0][i], '´' + consonant_system[2][i]))
        replacements_900s_non.append(('!', '`'))
        if augmented:
            word = word.replace('!', '´')
        else:
            word = replacement_suite(replacements_900s_non, word)

        if showprogress:
            print(word)

        replacements_1000s = [('([ei])([aəeiou][`´])', r'\1y\2'), ('([ou])([aəeiou][`´])', r'\1v\2'),
                              ('([aə])([aəeiou][`´])', r'\2'),
                              (r'([aəeiou])([`´]?)\1', r'\1\2'), (r'([aəeiou])([`´]?)a', r'\1\2ə'),
                              (r'([aəeiou])([`´]?)e', r'\1\2i'), (r'([aəeiou])([`´]?)o', r'\1\2u'),
                              (r'[əe]([`´]?)i', r'e\1'), (r'[əo]([`´]?)u', r'o\1'), (r'a([`´]?)ə', r'a\1')]
        replacements_1000s *= 3  # a blunt way to ensure compliance
        replacements_1000s.append(('ñ', 'n'))
        word = replacement_suite(replacements_1000s, word)

        if showprogress:
            print(word)

        replacements_1200s = [('^Mp', 'B'), ('^Mt', 'D'), ('^Mc', 'anc'), ('^Mk', 'G'),
                              ('^Hp', 'P'), ('^Ht', 'T'), ('^Hc', 'C'), ('^Hk', 'K'),
                              ('([aou][`´]?)i', r'\1Y'), ('([aei][`´]?)u', r'\1U'),
                              ('([ei][`´]?)ə', r'\1A'), ('([ou])([`´]?)ə', r'o\2A'),
                              ('([YUA])([`´])', r'\2\1'),
                              ('([ei][`´]?)A([HM])', r'\1ya\2'), ('([ou][`´]?)A([HM])', r'\1va\2'),
                              ('Y([HM])', r'ye\1'), ('U([HM])', r'vo\1')]
        word = replacement_suite(replacements_1200s, word)

        if showprogress:
            print(word)

        replacements_1400s = [('ə([`´])', r'e\1'), ('u([`´])', r'o\1'), ('u', 'ə'), ('[ao]$', 'ə'), ('e$', 'i'),
                              ('(%s%s)ə$' % (vowel_re, onset_re), r'\1'),
                              ('(%s)yi$' % vowel_re, r'\1Y'),
                              ('(%s%s)ə(%s%s)' % (vowel_re, onset_re, onset_re,
                                                  vowel_re), r'\1\2'),
                              ('ə', 'a')]
        word = replacement_suite(replacements_1400s, word)

        if showprogress:
            print(word)

        replacements_1500s = [
            # ('y(%s)' % onset_re, r'Y\1'),
            # ('v(%s)' % onset_re, r'U\1'),
            # ('l(%s)' % onset_re, r'R\1'),
            # ('[mnṅ](%s)' % onset_re, r'M\1'),
            # ('[ptk](%s)' % onset_re, r'H\1'),
            # ('[cs](%s)' % onset_re, r'S\1'),
            ('H([ptck])', r'\1\1'), ('Y', 'y'), ('U', 'v'),
            ('Mp', 'mp'), ('M([tc])', r'n\1'), ('Mk', 'ṅk'),
            ('([ei][`´]?)y$', r'\1'),
            ('(o[`´]?)v$', r'\1'),
        ]
        word = replacement_suite(replacements_1500s, word)

        if showprogress:
            print(word)

        return LauvinkoForm.syllabify(word)

    def apply_case(self, case):
        new_form = deepcopy(self)
        if self.augmented != case_augments.get(case):
            raise LauvinkoError(f"{case} case must use a {'' if self.augmented else 'non'}augmented stem.")

        if case in ["$vol$", "$pat$"]:
            pass
        elif case == "$ins$":
            new_form.falavay = new_form.get_falavay() + "kq"
            if new_form.structure[-1][3] == '':
                new_form.structure[-1][3] = 'k'
            else:
                new_form.structure.append([new_form.structure[-1][3], 'a', '', 'k'])
                new_form.structure[-2][3] = ''
        elif case in ["$dat$", "$all$"]:
            new_form.falavay = new_form.get_falavay() + "MIq"
            if new_form.structure[-1][3] == '':
                if new_form.structure[-1][1] in ["a", "o"]:
                    new_form.structure[-1][3] = 'y'
            else:
                new_form.structure.append([new_form.structure[-1][3], 'i', '', ''])
                new_form.structure[-2][3] = ''
        elif case in ["$loc$", "$abl$"]:
            new_form.falavay = new_form.get_falavay() + "U"
            if new_form.structure[-1][3] == '':
                if new_form.structure[-1][1] != 'o':
                    new_form.structure[-1][3] = 'v'
            else:
                new_form.structure.append([new_form.structure[-1][3], 'o', '', ''])
                new_form.structure[-2][3] = ''
        elif case == "$prl$":
            new_form.falavay = new_form.get_falavay() + "mX"
            new_form.structure.append(['m', 'i', '', ''])
        elif case == "$par$":
            new_form.falavay = new_form.get_falavay() + "E"
            if new_form.structure[-1][3] == '':
                new_form.structure.append(['y', 'e', '', ''])
            else:
                new_form.structure.append([new_form.structure[-1][3], 'e', '', ''])
                new_form.structure[-2][3] = ''
        else:
            raise LauvinkoError("Unknown case: " + case)

        return new_form

    @staticmethod
    def join_clitics(*pieces, stress):
        if len(pieces) > 2:
            return LauvinkoForm.join_clitics(LauvinkoForm.join_clitics(*pieces[:2], stress=min(stress, 1)),
                                             *pieces[2:], stress=min(stress-1, 0))

        left_structure = deepcopy(pieces[0].structure)
        right_structure = deepcopy(pieces[1].structure)
        LauvinkoForm.sandhi(left_structure, right_structure)
        LauvinkoForm.destress(right_structure) if stress == 0 else LauvinkoForm.destress(left_structure)

        out = deepcopy(pieces[stress])
        out.structure = left_structure + right_structure
        out.falavay = pieces[0].get_falavay() + pieces[1].get_falavay()
        return out

    @staticmethod
    def destress(structure):
        for syll in structure:
            syll[2] = ''

    @staticmethod
    def sandhi(left_structure, right_structure):
        """Lauvinko has some complicated sandhi rules yo
        """
        if right_structure[0][0] != '':
            return

        if left_structure[-1][3] != '':
            right_structure[0][0] = left_structure[-1][3]
            left_structure[-1][3] = ''
            return

        v1, s1, v2, s2 = left_structure[-1][1], left_structure[-1][2], right_structure[0][1], right_structure[0][2]
        c = right_structure[0][3]

        if s2 == '' and c == '':
            if v2 in 'ei' and  v1 in 'ao':
                left_structure[-1][3] = 'y'
            elif v2 == 'o' and v1 != 'o':
                left_structure[-1][3] = 'v'
            elif v2 == 'a' and v1 != 'a':
                left_structure[-1][3] = 'A'
            del right_structure[0]

        elif v1 in 'ei' and v2 in 'ao':
            right_structure[0][0] = 'y'

        elif v1 == 'o' and v2 != 'o':
            right_structure[0][0] = 'v'

        elif s1 == '':
            if v1 == 'a':
                right_structure[0][0] = left_structure[-1][0]
                del left_structure[-1]
            elif v1 in 'ei':
                assert(v2 in 'ei')
                right_structure[0][0] = left_structure[-1][0]
                del left_structure[-1]
            elif v1 == 'o':
                assert(v2 == 'o')
                right_structure[0][0] = left_structure[-1][0]
                del left_structure[-1]
            else:
                raise ValueError

        else:
            if v1 == 'a':
                if v2 == 'a':
                    raise ValueError("I don't even know what to do here lol")
                else:
                    right_structure[0][0] = associated_semivowels[v2]

            # vowels are either both front or both 'o'
            else:
                if s2 == '':
                    left_structure[-1][3] = right_structure[0][3]
                    del right_structure[0]
                else:
                    right_structure[0][0] = associated_semivowels[v2]


class LauvinkoLemma(KasanicDescendantLemma):
    FORM_CLASS = LauvinkoForm
    HAS_AUGMENT = True

    @staticmethod
    def all_forms(category):
        for aspect in stem_categories[category]:
            for augment in ["au", "na"]:
                yield f"{aspect}.{augment}"

    def update_form(self, label, stem):
        primary_aspect, augment_label = label.split(".")
        if augment_label not in ["au", "na"]:
            raise ValueError
        augment = augment_label == "au"
        if primary_aspect not in stem_categories[self.category]:
            raise ValueError

        form = self.get_form(primary_aspect, [], augment)
        if "phonemic" in stem:
            form.structure = LauvinkoForm.syllabify(stem["phonemic"])
        if "falavay" in stem:
            form.falavay = stem["falavay"]
        self.forms[(primary_aspect, '', augment)] = form

    def to_json(self):
        out = {"definition": self.definition, "forms": {}}
        for primary_aspect in stem_categories[self.category]:
            for augment in [True, False]:
                form = self.get_form(primary_aspect, [], augment)
                out["forms"][f"${primary_aspect}$.{'$au$' if augment else '$na$'}"] = form.to_json()
        return out