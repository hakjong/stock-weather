from konlpy.tag import Kkma
import csv


kkma = Kkma()


def gen_pol_dic():
    t = {}
    with open('./polarity.csv', 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        for line in rdr:
            word = line[0].split('/')[0].replace('*', '')
            val = line[7]
            if val == 'POS' or val == 'NEG':
                if word not in t:
                    t[word] = {'POS': 0, 'NEG': 0}
                t[word][val] += 1
    for word in t:
        t[word] = max(t[word], key=t[word].get)
    return t


pol_dic = gen_pol_dic()


def analyze(title, text):
    p = kkma.pos(title + ' ' + text)
    pos = 0
    neg = 0
    for p_item in p:
        word = p_item[0]
        if word not in pol_dic:
            continue
        pol = pol_dic[word]
        if pol == 'POS':
            pos += 1
        else:
            neg += 1

    if pos > neg:
        result = 'POS'
    else:
        result = 'NEG'

    print(result + ' (%d/%d)\t: ' % (pos, neg) + title)

    return result

