'''
1.download the corpus from wikipedis
2.使用WikiExtractor解析下载的wiki语料
3.turnToOnefile将所有wiki文件连接成1个文件，便于繁简转换
4.使用opencc将繁体转换为简体：opencc -i content.txt -o content_simp.txt -c t2s.json


'''

import os
import pandas as pd
import jieba
import re
from functools import reduce
from collections import Counter

def findfile(fdir):
    filelist=[]
    for root, dirs, files in os.walk(fdir):
        for file in files:
            tmp_path = os.path.join(fdir,file)
            if not os.path.isdir(tmp_path):
                filelist.append(tmp_path)
            else:
                findfile(tmp_path)
    return filelist

def token(string):
    return " ".join(re.findall('[\w|\d]+', string))+" "

def cut(line):
    return list(jieba.cut(line))

def turnToOnefile(filedir,conf):
    files = findfile(filedir)
    content = ""
    n = 0
    m = 0
    for file in files:
        print(n)
        with open(file,'r',encoding="utf-8") as f:
            line = f.readline()
            while line:
                #print(str(m) + "b----" + line)
                if line.find("</doc") != -1 or line.find("<doc") != -1:
                    line = f.readline()
                else:
                    content += token(line)
                    conf.write(token(line))
                    print(str(m) + "a----" + token(line))
                    m += 1
                    line = f.readline()

        n += 1

    print("content:",content)

def get_prob(word):
    esp = 1/frequency_sum
    if word in words_count:
        return words_count[word]/frequency_sum
    else:
        return esp

def product(numbers):
    return reduce(lambda n1, n2 : n1 * n2, numbers)

def language_model_one_gram(string):
    words = cut(string)
    return product([get_prob(i) for i in words])


def get_combination_prob(w1,w2):
    if w1 + w2 in _2_gram_counter:return _2_gram_counter[w1+w2]/_2_gram_sum
    else:return 1/_2_gram_sum

def get_prob_2_gram(w1,w2):
    return get_combination_prob(w1,w2)/get_prob(w1)

def language_model_of_2_gram(sentence):
    sentence_probability = 1

    words = cut(sentence)

    for i, w in enumerate(words):
        #print(i,w,words)
        if i == 0:
            prob = get_prob(w)
        else:
            previous = words[i - 1]
            prob = get_prob_2_gram(previous, w)
        sentence_probability *= prob
    return sentence_probability


def dealcorpus(fpath):
    with open(fpath, "r", encoding="utf-8") as contentfile:
        line = contentfile.readline()
        text = ""
        while line:
            text += line
            line = contentfile.readline()

        TEXT = text
        ALL_TOKENS = cut(TEXT)
        valid_tokens = [t for t in ALL_TOKENS if t.strip() and t != "n"]
        words_count = Counter(valid_tokens)
        frequences = [f for w, f in words_count.most_common(100)]
        frequency_all = [f for w, f in words_count.most_common()]
        frequency_sum = sum(frequency_all)
        #print("words_count : {} , frequency_sum : {}".format(words_count,frequency_sum))
        return valid_tokens, words_count, frequency_sum




if __name__ == "__main__":
    filedir = "C:\\Users\\fangsj\\Desktop\\NLPcourse-2019.3\\enwiki\\AA"
    '''
    将语料转换成一个文件
    conf = open("C:\\Users\\fangsj\\Desktop\\NLPcourse-2019.3\\enwiki\\content.txt", "w+",encoding="utf-8")
    turnToOnefile(filedir, conf)
    conf.close()
    '''

    contentpath = "C:\\Users\\fangsj\\Desktop\\NLPcourse-2019.3\\enwiki\\content_simp_10000.txt"
    valid_tokens, words_count, frequency_sum =dealcorpus(contentpath)

    valid_tokens_str = [str(t) for t in valid_tokens]
    all_2_grams_words = [''.join(valid_tokens_str[i:i + 2]) for i in range(len(valid_tokens_str[:-2]))]

    _2_gram_counter = Counter(all_2_grams_words)
    _2_gram_sum = len(all_2_grams_words)

    sentences = [
        "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
        "真事一只好看的小猫 真是一只好看的小猫",
        "我去吃火锅，今晚 今晚我去吃火锅"
    ]

    for s in sentences:
        s1, s2 = s.split()

        print("one gram: ")
        p1, p2 = language_model_one_gram(s1), language_model_one_gram(s2)
        better1 = s1 if p1 > p2 else s2
        print("{} is more possible,".format(better1))
        print("-" * 4 + "{} with probability {}".format(s1, p1))
        print("-" * 4 + "{} with probability {}".format(s2, p2))

        print("two gram: ")
        p3, p4 = language_model_of_2_gram(s1), language_model_of_2_gram(s2)
        better2 = s1 if p3 > p4 else s2
        print("{} is more possible,".format(better2))
        print("-" * 4 + "{} with probability {}".format(s1, p3))
        print("-" * 4 + "{} with probability {}".format(s2, p4))

















