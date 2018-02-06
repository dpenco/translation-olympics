import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from pymouse import PyMouse
from pykeyboard import PyKeyboard

import pyperclip

k = PyKeyboard()
m = PyMouse()

delay = 5 # number of seconds to wait between actions
m.click(100, 900)

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
