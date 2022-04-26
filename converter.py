import re

def replace_custom(text):
    res = text
    pattern = r'<:suimindaijizo:[0-9]+>'
    res = re.sub(pattern,'すいみんだいじぞ！',res)
    pattern = r'<:souyazo:[0-9]+>'
    res = re.sub(pattern,'そうやぞ！',res)
    pattern = r'<:eraierai:[0-9]+>'
    res = re.sub(pattern,'えらいえらい',res)
    pattern = r'<:fuun:[0-9]+>'
    res = re.sub(pattern,'ふーーん',res)
    pattern = r'<:imarice:[0-9]+>'
    res = re.sub(pattern,'うう',res)
    pattern = r'<:makaimura:[0-9]+>'
    res = re.sub(pattern,'まかいむら！',res)
    pattern = r'<:chili:[0-9]+>'
    res = re.sub(pattern,'ちり！',res)
    pattern = r'<:maigo:[0-9]+>'
    res = re.sub(pattern,'わたし、いまどこ？',res)
    pattern = r'<:imosi:[0-9]+>'
    res = re.sub(pattern,'やってんね〜',res)
    pattern = r'<:iizo:[0-9]+>'
    res = re.sub(pattern,'いいぞ！',res)
    pattern = r'<:gorohika:[0-9]+>'
    res = re.sub(pattern,'ごろひか',res)

    pattern = r'<:emo:[0-9]+>'
    res = re.sub(pattern,'エモ',res)
    pattern = r'<:hyakuriaru:[0-9]+>'
    res = re.sub(pattern,'ひゃくりある',res)
    pattern = r'<:ikite:[0-9]+>'
    res = re.sub(pattern,'いきて',res)
    pattern = r'<:jigoku:[0-9]+>'
    res = re.sub(pattern,'じごく',res)
    pattern = r'<:matajigoku:[0-9]+>'
    res = re.sub(pattern,'またじごくですかー',res)
    pattern = r'<:nete:[0-9]+>'
    res = re.sub(pattern,'ねて',res)
    pattern = r'<:ryoukaidesu:[0-9]+>'
    res = re.sub(pattern,'りょうかいです',res)
    pattern = r'<:saikou:[0-9]+>'
    res = re.sub(pattern,'ふぁんたすてぃっく！',res)
    pattern = r'<:shitandesune:[0-9]+>'
    res = re.sub(pattern,'えっちなことしたんですね',res)
    pattern = r'<:sorehasou:[0-9]+>'
    res = re.sub(pattern,'それはそう',res)
    pattern = r'<:tanoshimi:[0-9]+>'
    res = re.sub(pattern,'たのしみ',res)
    pattern = r'<:tensai1:[0-9]+>'
    res = re.sub(pattern,'てんさい',res)
    pattern = r'<:tsuyoi:[0-9]+>'
    res = re.sub(pattern,'つよい',res)
    pattern = r'<:waiwai:[0-9]+>'
    res = re.sub(pattern,'わいわい',res)
    pattern = r'<:wow:[0-9]+>'
    res = re.sub(pattern,'わぉ',res)
    pattern = r'<:yattane:[0-9]+>'
    res = re.sub(pattern,'やったね',res)
    pattern = r'<:yoki:[0-9]+>'
    res = re.sub(pattern,'よき',res)
    pattern = r'<:hamuri:[0-9]+>'
    res = re.sub(pattern,'は？むり',res)

    pattern = r'<:SUKI:[0-9]+>'
    res = re.sub(pattern,'すき',res)
    pattern = r'<:koufun:[0-9]+>'
    res = re.sub(pattern,'こうふんしました',res)
    pattern = r'<:nante:[0-9]+>'
    res = re.sub(pattern,'なんて？',res)
    pattern = r'<:orokadana:[0-9]+>'
    res = re.sub(pattern,'おろかだな',res)
    pattern = r'<:ura:[0-9]+>'
    res = re.sub(pattern,'うら',res)
    pattern = r'<:pien_cat:[0-9]+><:pien_cat:[0-9]+>'
    res = re.sub(pattern,'ぴえんこえてぱおん',res)
    pattern = r'<:pien_cat:[0-9]+>'
    res = re.sub(pattern,'ぴえん',res)
    pattern = r'<:seiheki:[0-9]+>'
    res = re.sub(pattern,'せいへきいっち',res)
    pattern = r'<:warship:[0-9]+>'
    res = re.sub(pattern,'しんこうしゅうきょう',res)
    pattern = r'<:wedding-1:[0-9]+>'
    res = re.sub(pattern,'けっこん',res)


    pattern = r'<:ura:[0-9]+>'
    res = re.sub(pattern,'うら',res)
    pattern = r'<:abareruzo:[0-9]+>'
    res = re.sub(pattern,'あばれるぞ',res)
    pattern = r'<:chigau:[0-9]+>'
    res = re.sub(pattern,'ちがうんです',res)
    pattern = r'<:chikarakoso:[0-9]+>'
    res = re.sub(pattern,'ちからこそぱわー',res)
    pattern = r'<:yahari:[0-9]+>'
    res = re.sub(pattern,'やはりぼうりょく',res)
    pattern = r'<:kigakuruu:[0-9]+>'
    res = re.sub(pattern,'きがくるう',res)
    pattern = r'<:sinoyokan:[0-9]+>'
    res = re.sub(pattern,'しのよかん',res)

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
