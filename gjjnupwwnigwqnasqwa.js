// gjjnupwwnigwqnasqwa!
// ——鍵盤滾手粵語拼音方案轉換器（粵拼->鍵盤滾手）
// 方案描述：https://zhuanlan.zhihu.com/p/422040247
// 音位分析與方案原理：https://www.zhihu.com/pin/1432325715303378945
// 方案創意：@KwingiemChan、@UntPhesoca、@以成
//
// 請使用 Node.js 運行本文件，指令：node + 文件名
// Author: @以成
// Date: 2021-11-05

const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
})

const 其它字符正則匹配 = `^[^a-zA-Z0-9]`
const 單字粵拼正則匹配 = `^[a-zA-Z](.*?)[0-9][0-9']?`
const 聲母正則匹配 = `^(n[jg]?|bb?|dd?|[zcs][hrjl]?|[ptg]h?|[gk][wv]?|[hmqfvwjl])(?=[aeoiuy])`
const 輔音韻尾正則匹配 = `(?<=[aoreiwu])(n[ng]?|[mptkh])(?=[0-9][0-9']?$)`
const 聲調正則匹配 = `[0-9][0-9']?$`
const 首元音正則匹配 = `^(ng$|m$|ii|iw|uw|[iu][:]?|[aeo][aeo]?|yu$|y|w)`
const 轉換元音 = {
    'i': 'j', 'u': 'w', 'i:': 'jj', 'u:': 'ww',
    'w': 'w', 'yu': 'yy',
    'iw': 'j', 'eo': 'y', 'uw': 'w',
    'e': 'qj', 'oe': 'qy', 'o': 'rw',
    'a': 'q',
    'aa': 'qq',
    'm': 'm', 'ng': 'ng'
}
const 轉換聲調 = {
    '1': ' ', '2': 'a', '3': 'e',
    '4': 'i', '5': 'o', '6': 'u'
}

const 粵拼轉爲鍵盤滾手 = (待轉換粵拼) => {
    // 待轉換粵拼 = 'saam1 gau2 sei3 ling4 ng5 ji6 cat1 baat3 luk6'
    // console.log(待轉換粵拼)
    let 轉換後粵拼 = ''

    while (待轉換粵拼.length > 0) {
        // 跳過其它字符
        let 其它字符 = 待轉換粵拼.match(其它字符正則匹配)
        其它字符 = 其它字符 === null ? '' : 其它字符[0]
        if (其它字符 !== '') {
            轉換後粵拼 += 其它字符
            待轉換粵拼 = 待轉換粵拼.slice(其它字符.length)
            continue
        }
        // 匹配單字
        let 當前單字 = 待轉換粵拼.match(單字粵拼正則匹配)
        當前單字 = 當前單字 === null ? '' : 當前單字[0]
        // console.log('當前單字：' + 當前單字)
        // 提取聲母、輔音韻尾及聲調
        let 聲母 = 當前單字.match(聲母正則匹配)
        let 輔音韻尾 = 當前單字.match(輔音韻尾正則匹配)
        let 聲調 = 當前單字.match(聲調正則匹配)
        聲母 = 聲母 === null ? '' : 聲母[0]
        輔音韻尾 = 輔音韻尾 === null ? '' : 輔音韻尾[0]
        聲調 = 聲調 === null ? '' : 聲調[0]
        // 提取元音們
        let 元音們 = (輔音韻尾 !== '' || 聲調 !== '') ?
                    當前單字.slice(聲母.length, -(輔音韻尾.length + 聲調.length)) :
                    當前單字.slice(聲母.length)
        // console.log('聲母：' + 聲母 + '　元音們：' + 元音們 + '　輔音韻尾：' + 輔音韻尾 + '　聲調：' + 聲調)
        // 預先處理：按韻尾分別處理 u、o 元音
        if (輔音韻尾 === 'ng' || 輔音韻尾 === 'k') {
            if (元音們 === 'u') {
                元音們 = 'uw'
            } else if (元音們 === 'i') {
                元音們 = 'iw'
            }
        }
        // 單獨處理 i、u、ei、ou、eoi 韻母
        if (元音們 === 'i') 元音們 = 'i:'
        if (元音們 === 'u') 元音們 = 'u:'
        if (元音們 === 'ei') 元音們 = 'i'
        if (元音們 === 'ou') 元音們 = 'u'
        if (元音們 === 'eoi') 元音們 = 'eo'
        // 逐個提取元音，並轉換元音
        let 提取出的元音們 = []
        while (元音們.length > 0) {
            let 當前元音 = 元音們.match(首元音正則匹配)[0]
            提取出的元音們.push(轉換元音[當前元音])
            元音們 = 元音們.slice(當前元音.length)
        }
        提取出的元音們 = 提取出的元音們.join('')
        // 合併到結果，並轉換聲調
        let 轉換後單字 =  聲母 + 提取出的元音們 + 輔音韻尾 + 轉換聲調[聲調]
        // console.log('轉換後單字：' + 轉換後單字)
        轉換後粵拼 += 轉換後單字
        待轉換粵拼 = 待轉換粵拼.slice(當前單字.length)
    }
    console.log(轉換後粵拼)
}

readline.question(`請輸入文本：`, 待轉換粵拼 => {
    粵拼轉爲鍵盤滾手(待轉換粵拼)
    
    readline.close()
})
