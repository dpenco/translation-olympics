import jieba

with open('newChineseOutputPostProcessed.txt','r') as unsegmented: # newChineseOutputPostProcessed newChineseDesegmented
    with open('newChineseOutputPostProcessedSegmented.txt','w') as segmented: #newChineseOutputPostProcessedSegmented newChineseDeAndReSegmented
        for sentence in unsegmented:
            segmented.write(' '.join(jieba.cut(sentence)))
