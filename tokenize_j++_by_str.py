import re

str = ''
to_be_tokenize = ''

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
