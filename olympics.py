'''
Author: David Penco
Date: 2018-05-24
TODO: add selenium wait instead of time.sleep in yandex
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
        chrome_options = Options()
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_experimental_option('prefs', \
        {'intl.accept_languages': 'en-US'})
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.courtesyDelay = 8
        self.dictionary = WebsiteDictionaries()
        setupChiToEng(self)

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

def enterInput(site, sentence):
    driver.find_element_by_id(inputBox[site]).clear()
    driver.find_element_by_id(inputBox[site]).send_keys(sentence)

def getOutput(site):
    if site == 'baidu':
        return driver.find_element_by_class_name('target-output').text
    elif site == 'bing':
        driver.find_element_by_id('t_copyIcon').click()
        return pyperclip.paste()
    elif site == 'google':
        return driver.find_element_by_id('result_box').text
    elif site == 'sogou':
        return driver.find_element_by_id('sogou-translate-output').text
    elif site == 'yandex':
        return driver.find_element_by_id('translation').text
    else:
        return ''

def engToChiWorkflow(tabCounter):
    openWebsites(tabCounter, fromEnglish=True)
    numberOfSentences = 0
    with open('newEnglish.txt', 'r') as englishInput:
        for sentence in englishInput:
            if sentence != '':
                numberOfSentences += 1
                for tab in tabOrder:
                    driver.switch_to.window(driver.window_handles[tab])
                    enterInput(tabOrder[tab], sentence)
                time.sleep(courtesyDelay)
                for tab in tabOrder:
                    driver.switch_to.window(driver.window_handles[tab])
                    output[tabOrder[tab]].append(getOutput(tabOrder[tab]))
    driver.quit()
    with open('newChineseOutput.txt', 'w') as chineseOutput:
        for site in output:
            chineseOutput.write('%s\n' % site)
            for sentence in output[site]:
                chineseOutput.write('%s\n' % sentence)
    return numberOfSentences

def chiToEngWorkflow(tabCounter):
    openWebsites(tabCounter, fromEnglish=False)
    numberOfSentences = 0
    with open('newChineseDesegmented.txt', 'r') as chineseInput:
        for sentence in chineseInput:
            if sentence != '':
                numberOfSentences += 1
                for tab in tabOrder:
                    driver.switch_to.window(driver.window_handles[tab])
                    enterInput(tabOrder[tab], sentence)
                time.sleep(courtesyDelay)
                for tab in tabOrder:
                    driver.switch_to.window(driver.window_handles[tab])
                    output[tabOrder[tab]].append(getOutput(tabOrder[tab]))
    driver.quit()
    with open('newEnglishOutputFromChiDeseg.txt', 'w') as englishOutput:
        for site in output:
            englishOutput.write('%s\n' % site)
            for sentence in output[site]:
                englishOutput.write('%s\n' % sentence)
    return numberOfSentences

engToChiWorkflow(tabCounter=0)
chiToEngWorkflow(tabCounter=0)
