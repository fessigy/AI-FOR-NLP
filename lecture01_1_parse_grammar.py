"""
出现的问题：
1.grammar_str中有/n，会造成line为空
"""
grammar = """
sentence => noun_phrase verb_phrase 
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的
"""

import random

def parse_grammar(grammar_str, sep1, sep2):
    g = {}
    for line in grammar_str.split("\n"):
        print(line.strip())
        if line:
            target,rules = line.split(sep1)
            g[target.strip()] = [r.split() for r in rules.split(sep2)]
    print("g:",g)
    return g


def generate(gra,target):
    if target in gra:
        rule = random.choice(gra[target])
        return "".join(generate(gra,r) for r in rule if r != 'null')
    else:
        return target


if __name__ == "__main__":
    print(generate(parse_grammar(grammar,"=>","|"),"sentence"))