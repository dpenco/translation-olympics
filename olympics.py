'''
Author: David Penco
Date: 2018-05-24
TODO: engToChi should clear the textboxes
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

chrome_options = Options()
chrome_options.add_argument('--disable-infobars')
chrome_options.add_experimental_option('prefs', \
{'intl.accept_languages': 'en-US'})
driver = webdriver.Chrome(chrome_options=chrome_options)

sites = {'baidu': 'https://fanyi.baidu.com/', \
'bing': 'https://www.bing.com/translator', \
'google': 'https://translate.google.com/', \
'sogou': 'https://fanyi.sogou.com', \
'yandex': 'https://translate.yandex.com/'}

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
        driver.find_element_by_xpath('(//div[@data-value="zh"])[2]').click()
        driver.find_element_by_id('srcLangButton').click()
        driver.find_element_by_xpath('(//div[@data-value="en"])').click()


for name, url in sites.items():
    tabOrder[name] = tabCounter
    tabCounter += 1
    driver.get(url)
    engToChi(name)
    if len(driver.window_handles) < len(sites):
        driver.execute_script('window.open("about:blank");')
        driver.switch_to.window(driver.window_handles[-1])



input()
driver.quit()

'''
with open('chinese.txt','r') as en:
    with open('zhen.txt','a') as zh:
        for sentence in en:
            # 搜狗翻译
            k.press_keys(['Control_L', 'Tab'])
            time.sleep(delay)
            m.click(355, 300, 1, 3)
            time.sleep(delay)
            pyperclip.copy(sentence.replace('\ufeff', '').strip())
            time.sleep(delay)
            k.press_keys(['Control_L', 'v'])
            time.sleep(delay)
            m.click(960, 300, 1, 3)
            time.sleep(delay)
            k.press_keys(['Control_L', 'c'])
            time.sleep(delay)
            translation = pyperclip.paste()
            zh.write(translation)
            time.sleep(delay)
            # 百度翻译
            k.press_keys(['Control_L', 'Tab'])
            time.sleep(delay)
            m.click(357, 238, 1, 3)
            time.sleep(delay)
            pyperclip.copy(sentence.replace('\ufeff', '').strip())
            time.sleep(delay)
            k.press_keys(['Control_L', 'v'])
            time.sleep(delay)
            m.click(850, 200)
            time.sleep(delay)
            m.click(962, 237, 1, 3)
            time.sleep(delay)
            k.press_keys(['Control_L', 'c'])
            time.sleep(delay)
            translation = pyperclip.paste()
            zh.write(translation)
            time.sleep(delay)
            # 谷歌翻译
            k.press_keys(['Control_L', 'Tab'])
            time.sleep(delay)
            m.click(37, 285, 1, 3)
            time.sleep(delay)
            pyperclip.copy(sentence.replace('\ufeff', '').strip())
            time.sleep(delay)
            k.press_keys(['Control_L', 'v'])
            time.sleep(delay)
            m.click(680, 285, 1, 3)
            time.sleep(delay)
            k.press_keys(['Control_L', 'c'])
            time.sleep(delay)
            translation = pyperclip.paste()
            zh.write(translation)
            time.sleep(delay)
'''
