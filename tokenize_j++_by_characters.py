import re

# 由文件 tokenize_j++_by_characters_characters_input.txt 中讀入 已經 tokenized 的 漢字 源數據
with open('tokenize_j++_by_characters_characters_input.txt', 'r', encoding='utf-8') as file:
    tokenize_jpp_by_characters_characters_input = file.read()

# 由文件 tokenize_j++_by_characters_j++_input.txt 中讀入 未 tokenized 的 j++ 源數據
with open('tokenize_j++_by_characters_j++_input.txt', 'r', encoding='utf-8') as file:
    tokenize_jpp_by_characters_jpp_input = file.read()

characters = re.sub('\*', '', tokenize_jpp_by_characters_characters_input)  # 去除「*」
characters = re.sub('[a-zA-Z](.*?)[0-9]', '□', characters)  # 將 粵拼 轉成 方框
characters = re.sub('-', '', characters)  # 去除「-」
characters = re.sub('[(](.?)[)]', '', characters)  # 去除 英文圓括號 及 其中內容
characters = characters.splitlines()

jpp = re.sub(' - ', ' ', tokenize_jpp_by_characters_jpp_input)  # 去除 地名之間的「 - 」
jpp = jpp.splitlines()

output = []

if len(characters) == len(jpp):  # 確保行數對應
    for i in range(0, len(characters)):
        tokenized = ''

        split_characters = characters[i].split()
        split_jpp = re.sub(' +', ' ', jpp[i]).split()

        curr_index = -1
        for token in split_characters:
            for i in range(0, len(token)):
                curr_index += 1
                tokenized += split_jpp[curr_index] + ' '
            if curr_index != len(split_jpp) - 1:
                tokenized += '| '

        output.append(tokenized)

        print(split_characters)
        print(tokenized)
        if len(''.join(split_characters)) != len(split_jpp):  # 確保每行的字數對應
            raise RuntimeError('Error')

# print(characters)
# print(jpp)
# print(output)
# print(tokenized[:-1].split(' | '))

with open('tokenize_j++_by_characters_characters_output.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(output))

print('轉換成功！已輸出到 tokenize_j++_by_characters_characters_output.txt')
