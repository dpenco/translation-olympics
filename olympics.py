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

        if self.scrapeEng or self.scrapeChi:
            chrome_options = Options()
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_experimental_option('prefs', \
            {'intl.accept_languages': 'en-US'})
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
            self.courtesyDelay = 8

        self.dictionary = WebsiteDictionaries()
        self.scrapeData()

    def setupChiToEng(self):
        tabNumber = 0
        self.driver.switch_to.window(self.driver.window_handles[0])
        for site in self.dictionary.url:
            self.driver.get(self.dictionary.url[site])
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
            self.dictionary.tabOrder[tabNumber] = site
            if len(self.driver.window_handles) < len(self.dictionary.url):
                self.driver.execute_script('window.open(\'about:blank\');')
                self.driver.switch_to.window(self.driver.window_handles[-1])
                tabNumber += 1
        self.driver.switch_to.window(self.driver.window_handles[0])

    def setupEngToChi(self):
        tabNumber = 0
        self.driver.switch_to.window(self.driver.window_handles[0])
        for site in self.dictionary.url:
            self.driver.get(self.dictionary.url[site])
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
            self.dictionary.tabOrder[tabNumber] = site
            if len(self.driver.window_handles) < len(self.dictionary.url):
                self.driver.execute_script('window.open(\'about:blank\');')
                self.driver.switch_to.window(self.driver.window_handles[-1])
                tabNumber += 1
        self.driver.switch_to.window(self.driver.window_handles[0])

    def scrapeData(self):
        if self.scrapeEng:
            self.setupChiToEng()
            with open(self.chineseInput, 'r') as inFile:
                for sentence in inFile:
                    if sentence != '':
                        sentence = sentence.replace(' ', '').replace('.', '. ').replace(',', ', ')
                        for tab in self.dictionary.tabOrder:
                            self.driver.switch_to.window(self.driver.window_handles[tab])
                            self.driver.find_element_by_id(self.dictionary.inputBox[self.dictionary.tabOrder[tab]]).clear()
                            self.driver.find_element_by_id(self.dictionary.inputBox[self.dictionary.tabOrder[tab]]).send_keys(sentence)
                        time.sleep(self.courtesyDelay)
                        for tab in self.dictionary.tabOrder:
                            self.driver.switch_to.window(self.driver.window_handles[tab])
                            self.dictionary.output[self.dictionary.tabOrder[tab]].append(self.getOutput(self.dictionary.tabOrder[tab]))
            with open(self.englishOutput, 'w') as outFile:
                for site in self.dictionary.output:
                    outFile.write('%s\n' % site)
                    for sentence in self.dictionary.output[site]:
                        outFile.write('%s\n' % sentence)

        if self.scrapeChi:
            self.setupEngToChi()
            with open(self.englishInput, 'r') as inFile:
                for sentence in inFile:
                    if sentence != '':
                        for tab in self.dictionary.tabOrder:
                            self.driver.switch_to.window(self.driver.window_handles[tab])
                            self.driver.find_element_by_id(self.dictionary.inputBox[self.dictionary.tabOrder[tab]]).clear()
                            self.driver.find_element_by_id(self.dictionary.inputBox[self.dictionary.tabOrder[tab]]).send_keys(sentence)
                        time.sleep(self.courtesyDelay)
                        for tab in self.dictionary.tabOrder:
                            self.driver.switch_to.window(self.driver.window_handles[tab])
                            self.dictionary.output[self.dictionary.tabOrder[tab]].append(self.getOutput(self.dictionary.tabOrder[tab]))
            with open(self.chineseOutput, 'w') as outFile:
                for site in self.dictionary.output:
                    outFile.write('%s\n' % site)
                    for sentence in self.dictionary.output[site]:
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

def postProcess(driver, file):
    with fileinput.FileInput(file, inplace=True) as unprocessed:
        for sentence in unprocessed:
            for properNoun in driver.dictionary.properNouns:
                sentence = sentence.replace(properNoun, driver.dictionary.properNouns[properNoun])
            for properNoun in driver.dictionary.moreProperNouns:
                sentence = sentence.replace(properNoun, driver.dictionary.moreProperNouns[properNoun])
            for char in driver.dictionary.punctuation:
                sentence = sentence.replace(char, driver.dictionary.punctuation[char])
            sentence = ' '.join(jieba.cut(sentence))
            print(sentence, end='')

def main():
    driver = ChromeDriver()
    if driver.scrapeEng:
        postProcess(driver, driver.chineseInput)
    if driver.scrapeChi:
        postProcess(driver, driver.chineseOutput)

if __name__ == "__main__": main()
