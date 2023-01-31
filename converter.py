import re

def replace_custom(text):
    res = text
    pattern = r'<:pien_cat:[0-9]+><:pien_cat:[0-9]+>'
    res = re.sub(pattern,'ぴえんこえてぱおん',res)
    pattern = r'<:shippai:[0-9]+><:shippai:[0-9]+><:shippai:[0-9]+>'
    res = re.sub(pattern,'しっぱいしっぱいだいしっぱい',res)

    res = replace_word(res, 'SUKI', 'すき')
    res = replace_word(res, 'abareruzo', 'あばれるぞ')
    res = replace_word(res, 'butsuri', 'ぶつり')
    res = replace_word(res, 'chigau', 'ちがうんです')
    res = replace_word(res, 'chikarakoso', 'ちからこそぱわー')
    res = replace_word(res, 'chili', 'ちり！')
    res = replace_word(res, 'chokingmanju', 'ちょうきんまんじゅう')
    res = replace_word(res, 'chokingmanju1', 'きんにくまんじゅう')
    res = replace_word(res, 'emo', 'エモ')
    res = replace_word(res, 'eraierai', 'えらいえらい')
    res = replace_word(res, 'fuun', 'ふーーん')
    res = replace_word(res, 'gorohika', 'ごろひか')
    res = replace_word(res, 'haishin', 'はいしん')
    res = replace_word(res, 'hamuri', 'は？むり')
    res = replace_word(res, 'hyakuriaru', 'ひゃくりある')
    res = replace_word(res, 'iizo', 'いいぞ！')
    res = replace_word(res, 'ikite', 'いきて')
    res = replace_word(res, 'imarice', 'うう')
    res = replace_word(res, 'itaish', 'いたいっしゅ')
    res = replace_word(res, 'itaisshu', 'いたいっしゅ')
    res = replace_word(res, 'jigoku', 'じごく')
    res = replace_word(res, 'kanashiitake', 'かなしいたけ')
    res = replace_word(res, 'kangaerukao', 'かんがえるかお')
    res = replace_word(res, 'kanoji', 'かのおじ')
    res = replace_word(res, 'katsudon', 'かつどん')
    res = replace_word(res, 'kigakuruu', 'きがくるう')
    res = replace_word(res, 'koufun', 'こうふんしました')
    res = replace_word(res, 'mada', 'まだ？')
    res = replace_word(res, 'maigo', 'わたし、いまどこ？')
    res = replace_word(res, 'makaimura', 'まかいむら！')
    res = replace_word(res, 'matajigoku', 'またじごくですかー')    
    res = replace_word(res, 'nante', 'なんて？')
    res = replace_word(res, 'nete', 'ねて')
    res = replace_word(res, 'oiteko', 'おいてこ')
    res = replace_word(res, 'orokadana', 'おろかだな')
    res = replace_word(res, 'pien_cat', 'ぴえん')
    res = replace_word(res, 'pokemon', 'ぽけもんげっとだぜ')
    res = replace_word(res, 'raji', 'らじ')
    res = replace_word(res, 'ramen-1', 'ラーメン')
    res = replace_word(res, 'ryoukaidesu', 'りょうかいです')
    res = replace_word(res, 'saikou', 'ふぁんたすてぃっく！')
    res = replace_word(res, 'seiheki', 'せいへきいっち')
    res = replace_word(res, 'shippai', 'しっぱい')
    res = replace_word(res, 'shitandesune', 'えっちなことしたんですね')
    res = replace_word(res, 'sinoyokan', 'しのよかん')
    res = replace_word(res, 'sorehasou', 'それはそう')
    res = replace_word(res, 'souyazo', 'そうやぞ！')
    res = replace_word(res, 'suimindaijizo', 'すいみんだいじぞ！')
    res = replace_word(res, 'tanoshimi', 'たのしみ')
    res = replace_word(res, 'tensai1', 'てんさい')
    res = replace_word(res, 'tsuyoi', 'つよい')
    res = replace_word(res, 'ura', 'うら')
    res = replace_word(res, 'waiwai', 'わいわい')
    res = replace_word(res, 'warship', 'しんこうしゅうきょう')
    res = replace_word(res, 'wedding', 'けっこん')
    res = replace_word(res, 'wow', 'わぉ')
    res = replace_word(res, 'yahari', 'やはりぼうりょく')
    res = replace_word(res, 'yattane', 'やったね')
    res = replace_word(res, 'yatteru', 'やってんね〜')
    res = replace_word(res, 'yoki', 'よき')
    return res

def replace_word(text, emoji, yomi):
    res = text
    pattern = r'<:' + emoji + r':[0-9]+>'
    res = re.sub(pattern, yomi ,res)
    return res

def replace_www(text):
    res = text
    pattern = r'[wｗ]{6,}'
    res = re.sub(pattern, 'だいそうげん' ,res)
    pattern = r'[wｗ]{2,}'
    res = re.sub(pattern, 'くさ' ,res)

    return res

def replace_a_emoji(text):
    pattern = r'<a:[a-zA-Z0-9_]+:[0-9]+>'
    return re.sub(pattern,'',text)

def replace_emoji(text):
    pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'
    return re.sub(pattern,'',text)

def replace_mention(text):
    pattern = r'<@[!0-9]*>'
    return re.sub(pattern,'',text)

def replace_kaomoji(text):
    pattern = r'[´`'']'
    return re.sub(pattern, '' ,text)

def replace_url(text):
    pattern = 'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
    return re.sub(pattern,'URLは置いといて...',text)

def replace_long_message(text):
    text_len = len(text)
    if text_len >= 44:
        return text[:40] + '・割愛！'
    return text

def convert(text):
    res = text
    res = replace_custom(res)
    res = replace_a_emoji(res)
    res = replace_emoji(res)
    res = replace_mention(res)
    res = replace_kaomoji(res)
    res = replace_url(res)
    res = replace_www(res)
    res = replace_long_message(res)
    return res

if __name__ == '__main__':
    print(convert(':chicken:'))
    print(convert('https://discord.com/channels/630393792872054814/630393792872054816　これ'))
    print(convert('金曜夜だし明日やりたい人いればやりますがどうでしょうか！また適当に揃ったら開始ぐらいでもいいかも'))
    print(convert('金曜夜だし明日やりたい人いればやりますがどうでしょうか！また適当に揃ったら開始ぐらいで'))
    print(convert('(о´∀`о)'))
    print(convert(':imarice:'))
    print(convert('ww'))
    print(convert('www'))
    print(convert('wwww'))
    print(convert('wwwww'))
    print(convert('wwwwwww'))
    print(convert('<:suimindaijizo:805971651245506590>'))
    print(convert('<:souyazo:806087551416795156>'))
    print(convert('<:makaimura:799163994388168734>'))
    print(convert('<:imarice:799991320642322482>'))
    print(convert('<:fuun:806085617929945098>'))
    print(convert('<:eraierai:805971841234894898>'))
    print(convert('<:chili:799106785696808970>'))
    print(convert('<:iizo:799106785696808970>'))
    print(convert('<:pien_cat:799106785696808970>'))
    print(convert('<:pien_cat:799106785696808970><:pien_cat:799106785696808970>'))
    print(convert('<a:aniblobpopcorn:799106785696808970>'))
    print(convert('<@!888857383814725662> <@!888857383814725662>　めんしょん <@!888857383814725662>'))
    print(convert('<@630372491939807235> <@594415342395195402> <@!281345709788233729> ちりしん'))
