
'''
    viterbi 算法的实现
'''

import sys
import random
import pypinyin
from pypinyin import pinyin,lazy_pinyin
from math import log

word1_dir = {}
word1_cnt = 0
word2_dir = {}
word3_dir = {}
pinyin_dir = {}

lamda1 = 0.25
lamda2 = 0.15
nofound = 20.0

word_filenames = [
    './word/word1_b.txt',
    './word/word2_b.txt',
    './word/word3_b.txt'
]


def get_dir(filename):
    word = {}
    fread = open(filename, 'r', encoding='utf-8')
    line = fread.readline()
    while line:
        w = line[0:-1]
        w = w.split(' ')
        word[w[0]] = int(w[1])
        line = fread.readline()
    return word


def get_possibility1(dic1, wi):
    if wi in dic1.keys():
        return -log((dic1[wi]+0.0)/(word1_cnt+0.0), 10)
    else:
        return nofound


def get_possibility2(dic1, dic2, wi, wj):
    if wi+wj in dic2.keys():
        return -log((dic2[wi+wj]+0.0)/(dic1[wi]), 10)
    else:
        return nofound


def get_possibility3(dic2, dic3, wi, wj, wk):
    if wi+wj+wk in dic3.keys() and wi+wj in dic2.keys():
        return -log((dic3[wi+wj+wk]+0.0)/(dic2[wi+wj]), 10)
    else:
        return nofound


def find_in_dict(pinyin):
    with open("./word/pinyin.txt", "r", encoding="gbk") as file:
        wordlists = file.readlines()
        for item in wordlists:
            line = item.replace('\n', '')
            line = line.split(' ')
            if pinyin == line[0]:
                del line[0]
                return line


def get_pinyin_dir():
    dir = {}
    with open("./word/pinyin.txt", "r", encoding="gbk") as file:
        wordlists = file.readlines()
        for item in wordlists:
            line = item.replace('\n', '')
            line = line.split(' ')
            pinyin = line[0]
            del line[0]
            dir[pinyin] = line
    return dir


def get_pinyin_dict(pinyin_list):
    dic = []
    pylist = pinyin_list.split(' ')
    for item in pylist:
        if item in pinyin_dir.keys():
            dic.append(pinyin_dir[item])
        else:
            print("not valid pinyin, please input again")
            # print(item)
            return []
    return dic


def viterbi(pinyin_list):
    pinyin_dict = get_pinyin_dict(pinyin_list)
    # print(pinyin_dict)
    if not pinyin_dict:
        return pinyin_dict
    length = len(pinyin_dict)
    possibilities = []
    outputs = []
    # 将初始概率加入
    r = []
    maxr = 1000
    linei = pinyin_dict[0]
    leni = len(linei)
    for j in range(0, leni):
        t = get_possibility1(word1_dir, linei[j])
        if t < maxr:
            maxr = t
            index = j
            print("in possi1..." + str(index))
        r.append(t)
        # print(str(j) + " " + str(linei[j]) + " possibitity=" + str(t))
    possibilities.append(r)
    # 开始计算转移概率
    print("transmission...")
    for words in range(1, length):
        # print("in word " + str(words))
        linei = pinyin_dict[words]
        leni = len(linei)
        linej = pinyin_dict[words-1]
        lenj = len(linej)
        r = []
        output = []
        for i in range(0, leni):
            maxr = 1000
            indexj = 0
            for j in range(0, lenj):
                t1 = get_possibility2(word1_dir, word2_dir, linej[j], linei[i])
                t = t1 + possibilities[words - 1][j]
                t = t*(1-lamda1) + lamda1*get_possibility1(word1_dir,linei[i])
                if t < 10:
                    print("t = " + str(t) + linej[j] + linei[i] + " poss2=" + str(t1) + " possAdd=" + str(t))
                if t < maxr:
                    maxr = t
                    indexj = j
                    # print("in possi2..." + str(indexj))
            r.append(maxr)
            output.append(indexj)
        possibilities.append(r)
        outputs.append(output)
    # print(possibilities)
    # print(outputs)
    # 回溯寻找最优解
    result = []
    minr = min(possibilities[length-1])
    index = possibilities[length-1].index(minr)
    result.append(pinyin_dict[length-1][index])
    for words in range(length-2, -1, -1):
        index = outputs[words][index]
        result.append(pinyin_dict[words][index])
    # print(result)
    #
    sentence = ""
    for i in range(len(result)-1, -1, -1):
        sentence = sentence + result[i]
    return sentence


