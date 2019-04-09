"""
问题：
1.遇到了空格的问题
    "hey hello a"能匹配"?*x hello ?*y"，但"hello"无法匹配，待优化
2.中文处理未写完
"""
from collections import defaultdict
import random

def is_variable(pat):
    return pat.startswith('?') and all(s.isalpha() for s in pat[1:])

def is_pattern_segment(pattern):
    return pattern.startswith('?*') and all(a.isalpha() for a in pattern[2:])


fail = [True, None]

def pat_match_with_seg(pattern, saying):
    if not pattern or not saying: return []

    pat = pattern[0]

    if is_variable(pat):
        return [(pat, saying[0])] + pat_match_with_seg(pattern[1:], saying[1:])
    elif is_pattern_segment(pat):
        match, index = segment_match(pattern, saying)
        return [match] + pat_match_with_seg(pattern[1:], saying[index:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return fail


def segment_match(pattern, saying):
    seg_pat, rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')

    if not rest: return (seg_pat, saying), len(saying)

    for i, token in enumerate(saying):
        if rest[0] == token and is_match(rest[1:], saying[(i + 1):]):
            return (seg_pat, saying[:i]), i

    return (seg_pat, saying), len(saying)

def is_match(rest, saying):
    if not rest and not saying:
        return True
    if not all(a.isalpha() for a in rest[0]):
        return True
    if rest[0] != saying[0]:
        return False
    return is_match(rest[1:], saying[1:])

def pat_to_dict(patterns):
    return {k: ' '.join(v) if isinstance(v, list) else v for k, v in patterns}


def subsitite(rule, parsed_rules):
    if not rule: return []
    a  = [parsed_rules.get(rule[0], rule[0])]
    b = subsitite(rule[1:], parsed_rules)
    return a+ b

# problem1
def get_response(saying, response_rules):
    for k in response_rules:
        match = pat_match_with_seg(k.split(), saying.split())
        m = len(match)
        n = k.count("?")
        if  m == n:
            liststr = subsitite(random.choice(response_rules[k]).split(), pat_to_dict(pat_match_with_seg(k.split(), saying.split())))
            str = " ".join(liststr)
            return str



def cut_str(str):
    s = ""
    for i in jieba.cut(str): s = s + " " + i
    if s.strip().find("?*x"):
        s = s.replace("? * x","?*x")
    if s.strip().find("?*y"):
        s = s.replace("? * y","?*y")
    if s.strip().find("?*z"):
        s = s.replace("? * z","?*z")
    if s.strip().find("?x"):
        s = s.replace("? x","?x")
    if s.strip().find("?y"):
        s = s.replace("? y","?y")
    if s.strip().find("?z"):
        s = s.replace("? z","?z")
    return s

# problem2
def get_response_chinese(saying, response_rules):
    saying = cut_str(saying)

    for k in response_rules:

        match = pat_match_with_seg(cut_str(k).split(), saying.split())
        m = len(match)
        n = k.count("?")
        if m == n:
            sa = cut_str(random.choice(response_rules[k.strip()])).split()
            sb = pat_to_dict(pat_match_with_seg(cut_str(k).split(), saying.split()))
            liststr = subsitite(sa,sb)
            str = "".join(liststr)
            return str


#目前只能傻瓜识别，即包含中文则认为调用中文规则
def check_is_chinese(str):
    for ch in str:
        if u'\u4e00' <= ch <= u'\u9fff':return True
        else: return False

import jieba
if __name__ =="__main__":
    rules = {
        '?*x hello ?*y': ['How do you do', 'Please state your problem'],
        '?*x I want ?*y': ['what would it mean if you got ?y', 'Why do you want ?y', 'Suppose you got ?y soon'],
        '?*x if ?*y': ['Do you really think its likely that ?y', 'Do you wish that ?y', 'What do you think about ?y', 'Really-- if ?y'],
        '?*x no ?*y': ['why not?', 'You are being a negative', 'Are you saying \'No\' just to be negative?'],
        '?*x I was ?*y': ['Were you really', 'Perhaps I already knew you were ?y', 'Why do you tell me you were ?y now?'],
        '?*x I feel ?*y': ['Do you often feel ?y ?', 'What other feelings do you have?']
    }

    rules_chinese = {
        '?*x你好?*y': ['你好呀', '请告诉我你的问题'],
        '?*x我想?*y': ['你觉得?y有什么意义呢？', '为什么你想?y', '你可以想想你很快就可以?y了'],
        '?*x我想要?*y': ['?x想问你，你觉得?y有什么意义呢?', '为什么你想?y', '?x觉得... 你可以想想你很快就可以有?y了', '你看?x像?y不', '我看你就像?y'],
        '?*x喜欢?*y': ['喜欢?y的哪里？', '?y有什么好的呢？', '你想要?y吗？'],
        '?*x讨厌?*y': ['?y怎么会那么讨厌呢?', '讨厌?y的哪里？', '?y有什么不好呢？', '你不想要?y吗？'],
        '?*xAI?*y': ['你为什么要提AI的事情？', '你为什么觉得AI要解决你的问题？'],
        '?*x机器人?*y': ['你为什么要提机器人的事情？', '你为什么觉得机器人要解决你的问题？'],
        '?*x对不起?*y': ['不用道歉', '你为什么觉得你需要道歉呢?'],
        '?*x我记得?*y': ['你经常会想起这个吗？', '除了?y你还会想起什么吗？', '你为什么和我提起?y'],
        '?*x如果?*y': ['你真的觉得?y会发生吗？', '你希望?y吗?', '真的吗？如果?y的话', '关于?y你怎么想？'],
        '?*x我?*z梦见?*y': ['真的吗? --- ?y', '你在醒着的时候，以前想象过?y吗？', '你以前梦见过?y吗'],
        '?*x妈妈?*y': ['你家里除了?y还有谁?', '嗯嗯，多说一点和你家里有关系的', '她对你影响很大吗？'],
        '?*x爸爸?*y': ['你家里除了?y还有谁?', '嗯嗯，多说一点和你家里有关系的', '他对你影响很大吗？', '每当你想起你爸爸的时候， 你还会想起其他的吗?'],
        '?*x我愿意?*y': ['我可以帮你?y吗？', '你可以解释一下，为什么想?y'],
        '?*x我很难过，因为?*y': ['我听到你这么说， 也很难过', '?y不应该让你这么难过的'],
        '?*x难过?*y': ['我听到你这么说， 也很难过',
                     '不应该让你这么难过的，你觉得你拥有什么，就会不难过?',
                     '你觉得事情变成什么样，你就不难过了?'],
        '?*x就像?*y': ['你觉得?x和?y有什么相似性？', '?x和?y真的有关系吗？', '怎么说？'],
        '?*x和?*y都?*z': ['你觉得?z有什么问题吗?', '?z会对你有什么影响呢?'],
        '?*x和?*y一样?*z': ['你觉得?z有什么问题吗?', '?z会对你有什么影响呢?'],
        '?*x我是?*y': ['真的吗？', '?x想告诉你，或许我早就知道你是?y', '你为什么现在才告诉我你是?y'],
        '?*x我是?*y吗': ['如果你是?y会怎么样呢？', '你觉得你是?y吗', '如果你是?y，那一位着什么?'],
        '?*x你是?*y吗': ['你为什么会对我是不是?y感兴趣?', '那你希望我是?y吗', '你要是喜欢， 我就会是?y'],
        '?*x你是?*y': ['为什么你觉得我是?y'],
        '?*x因为?*y': ['?y是真正的原因吗？', '你觉得会有其他原因吗?'],
        '?*x我不能?*y': ['你或许现在就能?y', '如果你能?y,会怎样呢？'],
        '?*x我觉得?*y': ['你经常这样感觉吗？', '除了到这个，你还有什么其他的感觉吗？'],
        '?*x我?*y你?*z': ['其实很有可能我们互相?y'],
        '?*x你为什么不?*y': ['你自己为什么不?y', '你觉得我不会?y', '等我心情好了，我就?y'],
        '?*x好的?*y': ['好的', '你是一个很正能量的人'],
        '?*x嗯嗯?*y': ['好的', '你是一个很正能量的人'],
        '?*x不嘛?*y': ['为什么不？', '你有一点负能量', '你说 不，是想表达不想的意思吗？'],
        '?*x不要?*y': ['为什么不？', '你有一点负能量', '你说 不，是想表达不想的意思吗？'],
        '?*x有些人?*y': ['具体是哪些人呢?'],
        '?*x有的人?*y': ['具体是哪些人呢?'],
        '?*x某些人?*y': ['具体是哪些人呢?'],
        '?*x每个人?*y': ['我确定不是人人都是', '你能想到一点特殊情况吗？', '例如谁？', '你看到的其实只是一小部分人'],
        '?*x所有人?*y': ['我确定不是人人都是', '你能想到一点特殊情况吗？', '例如谁？', '你看到的其实只是一小部分人'],
        '?*x总是?*y': ['你能想到一些其他情况吗?', '例如什么时候?', '你具体是说哪一次？', '真的---总是吗？'],
        '?*x一直?*y': ['你能想到一些其他情况吗?', '例如什么时候?', '你具体是说哪一次？', '真的---总是吗？'],
        '?*x或许?*y': ['你看起来不太确定'],
        '?*x可能?*y': ['你看起来不太确定'],
        '?*x他们是?*y吗？': ['你觉得他们可能不是?y？'],
        '?*x': ['很有趣', '请继续', '我不太确定我很理解你说的, 能稍微详细解释一下吗?']
       }


    #input = input("please input:")
    # input = "j I want hhhh"
    input ="小红喜欢小明"
    if check_is_chinese(input) is True:
        print(get_response_chinese(input, rules_chinese))
    else:print(get_response(input,rules))
