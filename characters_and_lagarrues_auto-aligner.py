import re

# 由文件 characters_and_lagarrues_auto-aligner_characters_input.txt 中讀入 未分行的漢字 源數據
with open('characters_and_lagarrues_auto-aligner_characters_input.txt', 'r', encoding='utf-8') as file:
    characters_and_lagarrues_auto_aligner_characters_input = file.read()

# 由文件 characters_and_lagarrues_auto-aligner_lagarrues_input.txt 中讀入 已經分行的 Lagarrue's 源數據
with open('characters_and_lagarrues_auto-aligner_lagarrues_input.txt', 'r', encoding='utf-8') as file:
    characters_and_lagarrues_auto_aligner_lagarrues_input = file.read()

chinese_punctuation_pattern = r'(\s?[！‘’“”「」（），—。：；《》？【】…｛｝$]\s?)'
english_punctuation_pattern = r'[!%&\'\(\)$#\"\/\\*+,-.:;<=>?@\[\]^_´{|}~]'

# 預處理 未分行的漢字 源數據
characters_input = re.sub(chinese_punctuation_pattern, '', characters_and_lagarrues_auto_aligner_characters_input)
characters_input = re.sub('\*', '', characters_input)  # 去除「*」
characters_input = re.sub('[a-zA-Z](.*?)[0-9]', '□', characters_input)  # 將 粵拼 轉成 方框
characters_input = re.sub('-', '', characters_input)  # 去除「-」
characters_input = re.sub('[(](.?)[)]', '', characters_input)  # 去除 英文圓括號 及 其中內容
characters_input = re.sub(' ', '', characters_input)
# print(characters_input)

# 預處理 已經分行的 Lagarrue's 源數據
lagarrues_input = re.sub('[(](.?)[)]', '', characters_and_lagarrues_auto_aligner_lagarrues_input)  # 去除 英文圓括號 及 其中內容
lagarrues_input = re.sub(english_punctuation_pattern, '', lagarrues_input)
lagarrues_input = re.sub(' +\n', '\n', lagarrues_input)
# print(lagarrues_input)

characters_output = ''
index = 0
for line in lagarrues_input.splitlines():
    print(line, end=' ')
    for i in range(0, len(line.split())):
        print(characters_input[index], end='')
        characters_output += characters_input[index]
        index += 1
    print()
    characters_output += '\n'

with open('characters_and_lagarrues_auto-aligner_characters_output.txt', 'w', encoding='utf-8') as file:
    file.write(characters_output[:-1])

print('轉換成功！已輸出到 characters_and_lagarrues_auto-aligner_characters_output.txt')
