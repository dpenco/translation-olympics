'''
Author: David Penco
Date: 2018-05-24
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pyperclip
import time

chrome_options = Options()
chrome_options.add_argument('--disable-infobars')
chrome_options.add_experimental_option('prefs', \
{'intl.accept_languages': 'en-US'})
driver = webdriver.Chrome(chrome_options=chrome_options)

courtesyDelay = 5

sites = {'baidu': 'https://fanyi.baidu.com/', \
'bing': 'https://www.bing.com/translator', \
'google': 'https://translate.google.com/', \
'sogou': 'https://fanyi.sogou.com', \
'yandex': 'https://translate.yandex.com/'}

inputBox = {'baidu': 'baidu_translate_input', 'bing': 't_sv', \
'google': 'source', 'sogou': 'sogou-translate-input', 'yandex': 'fakeArea'}

output = {}
for site in sites:
    output[site] = []

tabOrder = {}
tabCounter = 0

def engToChi(site):
    if site == 'baidu':
        driver.find_element_by_class_name('select-from-language').click()
        driver.find_element_by_xpath('//a[@value="en"]').click()
        driver.find_element_by_class_name('select-to-language').click()
        driver.find_element_by_xpath('(//a[@value="zh"])[3]').click()
    elif site == 'bing':
        Select(driver.find_element_by_id('t_sl')).select_by_visible_text('English')
        Select(driver.find_element_by_id('t_tl')).select_by_visible_text('Chinese Simplified')
    elif site == 'google':
        driver.find_element_by_id('gt-sl-gms').click()
        driver.find_element_by_id(':m').click()
        driver.find_element_by_id('gt-tl-gms').click()
        driver.find_element_by_id(':3c').click()
    elif site == 'sogou':
        driver.find_element_by_xpath('//em[@data-langtype="from"]').click()
        driver.find_element_by_xpath('//a[@lang="en"]').click()
        driver.find_element_by_xpath('//em[@data-langtype="to"]').click()
        driver.find_element_by_xpath('//a[@lang="zh-CHS"][@data-type="to"]').click()
    elif site == 'yandex':
        driver.find_element_by_id('dstLangButton').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('(//div[@data-value="zh"])[2]').click()
        driver.find_element_by_id('srcLangButton').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('(//div[@data-value="en"])').click()

def chiToEng(site):
    if site == 'baidu':
        driver.find_element_by_class_name('select-from-language').click()
        driver.find_element_by_xpath('//a[@value="zh"]').click()
        driver.find_element_by_class_name('select-to-language').click()
        driver.find_element_by_xpath('(//a[@value="en"])[3]').click()
    elif site == 'bing':
        Select(driver.find_element_by_id('t_sl')).select_by_visible_text('Chinese Simplified')
        Select(driver.find_element_by_id('t_tl')).select_by_visible_text('English')
    elif site == 'google':
        driver.find_element_by_id('gt-sl-gms').click()
        driver.find_element_by_id(':g').click()
        driver.find_element_by_id('gt-tl-gms').click()
        driver.find_element_by_id(':3j').click()
    elif site == 'sogou':
        driver.find_element_by_xpath('//em[@data-langtype="from"]').click()
        driver.find_element_by_xpath('//a[@lang="zh-CHS"]').click()
        driver.find_element_by_xpath('//em[@data-langtype="to"]').click()
        driver.find_element_by_xpath('//a[@lang="en"][@data-type="to"]').click()
    elif site == 'yandex':
        driver.find_element_by_id('dstLangButton').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('(//div[@data-value="en"])[2]').click()
        driver.find_element_by_id('srcLangButton').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('(//div[@data-value="zh"])').click()

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

def openWebsites(tabCounter, fromEnglish=True):
    for name in sites:
        tabOrder[tabCounter] = name
        tabCounter += 1
        driver.get(sites[name])
        if fromEnglish:
            engToChi(name)
        else:
            chiToEng(name)
        if len(driver.window_handles) < len(sites):
            driver.execute_script('window.open("about:blank");')
            driver.switch_to.window(driver.window_handles[-1])

def engToChiWorkflow(tabCounter):
    openWebsites(tabCounter, fromEnglish=True)
    with open('newEnglish.txt', 'r') as englishInput:
        for sentence in englishInput:
            if sentence != '':
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

def chiToEngWorkflow(tabCounter):
    openWebsites(tabCounter, fromEnglish=False)
    with open('newChinese.txt', 'r') as chineseInput:
        for sentence in chineseInput:
            if sentence != '':
                for tab in tabOrder:
                    driver.switch_to.window(driver.window_handles[tab])
                    enterInput(tabOrder[tab], sentence)
                time.sleep(courtesyDelay)
                for tab in tabOrder:
                    driver.switch_to.window(driver.window_handles[tab])
                    output[tabOrder[tab]].append(getOutput(tabOrder[tab]))
    driver.quit()
    with open('newEnglishOutput.txt', 'w') as englishOutput:
        for site in output:
            englishOutput.write('%s\n' % site)
            for sentence in output[site]:
                englishOutput.write('%s\n' % sentence)

chiToEngWorkflow(tabCounter)
