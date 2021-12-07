# 由文件 index_auto-generator_input.txt 中讀入源數據
with open('index_auto-generator_input.txt', 'r', encoding='utf-8') as file:
    index_auto_generator_input = file.read()

split_input = index_auto_generator_input.splitlines()
print(split_input)

for i in range(0, len(split_input)):
    if split_input[i] == '':  # 若當前行未補充 index
        last_line_type = split_input[i - 1][0]  # 獲取上一行類型
        last_line_indexes = split_input[i - 1][1:].split('.')
        print(last_line_type, last_line_indexes, len(last_line_indexes))

        if last_line_type == 'c':  # 若上一行也是 c，則最末的 index 直接加 1
            last_line_indexes[-1] = str(int(last_line_indexes[-1]) + 1)
            split_input[i] = last_line_type + '.'.join(last_line_indexes)
        elif last_line_type == 'j':  # 若上一行是 j，則在第三級 index 從 1 開始計數
            if len(last_line_indexes) == 3:
                last_line_indexes[2] = '1'
            elif len(last_line_indexes) != 3 and split_input[i + 1] != '':
                # 若上一行 index 數量不是 3 個，且下一行非空，即本行二級索引中只有 1 個 c
                print('本行二級索引中只有 1 個 c')
            else:
                last_line_indexes.append('1')
            split_input[i] = 'c' + '.'.join(last_line_indexes)

print(split_input)
split_output = '\n'.join(split_input)

with open('index_auto-generator_output.txt', 'w', encoding='utf-8') as file:
    file.write(split_output)

print('轉換成功！已輸出到 index_auto-generator_output.txt')
