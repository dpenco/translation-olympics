'''
Author: David Penco
Date: 2018-05-24
TODO: add selenium wait instead of time.sleep in yandex
TODO: mod the code so it can handle different language pairs, not just Chi-Eng
TODO: this script currently does not do pre-processing (to desegment the
Chinese), post-processing (to make formatting and proper nouns consistent) or
jieba segmentation, BLEU calculation or statistical analysis. Those parts of
the project are still in other files, at least for now
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pyperclip
import time

'''
Chrome Webdriver, based on Selenium
@Param driver: the Selenium webdriver object
@Param courtesyDelay: time delay, in seconds, to respect terms of service
@Param dictionaries: all the dictionaries used to drive the webscraping
'''
class ChromeDriver:
    def __init__(self):
        print('Constructing a new ChromeDriver...')
        self.chineseInput = input('\nPlease enter the name of the file ' +
        'containing the Chinese sentences. Ensure that each sentence is on a ' +
        'separate line in the file:\n')
        self.englishInput = input('\nPlease enter the name of the file ' +
        'containing the English sentences. Ensure that each sentence is on a ' +
        'separate line in the file:\n')
        self.chineseOutput = input('\nPlease enter the name of the file where' +
        ' you want to write the Chinese output (which comes from the English ' +
        'input):\n')
        self.englishOutput = input('\nPlease enter the name of the file where' +
        ' you want to write the English output (which comes from the Chinese ' +
        'input):\n')
        chrome_options = Options()
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_experimental_option('prefs', \
        {'intl.accept_languages': 'en-US'})
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.courtesyDelay = 8
        self.dictionary = WebsiteDictionaries()
        self.workflow()

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

    '''
    Note: this method currently trusts and relies on the user to provide two files
    with the same number of lines in each
    '''
    def workflow(self):
        self.setupChiToEng()
        sentenceCount = 0
        with open(self.chineseInput, 'r') as inFile:
            for sentence in inFile:
                if sentence != '':
                    sentenceCount += 1
                    print(sentenceCount)
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
        setupEngToChi(self)
        with open(self.englishInput, 'r') as inFile:
            for sentence in inFile:
                if sentence != '':
                    for tab in self.dictionary.tabOrder:
                        self.driver.switch_to.window(self.driver.window_handles[tab])
                        self.driver.find_element_by_id(self.dictionary.inputBox[self.dictionary.tabOrder[tab]]).clear()
                        self.driver.find_element_by_id(self.dictionary.inputBox[self.dictionary.tabOrder[tab]]).send_keys(sentence)
                    time.sleep(courtesyDelay)
                    for tab in self.dictionary.tabOrder:
                        self.driver.switch_to.window(self.driver.window_handles[tab])
                        self.dictionary.output[self.dictionary.tabOrder[tab]].append(self.getOutput(self.dictionary.tabOrder[tab]))
        self.driver.quit()
        with open(self.chineseOutput, 'w') as outFile:
            for site in self.dictionary.output:
                outFile.write('%s\n' % site)
                for sentence in self.dictionary.output[site]:
                    outFile.write('%s\n' % sentence)

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

'''
Dictionaries used to make the code body more modular and easier to edit
@Param url: maps website names to their url
@Param inputBox: maps website names to the id of their translation input box
@Param output: maps website names to their translation output
@Param tabOrder: maps webdriver tab indices to site names
'''
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

def main():
    ChromeDriver()

if __name__ == "__main__": main()
