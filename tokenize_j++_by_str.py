import re

str = '稟爲 被 強劃 良田 溝基 古圳 乞恩 轉 告事 現時 村上處* 有田 lung4-gen2 底凹 ， 築(cuk1)起 溝基 *古圳 來水通 湆(jaam3)下處 田地 耕食 圖物，歷年 糧稅 還納'
to_be_tokenize = 'ban2 veai4 bi4 kieeng4 vaat6 lieeng4 tin4 geau1 gi1 gu2 zan3 hak1 jan1 zin2 garu3 syu4 jin4 sli4 ' \
                 'slin1 soeng4 sli3 jeau5 tin4 loong4 gen2 dai2 nap1 , slook1 hi2 geau1 gi1 gu2 zan3 looi4 slwi2 ' \
                 'toong1 jam3 ha4 sli3 tin4 di4 gaang1 seek6 tu4 mat6 , leek6 nin4 lieeng4 slui3 vaan4 naap6'

tokenized = ''

split_str = str.split()
split_to_be_tokenize = re.sub(' +', ' ', to_be_tokenize).split()

curr_index = -1
for token in split_str:
    token = re.sub('\*', '', token)  # 去除「*」
    token = re.sub('[a-zA-Z](.*?)[0-9]', '□', token)  # 將 粵拼 轉成 方框
    token = re.sub('-', '', token)  # 去除「-」
    token = re.sub('[(](.*)[)]', '', token)  # 去除 英文圓括號 及 其中內容
    for i in range(0, len(token)):
        curr_index += 1
        tokenized += split_to_be_tokenize[curr_index] + ' '
    if curr_index != len(split_to_be_tokenize) - 1:
        tokenized += '| '

print(str)
print(to_be_tokenize)
print(tokenized)
