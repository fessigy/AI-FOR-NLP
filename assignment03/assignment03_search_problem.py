'''
1.从页面“北京地铁开通简表”第二列中获取所有线路的url
2.观察页面，所有页面中数据，除了“北京地铁亦庄线”需要从“车站信息”中获取之外，其它线路都含有“车站列表”
3.分别从这些url中“车站列表”中获取站点名及其顺序，“北京地铁亦庄线”从“车站信息”中获取。
4.
'''

import requests
from bs4 import BeautifulSoup
import re

import matplotlib.pyplot as plt

ori_url = "https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485"

#获取上述网址数据时，报错出现重定向问题“TooManyRedirects: Exceeded 30 redirects.”，
#增加参数allow_redirects=False，仍然不成功，报错302找不到location的地址不对。
#设置header，重新获取
def get_stationlist(ori_url):
    header={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    r = requests.get(ori_url,headers=header)
    r.encoding="utf-8"
    content = r.content.decode("utf8")
    soup = BeautifulSoup(content)

    urldict={}
    for i in soup.find_all('a'):
        if re.findall(r'北京地铁(.+?)线</a>', str(i)):
            m = str(re.findall(r'_blank">(.+?)</a>', str(i))[0])
            n = str(re.findall(r'href="(.+?)" target=', str(i))[0])
            #print(re.findall(r'_blank">(.+?)</a>', str(i)))
            #print(str(i))
            if m in urldict.keys():
                print("urllist exist {}".format(n))
            else:
                urldict[m] = n
                print("urllist append {}  {}".format(m, n))

    #组织stationline的数据
    stationline={}

    for j in urldict.items():
        url = "http://baike.baidu.com" + j[1]

        #如何使用BS来查找“车站列表”下的第一个表格？
        #参考别人

        rr = requests.get(url, headers=header)
        rr.encoding = "utf-8"
        con = rr.content.decode("utf8")
        soup = BeautifulSoup(con)

        emailid_regexp = re.compile('起始/终到车站')

        tb = soup.find_all("th",text=emailid_regexp)
        stationlist = []

        if tb:
            for th in tb:
                gap_station = th.parent.find_next_siblings("tr")
                for td in gap_station:
                    if td.contents[0].string:
                        start,dest = td.contents[0].string.split("——")

                        start = re.findall(r'(.+?)站$', start)[0] if re.findall(r'(.+?)站$', start) else start
                        dest = re.findall(r'(.+?)站$', dest)[0] if re.findall(r'(.+?)站$', dest) else dest

                        if start not in stationlist:
                            stationlist.append(start)
                        if dest not in stationlist:
                            stationlist.append(dest)
                        #print(start,dest)
        else:
        #处理北京地铁亦庄线、北京地铁9号线、北京地铁16号线等找不到“起始/终到车站”的数据
            emailid_regexp = re.compile('车站名称')
            tb = soup.find_all("th", text=emailid_regexp)

            if tb:
                for th in tb:
                    gap_station = th.parent.find_next_siblings("tr")
                    for td in gap_station:
                        if td.contents:
                            if td.contents[0].string:
                                #print(td.contents[0].string)
                                if re.findall(r'(.+?)站$', td.contents[0].string):
                                    station = re.findall(r'(.+?)站$', td.contents[0].string)[0]
                                else:
                                    station = td.contents[0].string
                                if station != "车站名称" and station not in stationlist:
                                    stationlist.append(station)
            else:
            #单独处理北京地铁西郊线
                tb = soup.find_all("div", text=emailid_regexp)

                if tb:
                    for th in tb:
                        gap_station = th.parent.parent.find_next_siblings("tr")
                        for tr in gap_station:
                            # print(tr)
                            for td in tr:
                                if td.contents[0].string:
                                    # print(td.contents[0].string)
                                    if re.findall(r'(.+?)站$', str(td.contents[0].string)):
                                        station = re.findall(r'(.+?)站$', str(td.contents[0].string))[0]
                                    if station not in stationlist:
                                        stationlist.append(station)

        stationline[j[0]]=stationlist
    return stationline

#print(get_stationlist(ori_url))

#已经取得的线路列表
stationline = {
'北京地铁1号线' : ['苹果园', '古城', '八角游乐园', '八宝山', '玉泉路', '五棵松', '万寿路', '公主坟', '军事博物馆', '木樨地', '南礼士路', '复兴门', '西单', '天安门西', '天安门东', '王府井', '东单', '建国门', '永安里', '国贸', '大望路', '四惠', '四惠东'],
'北京地铁13号线' : ['西直门', '大钟寺', '知春路', '五道口', '上地', '西二旗', '龙泽', '回龙观', '霍营', '立水桥', '北苑', '望京西', '芍药居', '光熙门', '柳芳', '东直门'],
'北京地铁八通线' : ['四惠', '四惠东', '高碑店', '传媒大学', '双桥', '管庄', '八里桥', '通州北苑', '果园', '九棵树', '梨园', '临河里', '土桥'],
'北京地铁5号线' : ['天通苑北', '天通苑', '天通苑南', '立水桥', '立水桥南', '北苑路北', '大屯路东', '惠新西街北口', '惠新西街南口', '和平西桥', '和平里北街', '雍和宫', '北新桥', '张自忠路', '东四', '灯市口', '东单', '崇文门', '磁器口', '天坛东门', '蒲黄榆', '刘家窑', '宋家庄'],
'北京地铁8号线' : ['朱辛庄', '育知路', '平西府', '回龙观东大街', '霍营', '育新', '西小口', '永泰庄', '林萃桥', '森林公园南门', '奥林匹克公园', '奥体中心', '北土城', '安华桥', '安德里北街', '鼓楼大街', '什刹海', '南锣鼓巷'],
'北京地铁10号线' : ['巴沟', '苏州街', '海淀黄庄', '知春里', '知春路', '西土城', '牡丹园', '健德门', '北土城', '安贞门', '惠新西街南口', '芍药居', '太阳宫', '三元桥', '亮马桥', '农业展览馆', '团结湖', '呼家楼', '金台夕照', '国贸', '双井', '劲松', '潘家园', '十里河', '分钟寺', '成寿寺', '宋家庄', '石榴庄', '大红门', '角门东', '角门西', '草桥', '纪家庙', '首经贸', '丰台', '泥洼', '西局', '六里桥', '莲花桥', '公主坟', '西钓鱼台', '慈寿寺', '车道沟', '长春桥', '火器营'],
'北京地铁机场线' : ['东直门', '三元桥', 'T3航站楼', 'T2航站楼'],
'北京地铁4号线' : ['安河桥北', '北宫门', '西苑', '圆明园', '北京大学东门', '中关村', '海淀黄庄', '人民大学', '魏公村', '国家图书馆', '动物园', '西直门', '新街口', '平安里', '西四', '灵境胡同', '西单', '宣武门', '菜市口', '陶然亭', '北京南站', '马家堡', '角门西', '公益西桥'],
'北京地铁15号线' : ['清华东路西口', '六道口', '北沙滩', '奥林匹克公园', '安立路', '大屯路东', '关庄', '望京西', '望京', '望京东', '崔各庄', '马泉营', '孙河', '国展', '花梨坎', '后沙峪', '南法信', '石门', '顺义', '俸伯'],
'北京地铁昌平线' : ['昌平西山口', '十三陵景区', '昌平', '昌平东关', '北邵洼', '南邵', '沙河高教园', '沙河', '巩华城', '朱辛庄', '生命科学园', '西二旗'],
'北京地铁大兴线' : ['公益西桥', '新宫', '西红门', '高米店北', '高米店南', '枣园', '清源路', '黄村西大街', '黄村火车站', '义和庄', '生物医药基地', '天宫院'],
'北京地铁房山线' : ['郭公庄', '大葆台', '稻田', '长阳', '篱笆房', '广阳城', '良乡大学城北', '良乡大学城', '良乡大学城西', '良乡南关', '苏庄', '阎村东'],
'北京地铁亦庄线' : ['万源街', '荣京东街', '荣昌东街', '同济南路', '经海路', '次渠南', '次渠'],
'北京地铁9号线' : ['郭公庄', '丰台科技园', '科怡路', '丰台南路', '丰台东大街', '七里庄', '六里桥', '六里桥东', '北京西站', '军事博物馆', '白堆子', '白石桥南', '国家图书馆'],
'北京地铁6号线' : ['海淀五路居', '慈寿寺', '花园桥', '白石桥南', '车公庄西', '车公庄', '平安里', '北海北', '南锣鼓巷', '东四', '朝阳门', '东大桥', '呼家楼', '金台路', '十里堡', '青年路', '褡裢坡', '黄渠', '常营', '草房', '物资学院路', '通州北关', '通运门', '北运河西', '北运河东', '郝家府', '东夏园', '潞城'],
'北京地铁14号线' : ['张郭庄', '园博园', '大瓦窑', '郭庄子', '大井', '七里庄', '西局', '北京南站', '陶然桥', '永定门外', '景泰', '蒲黄榆', '方庄', '十里河', '南八里庄', '北工大西门', '平乐园', '九龙山', '大望路', '红庙', '金台路', '朝阳公园', '枣营', '东风北桥', '将台', '高家园', '望京南', '阜通', '望京', '东湖渠', '来广营', '善各庄'],
'北京地铁7号线' : ['北京西站', '湾子', '达官营', '广安门内', '菜市口', '虎坊桥', '珠市口', '桥湾', '磁器口', '广渠门内', '广渠门外', '双井', '九龙山', '大郊亭', '百子湾', '化工', '南楼梓庄', '欢乐谷景区', '垡头', '双合', '焦化厂'],
'北京地铁16号线' : ['西苑', '农大南路', '马连洼', '西北旺', '永丰南', '永丰', '屯佃', '稻香湖路', '温阳路', '北安河'],
'北京地铁西郊线' : ['巴沟', '颐和园西门', '茶棚', '万安', '植物园', '香山'],
'北京地铁S1线' : ['苹果园', '四道桥', '桥户营', '上岸', '栗园庄', '小园', '石厂', '时间', '金安桥'],
'北京地铁燕房线' : ['燕山', '房山城关', '饶乐府', '马各庄', '大石河东', '星城', '阎村', '紫草坞', '阎村东'],
'北京地铁2号线' : ['西直门', '车公庄', '阜成门', '复兴门', '长椿街', '宣武门', '和平门', '前门', '崇文门', '北京站', '建国门', '朝阳门', '东四十条', '东直门', '雍和宫', '安定门', '鼓楼大街', '积水潭']
}

#组织beloneline，便于查找站名对应的线路
beloneline = {}
for k in stationline:
    for i in stationline[k]:
        if i in beloneline.keys():
            beloneline[i].append(k)
        else:
            beloneline[i] = [k]
print(beloneline)


#part2-visualize


import networkx as nx
import matplotlib.pyplot as plt

#组织站名列表
def calslist(G):
    slist=[]
    for n in G.nodes():
        slist.append(n)
    #print(slist)
    return slist

G = nx.Graph()

for i in stationline:
    for j in range(0,len(stationline[i])):
        if stationline[i][j] not in calslist(G):
            G.add_node(stationline[i][j])
            print("G add node {}".format(stationline[i][j]))
        if j!=0:
            G.add_edge(stationline[i][j-1],stationline[i][j])
            print("G add edge {} - {}".format(stationline[i][j-1],stationline[i][j]))


nx.draw(G, with_labels=True)

'''
#显示中文
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

plt.show()

#part3-search

def search_BFS(graph, start, dest):
    tmp_path = [[start]]
    path = []
    time = 0

    for i in tmp_path:

        tmp_path.pop()
        print(i, tmp_path)
        tmp = i[-1]
        # print(tmp,tmp != dest)
        if tmp != dest:

            for j in graph[tmp]:
                if j not in i:
                    tmp_path.append(i + [j])
                else:
                    continue
                print(time, j, i + [j], tmp_path)
        else:
            path.append(i + [j])
            print(time, j, i + [j], tmp_path, path)
        time += 1

        print("path:{}")
    return path
'''

def is_goal(destination):
    def _wrap(path):
        return path[-1] == destination
    return _wrap

def sort_path(cmp_func,beam=-1):
    def _sorted(pathes):
        return sorted(pathes,key=cmp_func)[:beam]
    return _sorted

#路程最短（站数最少）
def shortest_path(path):
    return len(path)

#最小换乘
def min_transfer(path):
    n = 1
    for i in range(0,len(path)-1):
        if len(beloneline[path[i]]) > 1:
            if path[i-1] != path[i+1]:
                n += 1
    return n


def search(graph, start, is_goal, search_strategy):
    pathes = [[start]]
    print("pathes：{} ...".format(pathes))
    seen = set()

    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]

        if froniter in seen: continue

        successors = graph[froniter]

        for city in successors:
            if city in path: continue

            new_path = path + [city]
            pathes.append(new_path)

            if is_goal(new_path):
                return new_path

        seen.add(froniter)
        pathes = search_strategy(pathes)

