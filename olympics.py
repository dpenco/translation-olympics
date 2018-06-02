'''
Author: David Penco
Date: 2018-05-24
TODO: add selenium wait instead of time.sleep in yandex
TODO: mod the code so it can handle different language pairs, not just Chi-Eng
TODO: this script currently does not do  BLEU calculation or statistical
analysis. Those parts of the project are still in other files, at least for now
'''

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pyperclip
import fileinput
import jieba
import nltk
import matplotlib.pyplot as plt
import numpy as np
import scipy


class WebsiteDictionaries:
    def __init__(self):
        self.url = {'Baidu': 'https://fanyi.baidu.com/', \
        'Bing': 'https://www.bing.com/translator', \
        'Google': 'https://translate.google.com/', \
        'Sogou': 'https://fanyi.sogou.com', \
        'Yandex': 'https://translate.yandex.com/'}

        self.inputBox = {'Baidu': 'baidu_translate_input', 'Bing': 't_sv', \
        'Google': 'source', 'Sogou': 'sogou-translate-input', 'Yandex': \
        'fakeArea'}

        self.output = {}
        for site in self.url:
            self.output[site] = []

        self.tabOrder = {}

        self.properNouns = {'Peter Gregg': '彼得·格雷格', 'Syed Amjad Ali': \
        '赛义德·阿姆贾德·阿里', 'Henrik Amneus': '亨里克·安纽斯', \
        '国际货币基金组织': '货币基金组织', '160条': '一六○条', '（IMF）': '', \
        'GDP': '国内总产值', '国内生产总值': '国内总产值', 'MER': '市场汇率', 'PARES': \
        '价格调整汇率', 'PARE率': '价格调整汇率', 'PAREs': \
        '价格调整汇率', 'PPP': '购买力平价', 'WAs': '世界地图集', \
        '和（或）': '和/或', '亨利. Amneus ': '亨里克·安纽斯'}

        self.moreProperNouns = {'Amneus': '安纽斯', 'IMF': '货币基金组织', 'PARE': \
        '价格调整汇率', 'WA': '世界地图集'}

        self.punctuation = {' ': '', '》': '', '《': '', '.': '。', ',': '，', \
        u'\ufeff': '', '(': '（', ')': '）', '1985和1990': '1985年和1990年', '6000美元': \
        '$6000', '（4）': '', ':': '：', ';': '；', '*': '·', '6 000美元': '$6000', \
        '[4]/': '', '1994 的': '1994年的', '一九八九至九四年': '1989-1994年', '1994的': \
        '1994年的'}

        self.bleuScores = {}
        for site in self.url:
            self.bleuScores[site] = 0

