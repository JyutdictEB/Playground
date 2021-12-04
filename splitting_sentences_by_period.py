import re

# 由文件 splitting_sentences_by_period_input.txt 中讀入源數據 篇章 1
with open('splitting_sentences_by_period_input.txt', 'r', encoding='utf-8') as file:
    splitting_sentences_by_period_input = file.read()

str_p1 = re.sub('\n', '$', splitting_sentences_by_period_input)
str_p1 = re.sub('\"', '', str_p1)

str_p1 = re.sub('\. ', '.\n', str_p1)
str_p1 = re.sub('\; ', ';\n', str_p1)
str_p1 = re.sub('\。 ', '。\n', str_p1)
str_p1 = re.sub('\； ', '；\n', str_p1)

str_p1 = re.sub('\$\$', '$$\n', str_p1)

str_p1 = re.sub('\.\n\$', '.$', str_p1)
str_p1 = re.sub('\。\n\$', '。$', str_p1)

str_p1 = re.sub('\$(?![$\n])', '￥\n', str_p1)

str_p1 = re.sub('\.\n\.\n\.\n', '...\n', str_p1)

with open('splitting_sentences_by_period_output.txt', 'w', encoding='utf-8') as file:
    file.write(str_p1)

print('轉換成功！已輸出到 splitting_sentences_by_period_output.txt')