def isOneline(station1,station2):
    oneLine = False
    #print(type(station1))
    bs1 = beloneline[station1]
    bs2 = beloneline[station2]
    for i in range(len(beloneline[station1])):
        if beloneline[station1][i] in beloneline[station2]:
            oneLine = True
    return oneLine

def printStra(path):
    #print(beloneline[path[0]])
    #print(path[0])

    print("请从 {} - {}站 上车".format(beloneline[path[0]],path[0]))
    for i in range(1,len(path)-2):
        print(path[i])
        if isOneline(path[i-1],path[i+1]) == False:
            print("请在 {} 换乘 {}".format(path[i-1],beloneline[path[i]]))
    print("请从 {} - {}站 下车".format(beloneline[path[-1]],path[-1]))
'''
start = input("start:")
if start not in slist:
    print("wrong start!!!!!!!!")
    raise Exception("wrong start!!!!!!!!")


dest = input("destination:")
if dest not in slist:
    print("wrong destination!!!!!!!!")
    raise Exception("wrong destination!!!!!!!!")

by_way = int(input("by_way(1.shortest_path; 2.min_transfer): "))

if by_way == 1:
    path = search(graph=G, start=start,is_goal=is_goal(dest),search_strategy=shortest_path,beam=30))
elif by_way == 2:
    path = search(graph=G, start=start, is_goal=is_goal(dest), search_strategy=min_transfer,beam=30))
else:
    print("wrong input!!!!!!!!")
    raise Exception("wrong input!!!!!!!!")
'''

path = search(graph=G, start='首经贸', is_goal=is_goal('天通苑'), search_strategy=sort_path(min_transfer,beam=10000))
print(path)
printStra(path)
