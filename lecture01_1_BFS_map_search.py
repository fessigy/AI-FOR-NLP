"""
思路：
tmp_pathes来记录需要遍历的路径
finnal_pathes来记录完成从start到达destination的path list
过程是，对于tmp_pathes中每一个需要遍历的path，寻找最后一个节点能往后进行的点，添加记录到tmp_pathes中，若达到终点，则记录到finnal_pathes中。

遇到的问题：
0.刚开始时准备使用一个变量pathes来记录整个过程中的遍历过程，以及最后结果，后来还是觉得使用两个变量更为方便。
1.使用list时，刚开始使用tmp_pathes=pathes.append(path)，结果不正确，引用的问题
2.使用pathes.remove(path)，pathes从[['CHANGCHUN', 'BEIJING', 'URUMQI'], ['CHANGCHUN', 'BEIJING', 'WUHAN'], ['CHANGCHUN', 'BEIJING', 'SHENZHEN', 'WUHAN', 'SHANGHAI', 'NEWYORK ']]变成None，后改用pop
3.connection定义有问题，有的是单项边，所以后续未验证了

另外，代码中加了一个处理：从当前点不会再找path中出现过的点，避免重复，最后直接输出final_path

要交作业时间来不及了的Todo：
0.pathes.remove(path)到底是什么问题导致数据错误
1.学习使用networkx、matplotlib
2.对比老师代码，可重构的地方

"""
BEIJING, CHANGCHUN, URUMQI, WUHAN, GUANGZHOU, SHENZHEN, BANGKOK, SHANGHAI, NEWYORK = """BEIJING,CHANGCHUN,URUMQI,WUHAN,GUANGZHOU,SHENZHEN,BANKOK,SHANGHAI,NEWYORK """.split(",")

dictionary = {}

connection = {
    CHANGCHUN: [BEIJING],
    URUMQI: [BEIJING],
    BEIJING: [URUMQI, CHANGCHUN, WUHAN, SHENZHEN, NEWYORK],
    NEWYORK: [BEIJING, SHANGHAI],
    SHANGHAI: [NEWYORK, WUHAN],
    WUHAN: [SHANGHAI, BEIJING, GUANGZHOU],
    GUANGZHOU: [WUHAN, BANGKOK],
    SHENZHEN: [WUHAN, BANGKOK],
    BANGKOK: [SHENZHEN, GUANGZHOU]
}


def BFS(start, destination, connection_graph):
    tmp_pathes = [[start]]
    finnal_pathes = []
    i = 0

    while tmp_pathes:
        #不要乱用lista.remove(listb)!!!
        #print("11111tmp_pathes:", tmp_pathes)
        path = tmp_pathes.pop()
        #print("22222tmp_pathes:",tmp_pathes)
        #print("22222path:",path)
        frontier = path[-1]
        #print("frontier:",path[-1])
        next_points = connection_graph[frontier]
        print("next_points:", next_points)
        if next_points:
            for n in next_points:
                if n not in path:
                    path.append(n)
                    if n == destination:
                        print("finnal_pathes append", n)
                        #如果不使用copy，则会直接引用path，path的修改会导致finnal_pathes的改变
                        finnal_pathes.append(path.copy());
                    else:
                        print("tmp_pathes append ", n)
                        if tmp_pathes == None:tmp_pathes = [path.copy()]
                        else: tmp_pathes.append(path.copy())
                    path.remove(n)
                    #print("path add:", n)

        else:
            print("delet path:", path)
        print("tmp_pathes:",tmp_pathes)
        print("finnal_pathes:", finnal_pathes)
        i += 1
        print(i)

    return finnal_pathes

if __name__ =="__main__":
    print("final_path:",BFS(CHANGCHUN, BANGKOK, connection))