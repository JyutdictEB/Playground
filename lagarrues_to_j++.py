import unicodedata
import re

# 由文件 lagarrues_to_j++_input.txt 中讀入源數據
with open('lagarrues_to_j++_input.txt', 'r', encoding='utf-8') as file:
    lagarrues_to_jpp_input = file.read()

lagarrues = re.sub('\n', '$', lagarrues_to_jpp_input)

viet_special_char = 'ĂÂĐÊÔƠƯăâđêôơư'
punctuation = r"[!%&'()$#\"/\*+,-.:;<=>?@[]^_´`{|}~]"
punctuation_pattern = r'(\s?[!%&\'\(\)$#\"\/\\*+,-.:;<=>?@\[\]^_´{|}~]\s?)'
initial_pattern = re.compile(r'^(kho|[nctkp]h|ngh|ng|quo|qu|ko|gi|[mnbptkchvgsdlx])(?=[aeoiuyăâđêôơư])')
initial_conversion = {
    'm': 'm', 'n': 'n', 'nh': 'nj', 'ng': 'ng', 'ngh': 'ng',
    'b': 'bb', 'p': 'b', 't': 'd', 'ch': 'z', 'k': 'g', 'c': 'g', 'qu': 'gv', 'quo': 'gvw', 'ko': 'gw',
    'th': 't', 'kh': 'k', 'kho': 'kw',
    'ph': 'f', 's': 's', 'h': 'h',
    'v': 'v', 'g': 'gh',
    'gi': 'j', 'd': 'j',
    'l': 'l',
    'x': 'sl'
}
special_rime_conversion = {
    'ai': 'aaij', 'ao': 'aao',
    'âu': 'eauw',
    'ôi': 'ooij',
    'ui': 'uij',
    'uy': 'wij',
}
rime_conversion = {
    'a': 'aa', 'ai': 'aai', 'ao': 'aau', 'am': 'aam', 'an': 'aan', 'ang': 'aang', 'ap': 'aap', 'at': 'aat', 'ac': 'aak',
    'ach': 'aakj',
    'ay': 'ai', 'au': 'au',
    'ăi': 'arj',
    'ăy': 'ari', 'ău': 'aru', 'ăo': 'aro', 'ăm': 'am', 'ăn': 'an', 'ăng': 'ang', 'ăp': 'ap', 'ăt': 'at', 'ăc': 'ak',
    'âi': 'eaj',
    'ây': 'eai', 'âu': 'eau', 'âo': 'eao', 'âm': 'eam', 'ân': 'ean', 'âng': 'eang', 'âp': 'eap', 'ât': 'eat',
    'ơi': 'ori', 'ơp': 'orp',
    'o': 'o', 'oi': 'oi', 'on': 'on', 'ong': 'ong', 'op': 'op', 'ot': 'ot', 'oc': 'ok',
    'ô': 'oo', 'ôi': 'ooi', 'ôn': 'oon', 'ông': 'oong', 'ôp': 'oop', 'ôt': 'oot', 'ôc': 'ook',
    'u': 'u', 'ui': 'ui', 'un': 'un', 'ung': 'ung', 'ut': 'ut', 'uc': 'uk',
    'uy': 'wi', 'uyn': 'yun',
    'ư': 'yu', 'ưng': 'yng', 'ưc': 'yk',
    'ưông': 'yoeng',
    'ương': 'oeng', 'ươc': 'oek',
    'i': 'i', 'y': 'i', 'iu': 'iu', 'im': 'im', 'in': 'in', 'ing': 'ijng', 'inh': 'inj', 'ip': 'ip', 'it': 'it',
    'ic': 'ijk', 'ich': 'ikj',
    'ê': 'ee', 'êu': 'eeu', 'êm': 'eem', 'ên': 'een', 'êng': 'eeng', 'ênh': 'ing', 'êp': 'eep', 'êt': 'eet',
    'êc': 'eek', 'êch': 'ik',
    'iêu': 'ieeu', 'iêm': 'ieem', 'iên': 'ieen', 'iêng': 'ieeng', 'iênh': 'ieenj', 'iêp': 'ieep', 'iêt': 'ieet',
    'iêc': 'ieek',
    'e': 'e', 'eu': 'eu', 'en': 'en', 'eng': 'eng', 'enh': 'enj', 'et': 'et', 'ec': 'ek', 'ech': 'ekj',
    'ieng': 'ieng', 'iec': 'iek',
    'ua': 'uaa', 'uông': 'uoong', 'uăt': 'uat', 'uôc': 'uook',
}
tone_conversion = {
    '́': '1', '̉': '2', '': '3', '̀': '4', '̣': '5', '̃': '5*'
}


