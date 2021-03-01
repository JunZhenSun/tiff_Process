import xmltodict
import json
import os
import csv
from py2neo import Graph, Node, Relationship


def xmlToJson(path):  # 将xml转换为json格式
    xml_str = open(path, "r").read()
    # '''传入xml字符串，返回字典'''
    dic = xmltodict.parse(xml_str, encoding='utf-8')
    dic = json.dumps(dic, indent=4)
    return dic


def getfiles():  # 遍历文件夹中的xml文档
    filenames = os.listdir(r'd:/data/006_矿产资源/46xml/xml/')
    filepaths = []
    for i in filenames:
        if '.xml' in i:
            filepaths.append(os.path.join("d:/data/006_矿产资源/46xml/xml/", i))
    return filepaths


# 数据库初始化
myGraph = Graph(
    "http://localhost:7474",
    username="neo4j2",
    password="password"
)

filepaths = getfiles()

for i in filepaths:

    # f2 = open(i.replace(".xml", ".json"), 'w')  # 将xml转换为json并保存到本地
    # f2.write(xmlToJson(i))
    # f2.close()

    dir = xmltodict.parse(open(i, "r").read(), encoding='utf-8')  # 将xml转换为字典

    lis = []  # 用于暂时存储单行数据的list

    lis.append(dir['WMS_Capabilities']['Service']['Title'])  # 数据第一列：服务的标题

    fNode = Node("WMS", name=dir['WMS_Capabilities']['Service']['Title'])  # 创建服务实体节点
    myGraph.create(fNode)  # 实体节点导入图谱

    a = dir['WMS_Capabilities']['Capability']['Layer']
    while type(a) != list and "Layer" in a.keys():
        a = a['Layer']
    if type(a) == list:
        for List in a:
            if "Title" in List.keys():
                lis.append(List["Title"])
                node_1 = Node('Title', content=List["Title"])  # 创建属性节点
                Rel_1 = Relationship(fNode, "keyword", node_1)  # 创建实体节点与属性节点的关系
                myGraph.create(node_1)  # 属性节点导入图谱
                myGraph.create(Rel_1)  # 实体属性关系导入图谱
            else:
                lis.append("")
            if "Abstract" in List.keys() and List["Abstract"] != None:
                lis.append(List["Abstract"].split(":")[-1])
                node_2 = Node('Abstract', content=List["Abstract"].split(":")[-1])  # 创建属性节点
                Rel_2 = Relationship(fNode, "keyword", node_2)  # 创建实体节点与属性节点的关系
                myGraph.create(node_2)  # 属性节点导入图谱
                myGraph.create(Rel_2)  # 实体属性关系导入图谱
            else:
                lis.append("")
            if "KeywordList" in List.keys():
                if type(List["KeywordList"]["Keyword"]) != list:
                    for l1 in List["KeywordList"]["Keyword"].split(";"):
                        lis.append(l1)
                        node_3 = Node("KeywordList", content=l1)  # 创建属性节点
                        Rel_3 = Relationship(fNode, "keyword", node_3)  # 创建实体节点与属性节点的关系
                        myGraph.create(node_3)  # 属性节点导入图谱
                        myGraph.create(Rel_3)  # 实体属性节点导入图谱
                else:
                    for ele in List["KeywordList"]["Keyword"]:
                        lis.append(ele)
                        node_4 = Node("KeywordList", content=ele)  # 创建属性节点
                        Rel_4 = Relationship(fNode, "keyword", node_4)  # 创建实体节点与属性节点的关系
                        myGraph.create(node_4)  # 属性节点导入图谱
                        myGraph.create(Rel_4)  # 实体属性关系导入图谱
            else:
                lis.append("")
    else:
        if "Title" in a.keys():
            lis.append(a["Title"])
            node_5 = Node('Title', content=a["Title"])  # 创建属性节点
            Rel_5 = Relationship(fNode, "keyword", node_5)  # 创建实体节点与属性节点的关系
            myGraph.create(node_5)  # 属性节点导入图谱
            myGraph.create(Rel_5)  # 实体属性关系导入图谱
        else:
            lis.append("")
        if "Abstract" in a.keys() and a["Abstract"] != None:
            lis.append(a["Abstract"].split(":")[-1])
            node_6 = Node('Abstract', content=a["Abstract"].split(":")[-1])  # 创建属性节点
            Rel_6 = Relationship(fNode, "keyword", node_6)  # 创建实体节点与属性节点的关系
            myGraph.create(node_6)  # 属性节点导入图谱
            myGraph.create(Rel_6)  # 实体属性关系导入图谱
        else:
            lis.append("")
        if "KeywordList" in a.keys():
            if type(a["KeywordList"]["Keyword"]) != list:
                for l2 in a["KeywordList"]["Keyword"].split(";"):
                    lis.append(l2)
                    node_7 = Node("KeywordList", content=l2)  # 创建属性节点
                    Rel_7 = Relationship(fNode, "keyword", node_7)  # 创建实体节点与属性节点的关系
                    myGraph.create(node_7)  # 属性节点导入图谱
                    myGraph.create(Rel_7)  # 实体属性关系导入图谱
            else:
                for ele in a["KeywordList"]["Keyword"]:
                    lis.append(ele)
                    node_8 = Node("KeywordList", content=ele)  # 创建属性节点
                    Rel_8 = Relationship(fNode, "keyword", node_8)  # 创建实体节点与属性节点的关系
                    myGraph.create(node_8)  # 属性节点导入图谱
                    myGraph.create(Rel_8)  # 实体属性关系导入图谱
        else:
            lis.append("")
    print(lis)
    csvFile = open("d:/data/006_矿产资源/data.csv", "at+", newline="")
    writer = csv.writer(csvFile)
    writer.writerow(lis)
    csvFile.close()
