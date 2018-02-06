import jieba

with open('baidu.txt','r') as pre:
    with open('baiduseg.txt','a') as post: 
        for sentence in pre:
            seg = jieba.cut(sentence)
            post.write(" ".join(seg))
