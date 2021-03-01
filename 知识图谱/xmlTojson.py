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
    username="neo4j",
    password="password"
)

filepaths = getfiles()

for i in filepaths:
    f2 = open(i.replace(".xml", ".json"), 'w')
    f2.write(xmlToJson(i))
    f2.close()

    dir = xmltodict.parse(open(i, "r").read(), encoding='utf-8')

    lis = []
    lis.append(dir['WMS_Capabilities']['Service']['Title'])
    a = dir['WMS_Capabilities']['Capability']['Layer']
    while type(a) != list and "Layer" in a.keys():
        a = a['Layer']
    if type(a) == list:
        for List in a:
            if "Title" in List.keys():
                lis.append(List["Title"])
            else:
                lis.append("")
            if "Abstract" in List.keys() and List["Abstract"] != None:
                lis.append(List["Abstract"].split(":")[-1])
            else:
                lis.append("")
            if "KeywordList" in List.keys():
                if type(List["KeywordList"]["Keyword"]) != list:
                    for l1 in List["KeywordList"]["Keyword"].split(";"):
                        lis.append(l1)
                else:
                    for ele in List["KeywordList"]["Keyword"]:
                        lis.append(ele)
            else:
                lis.append("")
    else:
        if "Title" in a.keys():
            lis.append(a["Title"])
        else:
            lis.append("")
        if "Abstract" in a.keys() and a["Abstract"] != None:
            lis.append(a["Abstract"].split(":")[-1])
        else:
            lis.append("")
        if "KeywordList" in a.keys():
            if type(a["KeywordList"]["Keyword"]) != list:
                for l2 in a["KeywordList"]["Keyword"].split(";"):
                    lis.append(l2)
            else:
                for ele in a["KeywordList"]["Keyword"]:
                    lis.append(ele)
        else:
            lis.append("")
    print(lis)
    csvFile = open("d:/data/006_矿产资源/data.csv", "at+", newline="")
    writer = csv.writer(csvFile)
    writer.writerow(lis)
    csvFile.close()
