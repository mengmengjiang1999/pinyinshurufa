import os


def checkAns(outputFile1, outputFile2):
    """
        该函数用于判断两个输入文件是否相同，这里采用的方式是读入两个文件的所有行，然后拼起来判断是否相同。可以根据需求修改
        outputFile1,outputFile2 分别为判断的两个文件的文件名
        函数返回布尔值
    """
    with open(outputFile1, "r") as f:
        output1 = f.readlines()
    with open(outputFile2, "r") as f:
        output2 = f.readlines()
    b = "".join(output1) == "".join(output2)
    if not b:
        print(output1)
        print(output2)
    return b


def cal_right_possibility(file1, file2):
    cnt_line = 0
    cnt_word = 0
    f1 = open(file1, 'r')
    f2 = open(file2, 'r')
    output1 = f1.readlines()
    output2 = f2.readlines()
    lines = len(output1)
    words = 0
    for i in range(0, lines):
        line1 = output1[i]
        line2 = output2[i]
        if line1 == line2:
            cnt_line += 1
        word = len(line1)
        words += word
        for j in range(0, word):
            if line1[j] == line2[j]:
                cnt_word += 1
    print(cnt_line)
    print(cnt_line/lines)
    print(cnt_word)
    print(cnt_word/words)
    return "共"+str(lines)+"句\n"+"正确"+str(cnt_line)+"句\n"+"句子正确率："+str(cnt_line/lines)+"\n共"\
           +str(words)+"字\n正确"+str(cnt_word)+"字\n单字正确率"+str(cnt_word/words)


if __name__=='__main__':
    t = cal_right_possibility('output.txt','answer.txt')
    print(t)