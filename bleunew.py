import nltk

total = 0
n = 0
with open('baiduseg.txt','r') as hyp:
    with open('chineseseg.txt','r') as ref:
        while True:
            ourHyp = hyp.readline().replace(u'\ufeff', '').split()
            if not ourHyp:
                break
            reference = ref.readline().replace(u'\ufeff', '').split()
            if not reference:
                break
            n += 1
            total += nltk.translate.bleu_score.sentence_bleu([reference], ourHyp)
print(total/n)
