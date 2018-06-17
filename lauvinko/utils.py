import re
import logging

def preprocess(text):
    orig = text
    text = text.replace('aai','Y')
    text = text.replace('aau','W')
    text = text.replace('aa','@')
    text = text.replace('a','~')
    text = text.replace('@','a')

    text = text.replace('ny','d')

    nasalized_cons = ['mp','nt','nc','nk','gk']
    for nc in nasalized_cons:
        if nc in text:
##            if nc == 'nk':
##                logging.warning('Word %s may be improperly formatted.' % orig)
            text = text.replace(nc,'M'+nc[1])

    glottalized_cons = ['pp','tt','cc','kk','\'p','\'t','\'c','\'k']
    for gc in glottalized_cons:
        if gc in text:
##            if gc[0] != '\'':
##                logging.warning('Word %s may be improperly formatted.' % orig)
            text = text.replace(gc,'H'+gc[1])

    return text

def falavay(text,augment=False):
    text = preprocess(text)

    prefixes = ['H','M']
    cons = ['m','n','d','g','p','t','c','k','v','l','s','h']
    vows = ['~','a','i','u','e','o','Y','W']
    tail_letter = 'q'
    tail_cons = ['t','k','s','h']
    tail_vows = ['a','i']
    tail_blocking_vows = ['a','u','o']

    assert(all(letter in prefixes + cons + vows for letter in text))
    
    i = 0
    out = ''
    sylls = re.findall(r'[HM]?[mndgptckvlsh]?[~aiueoYW]',text)

    def process_syll(syll):        
        if len(syll) == 1:
            assert(syll in vows)
            prefix = ''
            tail = tail_letter if syll in tail_vows else ''
            if syll == '~':
                core = 'Q'
            else:
                core = syll.upper()
        else:
            if len(syll) == 3:
                assert(syll[0] in prefixes)
                prefix = syll[0]
                syll = syll[1:]
            else:
                prefix = ''

            assert(len(syll) == 2 and syll[0] in cons and syll[1] in vows)

            
            tail = tail_letter if (syll[0] in tail_cons and syll[1] not in tail_blocking_vows) else ''
            
            if syll[1] == '~':
                core = syll[0]
            elif syll[1] == 'e':
                core = 'e' + syll[0]
            elif syll[1] == 'o':
                core = 'e' + syll[0] + 'o'
            elif syll[1] in ['Y','W']:
                core = syll[0] + tail + syll[1]
                tail = ''
            else:
                core = syll
                
        return prefix + core + tail

    processed_sylls = [process_syll(syll) for syll in sylls]
    if augment:
        processed_sylls.insert(1,'Kq')
    return ''.join(processed_sylls)

def classical(text):
    text = preprocess(text)
    
    replacements = {'a':'ā','~':'a','Y':'āi','W':'āu','d':'ñ','g':'ṅ','H':'\'',
                    'Mp':'mp','Mt':'nt','Mc':'ñc','Mk':'ṅk'}
    for r in replacements:
        text = text.replace(r,replacements[r])

    return text

# tests be below

def run_tests(suite,function,name='Test Suite'):
    errors = 0
    suite_size = len(suite.keys())
    print(name + ':')
    for test in suite:
        desired = suite[test]
        actual = function(test)
        print(test,actual)
        if desired != actual:
            print('Failure!')
            errors += 1
    passed = suite_size - errors
    print('%d of %d tests passed.' % (passed, suite_size))
    print()

falavay_tests = {'maakina':('mākina','maKqkiqn','makiqn'),
                 'oi':('oi','OKqIq','OIq'),
                 'aai':('āi','YKq','Y'),
                 'naatami':('nātami','naKqtqmi','natqmi'),
                 'ku\'kuta':('ku\'kuta','kuKqHkutq','kuHkutq'),
                 'kagka':('kaṅka','kqKqMkq','kqMkq'),
                 'e\'kugi':('e\'kuṅi','EKqHkugi','EHkugi')}

def alltests(word):
    return classical(word), falavay(word,True), falavay(word,False)

run_tests(falavay_tests,alltests,'Lauvinko Tests')
