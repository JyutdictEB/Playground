import unicodedata
import re

lagarrues = 'á ả a à ạ ã ọc chể ọc bao xìn chể xìn lồi'

lagarrues = input('請輸入要轉換的句子：')

viet_special_char = 'ĂÂĐÊÔƠƯăâđêôơư'
punctuation = r"[!%&'()$#\"/\*+,-.:;<=>?@[]^_´`{|}~]"
punctuation_pattern = r'(\s?[!%&\'\(\)$#\"\/\\*+,-.:;<=>?@\[\]^_´{|}~]\s?)'
initial_pattern = re.compile(r'^(kho?|[nctkp]h|ngh|ng|quo?|qu|ko|gi|[mnbptkchvgsdlx])(?=[aeoiuyăâđêôơư])')
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
rime_conversion = {
    'a': 'aa', 'ai': 'aai', 'ao': 'aau', 'am': 'aam', 'an': 'aan', 'ang': 'aang', 'ap': 'aap', 'at': 'aat', 'ac': 'aak', 'ach': 'aakj',
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
    if word == '' or word in punctuation:
        converted += word + ' '
        continue
    print(word)
    decomposed_word = ['', '', '']
    for char in word:
        decomposed_char = unicodedata.decomposition(char)
        if decomposed_char != '' and char not in viet_special_char:
            decomposed_char_l = decompose_viet_char(char)
            decomposed_word[1] += decomposed_char_l[0]
            decomposed_word[2] += decomposed_char_l[1]
        else:
            decomposed_word[1] += char
    decomposed_word[2] = tone_conversion[decomposed_word[2]]
    initial = initial_pattern.match(decomposed_word[1])
    if initial is not None:
        decomposed_word[0] = initial.group()
        decomposed_word[1] = decomposed_word[1][len(decomposed_word[0]):]
        decomposed_word[0] = initial_conversion[decomposed_word[0]]
        if decomposed_word[1] in rime_conversion:
            decomposed_word[1] = rime_conversion[decomposed_word[1]]
        else:
            if initial.group() == 'gi':
                decomposed_word[1] = rime_conversion['i' + decomposed_word[1]]
            else:
                raise RuntimeError('Error')
    else:
        decomposed_word[1] = rime_conversion[decomposed_word[1]]
        if decomposed_word[1] == 'yng':
            decomposed_word[1] = 'ng'
    if decomposed_word[1][-1] in 'ptk' and decomposed_word[2] == '5':
        decomposed_word[2] = '6'
    converted += ''.join(decomposed_word) + ' '
    print(decomposed_word)

print(lagarrues)
print(converted)