def viterbi_3(pinyin_list):
    pinyin_dict = get_pinyin_dict(pinyin_list)
    # print(pinyin_dict)
    if not pinyin_dict:
        return pinyin_dict
    length = len(pinyin_dict)
    possibilities = []
    outputs = []
    # 将初始概率加入
    r = []
    maxr = 1000
    linei = pinyin_dict[0]
    leni = len(linei)
    for j in range(0, leni):
        t = get_possibility1(word1_dir, linei[j])
        if t < maxr:
            maxr = t
            index = j
            # print("in possi1..." + str(index))
        r.append(t)
        # print(str(j) + " " + str(linei[j]) + " possibitity=" + str(t))
    possibilities.append(r)
    # 开始计算转移概率
    # print("transmission...")
    for words in range(1, length):
        # print("in word " + str(words))
        linei = pinyin_dict[words]
        leni = len(linei)
        linej = pinyin_dict[words-1]
        lenj = len(linej)
        r = []
        output = []
        for i in range(0, leni):
            maxr = 1000
            indexj = 0
            for j in range(0, lenj):
                t1 = get_possibility2(word1_dir, word2_dir, linej[j], linei[i])
                if words > 1:
                    t1 = get_possibility3(word2_dir, word3_dir, pinyin_dict[words-2][outputs[words-2][j]], linej[j], linei[i])
                t = t1 + possibilities[words - 1][j]
                t = t*(1-lamda2) + lamda2*(lamda1*get_possibility1(word1_dir,linei[i])+(1-lamda1)*get_possibility2(word1_dir, word2_dir, linej[j], linei[i]))
                # if t < 10:
                #     if words==1:
                #         print("maxr = "+str(maxr)+"t = " + str(t) +  linej[j] + linei[i] + " poss3=" + str(t1) + " possAdd=" + str(t)
                #           +" poss2="+ str(lamda1*get_possibility1(word1_dir,linei[i])+(1-lamda1)*get_possibility2(word1_dir, word2_dir, linej[j], linei[i])))
                #     else:
                #         print("maxr = "+str(maxr)+"t = " + str(t)+ pinyin_dict[words-2][outputs[words-2][j]] + linej[j] + linei[i] + " poss3=" + str(t1) + " possAdd=" + str(t)
                #           +" poss2="+ str(lamda1*get_possibility1(word1_dir,linei[i])+(1-lamda1)*get_possibility2(word1_dir, word2_dir, linej[j], linei[i])))
                if t < maxr:
                    maxr = t
                    indexj = j
                    # print("in possi2..." + str(indexj))
            r.append(maxr)
            output.append(indexj)
        possibilities.append(r)
        outputs.append(output)
    # print(possibilities)
    # print(outputs)
    # 回溯寻找最优解
    result = []
    minr = min(possibilities[length-1])
    index = possibilities[length-1].index(minr)
    result.append(pinyin_dict[length-1][index])
    for words in range(length-2, -1, -1):
        index = outputs[words][index]
        result.append(pinyin_dict[words][index])
    # print(result)
    #
    sentence = ""
    for i in range(len(result)-1, -1, -1):
        sentence = sentence + result[i]
    return sentence


def work(file_in, file_out):
    fread = open(file_in, 'r', encoding='utf-8')
    fwrite = open(file_out, 'w', encoding='utf-8')
    line = fread.readline()
    while line:
        line = line.strip()
        ans = viterbi_3(line)
        string = "".join(ans)+'\n'
        fwrite.write(string)
        line = fread.readline()


file_in = '../data/input.txt'
file_out = '../data/output.txt'

if __name__ == '__main__':
    pinyin_dir = get_pinyin_dir()
    # print(pinyin_dir)
    word1_dir = get_dir(word_filenames[0])
    # print(word1_dir)
    # print('\n')
    for item in word1_dir.keys():
        word1_cnt += word1_dir[item]
    word2_dir = get_dir(word_filenames[1])
    # print(word2_dir)
    # print('\n')
    word3_dir = get_dir(word_filenames[2])
    # print(word3_dir)
    # print('\n')
    print("end preparation!")

    # while(True):
    #     p = input()
    #     if p == 'quit':
    #         break
    #     print(viterbi_3(p))
    args = sys.argv

    if len(args) == 3:
        file_in = args[1]
        file_out = args[2]
        print("input file is "+file_in)
        print("output file is "+file_out)
    elif len(args) == 1:
        print("input file is " + file_in)
        print("output file is " + file_out)
    else:
        print("输入有误")
        print("python viterbi.py (option)path_of_input_file (option)path_of_output_file")
        exit(1)
    work(file_in, file_out)