class ChromeDriver:
    def __init__(self):
        self.scrapeEng = input('\nWould you like to input Chinese sentences' + \
        'to the translation websites and scrape their translations into ' + \
        'English? (Y/N)\n\n').upper() == 'Y'
        self.scrapeChi = input('\nWould you like to input English sentences' + \
        'to the translation websites and scrape their translations into ' + \
        'Chinese? (Y/N)\n\n').upper() == 'Y'

        if self.scrapeEng:
            self.chineseInput = input('\n\nPlease enter the name of the file ' +
            'containing the Chinese sentences to translate into English. Ensure' + \
            ' that each sentence is on a separate line in the file:\n')
            self.englishOutput = input('\n\nPlease enter the name of the file where' +
            ' you want to write the English translation output (which comes from' + \
            ' the Chinese sentence input):\n\n')

        if self.scrapeChi:
            self.englishInput = input('\n\nPlease enter the name of the file ' +
            'containing the English sentences to translate into Chinese. Ensure' + \
            ' that each sentence is on a separate line in the file:\n')
            self.chineseOutput = input('\n\nPlease enter the name of the file where' +
            ' you want to write the Chinese translation output (which comes from' + \
            ' the English sentence input):\n\n')

        if not self.scrapeEng:
            self.chineseInput = input('\n\nPlease enter the name of the file ' +
            'containing the Chinese reference sentences for analysis. Ensure' + \
            ' that each sentence is on a separate line in the file:\n')

        if not self.scrapeChi:
            self.englishInput = input('\n\nPlease enter the name of the file ' +
            'containing the English reference sentences for analysis. Ensure' + \
            ' that each sentence is on a separate line in the file:\n')

        if self.scrapeEng or self.scrapeChi:
            chrome_options = Options()
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_experimental_option('prefs', \
            {'intl.accept_languages': 'en-US'})
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
            self.courtesyDelay = 8

        dictionaries = WebsiteDictionaries()
        self.scrapeData(dictionaries)

    def setupChiToEng(self, dictionaries):
        tabNumber = 0
        self.driver.switch_to.window(self.driver.window_handles[0])
        for site in dictionaries.url:
            self.driver.get(dictionaries.url[site])
            if site.capitalize() == 'Baidu':
                self.driver.find_element_by_class_name('select-from-language').click()
                self.driver.find_element_by_xpath('//a[@value="zh"]').click()
                self.driver.find_element_by_class_name('select-to-language').click()
                self.driver.find_element_by_xpath('(//a[@value="en"])[3]').click()
            elif site.capitalize() == 'Bing':
                Select(self.driver.find_element_by_id('t_sl')).select_by_visible_text('Chinese Simplified')
                Select(self.driver.find_element_by_id('t_tl')).select_by_visible_text('English')
            elif site.capitalize() == 'Google':
                self.driver.find_element_by_id('gt-sl-gms').click()
                self.driver.find_element_by_id(':g').click()
                self.driver.find_element_by_id('gt-tl-gms').click()
                self.driver.find_element_by_id(':3j').click()
            elif site.capitalize() == 'Sogou':
                self.driver.find_element_by_xpath('//em[@data-langtype="from"]').click()
                self.driver.find_element_by_xpath('//a[@lang="zh-CHS"]').click()
                self.driver.find_element_by_xpath('//em[@data-langtype="to"]').click()
                self.driver.find_element_by_xpath('//a[@lang="en"][@data-type="to"]').click()
            elif site.capitalize() == 'Yandex':
                self.driver.find_element_by_id('dstLangButton').click()
                time.sleep(0.5)
                self.driver.find_element_by_xpath('(//div[@data-value="en"])[2]').click()
                self.driver.find_element_by_id('srcLangButton').click()
                time.sleep(0.5)
                self.driver.find_element_by_xpath('(//div[@data-value="zh"])').click()
            dictionaries.tabOrder[tabNumber] = site
            if len(self.driver.window_handles) < len(dictionaries.url):
                self.driver.execute_script('window.open(\'about:blank\');')
                self.driver.switch_to.window(self.driver.window_handles[-1])
                tabNumber += 1
        self.driver.switch_to.window(self.driver.window_handles[0])

    def setupEngToChi(self, dictionaries):
        tabNumber = 0
        self.driver.switch_to.window(self.driver.window_handles[0])
        for site in dictionaries.url:
            self.driver.get(dictionaries.url[site])
            if site.capitalize() == 'Baidu':
                self.driver.find_element_by_class_name('select-from-language').click()
                self.driver.find_element_by_xpath('//a[@value="en"]').click()
                self.driver.find_element_by_class_name('select-to-language').click()
                self.driver.find_element_by_xpath('(//a[@value="zh"])[3]').click()
            elif site.capitalize() == 'Bing':
                Select(self.driver.find_element_by_id('t_sl')).select_by_visible_text('English')
                Select(self.driver.find_element_by_id('t_tl')).select_by_visible_text('Chinese Simplified')
            elif site.capitalize() == 'Google':
                self.driver.find_element_by_id('gt-sl-gms').click()
                self.driver.find_element_by_id(':m').click()
                self.driver.find_element_by_id('gt-tl-gms').click()
                self.driver.find_element_by_id(':3c').click()
            elif site.capitalize() == 'Sogou':
                self.driver.find_element_by_xpath('//em[@data-langtype="from"]').click()
                self.driver.find_element_by_xpath('//a[@lang="en"]').click()
                self.driver.find_element_by_xpath('//em[@data-langtype="to"]').click()
                self.driver.find_element_by_xpath('//a[@lang="zh-CHS"][@data-type="to"]').click()
            elif site.capitalize() == 'Yandex':
                self.driver.find_element_by_id('dstLangButton').click()
                time.sleep(0.5)
                self.driver.find_element_by_xpath('(//div[@data-value="zh"])[2]').click()
                self.driver.find_element_by_id('srcLangButton').click()
                time.sleep(0.5)
                self.driver.find_element_by_xpath('(//div[@data-value="en"])').click()
            dictionaries.tabOrder[tabNumber] = site
            if len(self.driver.window_handles) < len(dictionaries.url):
                self.driver.execute_script('window.open(\'about:blank\');')
                self.driver.switch_to.window(self.driver.window_handles[-1])
                tabNumber += 1
        self.driver.switch_to.window(self.driver.window_handles[0])

    def scrapeData(self, dictionaries):
        if self.scrapeEng:
            self.setupChiToEng(dictionaries)
            with open(self.chineseInput, 'r') as inFile:
                for sentence in inFile:
                    if sentence != '':
                        sentence = sentence.replace(' ', '').replace('.', '. ').replace(',', ', ')
                        for tab in dictionaries.tabOrder:
                            self.driver.switch_to.window(self.driver.window_handles[tab])
                            self.driver.find_element_by_id(dictionaries.inputBox[dictionaries.tabOrder[tab]]).clear()
                            self.driver.find_element_by_id(dictionaries.inputBox[dictionaries.tabOrder[tab]]).send_keys(sentence)
                        time.sleep(self.courtesyDelay)
                        for tab in dictionaries.tabOrder:
                            self.driver.switch_to.window(self.driver.window_handles[tab])
                            dictionaries.output[dictionaries.tabOrder[tab]].append(self.getOutput(dictionaries.tabOrder[tab]))
            with open(self.englishOutput, 'w') as outFile:
                for site in dictionaries.output:
                    outFile.write('%s\n' % site)
                    for sentence in dictionaries.output[site]:
                        outFile.write('%s\n' % sentence)

        if self.scrapeChi:
            self.setupEngToChi(dictionaries)
            with open(self.englishInput, 'r') as inFile:
                for sentence in inFile:
                    if sentence != '':
                        for tab in dictionaries.tabOrder:
                            self.driver.switch_to.window(self.driver.window_handles[tab])
                            self.driver.find_element_by_id(dictionaries.inputBox[dictionaries.tabOrder[tab]]).clear()
                            self.driver.find_element_by_id(dictionaries.inputBox[dictionaries.tabOrder[tab]]).send_keys(sentence)
                        time.sleep(self.courtesyDelay)
                        for tab in dictionaries.tabOrder:
                            self.driver.switch_to.window(self.driver.window_handles[tab])
                            dictionaries.output[dictionaries.tabOrder[tab]].append(self.getOutput(dictionaries.tabOrder[tab]))
            with open(self.chineseOutput, 'w') as outFile:
                for site in dictionaries.output:
                    outFile.write('%s\n' % site)
                    for sentence in dictionaries.output[site]:
                        outFile.write('%s\n' % sentence)
        if self.scrapeEng or self.scrapeChi:
            self.driver.quit()

    def getOutput(self, site):
        if site.capitalize() == 'Baidu':
            return self.driver.find_element_by_class_name('target-output').text
        elif site.capitalize() == 'Bing':
            self.driver.find_element_by_id('t_copyIcon').click()
            return pyperclip.paste()
        elif site.capitalize() == 'Google':
            return self.driver.find_element_by_id('result_box').text
        elif site.capitalize() == 'Sogou':
            return self.driver.find_element_by_id('sogou-translate-output').text
        elif site.capitalize() == 'Yandex':
            return self.driver.find_element_by_id('translation').text
        else:
            return ''

def postProcess(dictionaries, file):
    with fileinput.FileInput(file, inplace=True) as unprocessed:
        for sentence in unprocessed:
            for properNoun in dictionaries.properNouns:
                sentence = sentence.replace(properNoun, dictionaries.properNouns[properNoun])
            for properNoun in dictionaries.moreProperNouns:
                sentence = sentence.replace(properNoun, dictionaries.moreProperNouns[properNoun])
            for char in dictionaries.punctuation:
                sentence = sentence.replace(char, dictionaries.punctuation[char])
            sentence = ' '.join(jieba.cut(sentence))
            print(sentence, end='')

def bleu(dictionaries, refFile, candFile):
    references = []

    with open(refFile, 'r') as reference:
        sentenceIndex = 0
        for sentence in reference:
            references[sentenceIndex] = sentence.replace(u'\ufeff', '').split()
            sentenceIndex += 1

    with open(candFile, 'r') as candidate:
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


def main():
    driver = ChromeDriver()
    if driver.scrapeEng:
        postProcess(driver, driver.chineseInput)
    if driver.scrapeChi:
        postProcess(driver, driver.chineseOutput)

if __name__ == "__main__": main()
