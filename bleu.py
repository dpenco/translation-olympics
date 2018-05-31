'''
Author: David Penco
Date: 2018-05-26
TODO: use corpus_bleu instead of sentence_bleu
TODO: create a unified workflow for the entire process in one script that can
be run from the terminal
TODO: make the plots all come up in one go instead of having to run repeatedly
TODO: put labels on the plots and add more demarcations to histograms
'''
import nltk
import matplotlib.pyplot as plt
import numpy as np
import scipy

sentences = 99
references = ['' for sentenceIndex in range(sentences)]
sites = {'Baidu': 0, 'Bing': 0, 'Google': 0, 'Sogou': 0, 'Yandex': 0}
for site in sites:
    sites[site] = [0 for sentence in range(sentences)]

with open('newChinese.txt', 'r') as reference:
    sentenceIndex = 0
    for sentence in reference:
        references[sentenceIndex] = sentence.replace(u'\ufeff', '').split()
        sentenceIndex += 1

with open('05-29ChiOut.txt', 'r') as candidate:
    for sentence in candidate:
        processedSentence = sentence.replace(u'\ufeff', '').split()
        if not processedSentence or not processedSentence[0]:
            continue
        if processedSentence[0] in sites:
            site = processedSentence[0]
            sentenceIndex = 0
            continue
        sites[site][sentenceIndex] = nltk.translate.bleu_score.sentence_bleu(references[sentenceIndex], processedSentence)
        sentenceIndex += 1
dataMatrix = np.array([[sites[site], site] for site in sites])
legend = [dataMatrix[siteIndex][1] for siteIndex in range(len(sites))]
with open('results.txt', 'w') as file:
    for siteIndex in range(len(sites)):
        file.write('Statistics for %s:\n\n' % legend[siteIndex])
        file.write('Variance:\n')
        file.write(repr(np.var([dataMatrix[siteIndex][0]])))
        file.write('\nInterquartile Range:\n')
        file.write(repr(scipy.stats.iqr([dataMatrix[siteIndex][0]])))
        file.write('\n')
        for percent in range(0, 110, 10):
            file.write('\n%sth percentile: ' % percent)
            file.write(repr(np.percentile([dataMatrix[siteIndex][0]], percent)))
        file.write('\n\n\n')
        plt.hist([dataMatrix[siteIndex][0]], 20)
        plt.show()
plt.boxplot(np.transpose([dataMatrix[siteIndex][0] for siteIndex in range(len(sites))]))
plt.show()
