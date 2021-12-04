from urllib import request
import re
import json
import os
# 断点调试
# 现成的框架：beautifulsoup库，Scrapy
# 爬虫、反爬、反反爬
# 频繁爬取可能被封IP，寻找代理IP
class Spider():
    url = 'https://www.huya.com/g/1'
    # 抓取项目的父节点
    root_pattern = '<span class="txt">([\w\W]*?)</li>'
    name_pattern = '<i class="nick" title="([\s\S]*?)">([\w\W]*?)</i>'
    num_pattern = '<i class="js-num">([\w\W]*?)</i>'

    def __fetch_content(self):# 抓取整页，设置为私有方法
        r = request.urlopen(Spider.url)#实例方法调用类变量的方式
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls


    def __analysis(self, htmls):#爬指定锚点，保存为字典类型
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            num = re.findall(Spider.num_pattern, html)
            anchor = {'name': name,'num': num}
            anchors.append(anchor)
        return anchors

        a = 1

    def __addto_path(self,data,**kwargs):
        if not os.path.exists('exports'):
            os.mkdir('exports')
            with open('exports/zhubo.txt', 'a+', encoding='utf-8') as f:
                    f.write(json.dumps(data,ensure_ascii=False))

    def __refine(self, anchors):
        l = lambda anchor: {
            'name':anchor['name'][0][0].strip(),#list.strip()去掉list前后的空格,name必须是list类型的
            'num':anchor['num'][0]
            }
        return map(l, anchors)
    #排序函数
    def __sort(self, anchors):
        #key指定元素进行比较运算
        anchors = sorted(anchors,key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        r = re.findall('[1-9]\d*\.?\d*', anchor['num'])#匹配任何带小数的观看量
        num = float(r[0])
        if '万' in anchor['num']:
            num *= 10000
        return num

    def __show(self, anchors):# 打印数据方法
        for i,anchor in enumerate(anchors):# 优雅的enumerate取到数据的同时还可以把下标取到
            print(i+1,anchors[i]['name'] + anchors[i]['num'])

        # for rank in range(0,len(anchors)):#for in循环中使用这种取到下标序号
        #     print(str(rank+1)
        #           +' :  ' +anchors[rank]['name']
        #           +'    ' +anchors[rank]['num'])


    def go(self):#入口方法(主方法)
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        # print(anchors)
        anchors = self.__sort(anchors)
        self.__show(anchors)
        # self.__addto_path(anchors)

spider = Spider()
spider.go()