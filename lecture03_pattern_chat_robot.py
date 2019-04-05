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
    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)

# problem1
def get_response(saying, response_rules):
    for k in response_rules:
        match = pat_match_with_seg(k.split(), saying.split())
        m = len(match)
        n = k.count("?")
        if  m == n:
            str = " ".join(subsitite(random.choice(response_rules[k]).split(), pat_to_dict(pat_match_with_seg(k.split(), saying.split()))))
            return str



def cut_str(str):
    s = ""
    for i in jieba.cut(str): s = s + " " + i
    return s

# problem2
def get_response_chinese(saying, response_rules):
    saying = cut_str(saying)

    for k in response_rules:
        k = cut_str(k)

        match = pat_match_with_seg(k.split(), saying.split())
        m = len(match)
        n = k.count("?")
        if m == n:
            str = " ".join(subsitite(random.choice(response_rules[k]).split(),
                                     pat_to_dict(pat_match_with_seg(k.split(), saying.split()))))
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
        '?*x我想要?*y': ['?x想问你，你觉得?y有什么意义呢?', '为什么你想?y', '?x觉得... 你可以想想你很快就可以有?y了', '你看?x像?y不', '我看你就像?y']
    }


    #input = input("please input:")
    input = "同学你好呀"
    if check_is_chinese(input) is True:
        jieba.add_word({"?*x","?*y"}, freq=None, tag=None)
        print(get_response_chinese(input, rules_chinese))
    else:print(get_response(input,rules))
