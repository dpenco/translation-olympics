import nltk

sogou = 0
baidu = 0
google = 0
n = 0
with open('enzhseg.txt','r') as hyp:
    with open('chineseseg.txt','r') as ref:
        while True:
            sogouHyp = hyp.readline().replace(u'\ufeff', '').split()
            if not sogouHyp:
                break
            baiduHyp = hyp.readline().replace(u'\ufeff', '').split()
            googleHyp = hyp.readline().replace(u'\ufeff', '').split()
            reference = ref.readline().replace(u'\ufeff', '').split()
            n += 1
            sogou += nltk.translate.bleu_score.sentence_bleu([reference], sogouHyp)
            baidu += nltk.translate.bleu_score.sentence_bleu([reference], baiduHyp)
            google += nltk.translate.bleu_score.sentence_bleu([reference], googleHyp)
print(sogou/n)
print(baidu/n)
print(google/n)
