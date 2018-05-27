properNouns = {'Peter Gregg': '彼得·格雷格', 'Syed Amjad Ali': \
'赛义德·阿姆贾德·阿里', 'Henrik Amneus': '亨里克·安纽斯', \
'国际货币基金组织': '货币基金组织', '160条': '一六○条', '（IMF）': '', \
'GDP': '国内总产值', '国内生产总值': '国内总产值', 'MER': '市场汇率', 'PARES': \
'价格调整汇率', 'PARE率': '价格调整汇率', 'PAREs': \
'价格调整汇率', 'PPP': '购买力平价', 'WAs': '世界地图集', \
'和（或）': '和/或'}

moreProperNouns = {'Amneus': '安纽斯', 'IMF': '货币基金组织', 'PARE': \
'价格调整汇率', 'WA': '世界地图集'}

punctuation = {' ': '', '》': '', '《': '', '.': '。', ',': '，', \
u'\ufeff': '', '(': '（', ')': '）', '1985和1990': '1985年和1990年', '6000美元': \
'$6000', '（4）': '', ':': '：', ';': '；', '*': '·', '6 000美元': '$6000', \
'[4]/': '', '1994': '1994年', '一九八九至九四年': '1989-1994年'}

def postProcess(inFile, outFile):
    with open(inFile, 'r') as unprocessed:
        with open(outFile, 'w') as result:
            for sentence in unprocessed:
                for properNoun in properNouns:
                    sentence = sentence.replace(properNoun, properNouns[properNoun])
                for properNoun in moreProperNouns:
                    sentence = sentence.replace(properNoun, moreProperNouns[properNoun])
                for char in punctuation:
                    sentence = sentence.replace(char, punctuation[char])
                result.write('%s' % sentence)

postProcess('newChinese.txt', 'newChineseDesegmented.txt')
postProcess('newChineseOutput.txt', 'newChineseOutputPostProcessed.txt')
