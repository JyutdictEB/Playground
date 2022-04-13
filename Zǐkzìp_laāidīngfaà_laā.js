// Zǐkzìp laāidīngfaà laā!
// ——將粵拼的數字調號轉爲（依照調類的）符號調號
// 陰平 saām 陰上 gáu 陰去 sèi 
// 陽平 lĩng 陽上 nĝ  陽去 jǐ
// 設計靈感：「陰調係直，陽調係攣；上聲指上，去聲指下」
//
// 請使用 Node.js 運行本文件，指令：node + 文件名
// Author: @以成
// Date: 2021-11-01

const 其它字符正則匹配 = `^[^a-zA-Z0-9]`
const 單字粵拼正則匹配 = `^[a-zA-Z](.*?)[0-9][0-9']?`
const 聲母正則匹配 = `^(n[jg]?|bb?|dd?|[zcs][hrjl]?|[ptg]h?|[gk][wv]?|[hmqfvwjl])(?=[aeoiuy])`
const 輔音韻尾正則匹配 = `(?<=[aoreiwu])(n[ng]?|[mptkh])(?=[0-9][0-9']?$)`
const 聲調正則匹配 = `[0-9][0-9']?$`
const 首元音正則匹配 = `^(ng$|m$|ii|[iu]|[aeo][aeo]?|yu$|y|w)`
const 數字調號轉爲符號調號 = {
    '1': '̄', '2': '́', '3': '̀',
    '4': '̃', '5': '̂', '6': '̌'
}

const 粵拼數字調號轉爲符號調號 = (待轉換粵拼) => {
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
        // console.log('聲母：' + 聲母 + '　輔音韻尾：' + 輔音韻尾 + '　聲調：' + 聲調)
        // 提取元音們
        let 元音們 = (輔音韻尾 !== '' || 聲調 !== '') ?
            當前單字.slice(聲母.length, -(輔音韻尾.length + 聲調.length)) :
            當前單字.slice(聲母.length)
        // 逐個提取元音
        let 提取出的元音們 = []
        while (元音們.length > 0) {
            let 當前元音 = 元音們.match(首元音正則匹配)[0]
            提取出的元音們.push(當前元音)
            元音們 = 元音們.slice(當前元音.length)
        }
        // 判斷聲調放置位置，並轉換聲調
        if (提取出的元音們.length > 1) {
            if (提取出的元音們[0] === 'i' || 提取出的元音們[0] === 'w' || 提取出的元音們[0] === 'y') {
                提取出的元音們[1] += 數字調號轉爲符號調號[聲調]
            } else {
                提取出的元音們[0] += 數字調號轉爲符號調號[聲調]
            }
        } else {
            提取出的元音們[0] += 數字調號轉爲符號調號[聲調]
        }
        提取出的元音們 = 提取出的元音們.join('')
        // 合併到結果
        let 轉換後單字 = 聲母 + 提取出的元音們 + 輔音韻尾
        // console.log('轉換後單字：' + 轉換後單字)
        轉換後粵拼 += 轉換後單字
        待轉換粵拼 = 待轉換粵拼.slice(當前單字.length)
    }

    return 轉換後粵拼
}

const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
})

readline.question(`1：Terminal；\n2：文件「io-files/zzldfl-input.txt」\n請選擇輸入方式：`, 輸入方式 => {
    if (輸入方式 === '1') {
        readline.question(`請輸入文本：`, 待轉換粵拼 => {
            console.log(粵拼數字調號轉爲符號調號(待轉換粵拼))

            readline.close()
        })
    } else if (輸入方式 === '2') {
        const fs = require('fs')
        let 轉換結果 = ''

        console.log('文本將會從「io-files/zzldfl-input.txt」讀入')

        try {
            const 待轉換粵拼 = fs.readFileSync('io-files/zzldfl-input.txt', 'utf8')
            轉換結果 = 粵拼數字調號轉爲符號調號(待轉換粵拼)
        } catch (err) {
            console.error(err)
        }

        console.log('文本將會向「io-files/zzldfl-output.txt」輸出')

        try {
            fs.writeFileSync('io-files/zzldfl-output.txt', 轉換結果)
        } catch (err) {
            console.error(err)
        }

        readline.close()
    }
})