def decompose_viet_char(char):
    # 處理二合字母
    decomposed_char = unicodedata.decomposition(char)
    chars = []
    for char in decomposed_char.split(' '):
        chars.append((r'\u' + char).encode().decode('unicode_escape'))
    # 處理三合字母
    decomposed_char = unicodedata.decomposition(chars[0])
    if decomposed_char != '':
        for char in decomposed_char.split(' '):
            chars.append((r'\u' + char).encode().decode('unicode_escape'))
        chars = chars[1:]
        if chars[0] in tone_conversion:
            chars = [unicodedata.normalize('NFC', chars[1] + chars[2]), chars[0]]
        elif chars[2] in tone_conversion:
            chars = [unicodedata.normalize('NFC', chars[1] + chars[0]), chars[2]]
    return chars


lagarrues = lagarrues.lower()
lagarrues = re.sub(punctuation_pattern, r' \1 ', lagarrues)
lagarrues_l = lagarrues.split(' ')
converted = ''
for word in lagarrues_l:
    is_special_rime = False  # 判斷 特殊韻（聲調標在韻尾）
    if word == '' or word in punctuation:  # 跳過符號
        converted += word + ' '
        continue
    if word == 'gềnh':  # 處理特殊情況 gềnh
        converted += 'ghing4' + ' '
        continue
    print(word)
    decomposed_word = ['', '', '']  # ['聲母', '韻母', '聲調']
    for char in word:
        decomposed_char = unicodedata.decomposition(char)
        if decomposed_char != '' and char not in viet_special_char:  # 若 當前字符 是 帶調越南語字母
            decomposed_char_l = decompose_viet_char(char)  # 分離聲調
            decomposed_word[1] += decomposed_char_l[0]
            decomposed_word[2] += decomposed_char_l[1]
            if word.find(char) == len(word) - 1:  # 若當前 帶聲調越南語字母 是 韻尾
                is_special_rime = True
        else:  # 否則跳過
            decomposed_word[1] += char
    decomposed_word[2] = tone_conversion[decomposed_word[2]]
    initial = initial_pattern.match(decomposed_word[1])  # 正則匹配 lagarrues 聲母
    if initial is not None:  # 若有聲母
        decomposed_word[0] = initial.group()
        decomposed_word[1] = decomposed_word[1][len(decomposed_word[0]):]  # 拆分聲母與韻母
        decomposed_word[0] = initial_conversion[decomposed_word[0]]  # 轉換聲母
        if decomposed_word[1] in special_rime_conversion and is_special_rime:  # 先轉換特殊韻母
            decomposed_word[1] = special_rime_conversion[decomposed_word[1]]
        elif decomposed_word[1] in rime_conversion:  # 轉換韻母
            decomposed_word[1] = rime_conversion[decomposed_word[1]]
        else:
            raise RuntimeError('Error')
        if decomposed_word[0] == 'gh' and decomposed_word[1][0] == 'i':  # 處理 gìn > ghin 一類的情況，改成 jin
            decomposed_word[0] = 'j'
        if decomposed_word[0] == 'j' and decomposed_word[1] == 'u':  # 處理 giù > ju 一類的情況，改成 jiu
            decomposed_word[1] = 'iu'
    else:  # 若無聲母
        if decomposed_word[1] in special_rime_conversion and is_special_rime:  # 先轉換特殊韻母
            decomposed_word[1] = special_rime_conversion[decomposed_word[1]]
        elif decomposed_word[1] in rime_conversion:  # 轉換韻母
            decomposed_word[1] = rime_conversion[decomposed_word[1]]
        else:
            raise RuntimeError('Error')
        if decomposed_word[1] == 'yng':  # 處理 有聲母時 ưng > yng 但 無聲母時 ưng > ng 的情況
            decomposed_word[1] = 'ng'
    # if (decomposed_word[1][-1] in 'ptk' or decomposed_word[1][-2:] == 'kj') and decomposed_word[2] == '5':
        # 處理 入聲調 標成 5 的情況
        # decomposed_word[2] = '6'
    converted += ''.join(decomposed_word) + ' '
    print(decomposed_word)

converted = re.sub(' +', ' ', converted)

with open('lagarrues_to_j++_output.txt', 'w', encoding='utf-8') as file:
    converted = re.sub(' \$ ', '\n', converted)
    file.write(converted)

print('轉換成功！已輸出到 lagarrues_to_j++_output.txt')
