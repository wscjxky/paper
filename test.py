# import re
# url='https://www.researchgate.net/publication/319362128_Channel_Estimation_with_Expectation_Maximization_and_Historical_Information_based_Basis_Expansion_Model_for_Wireless_Communication_Systems_on_High_Speed_Railways'
# print(re.search('\d+_(.+)',url).group(1))
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
import re
import urllib.request

import requests
import xlwt
import xlrd
from xlutils.copy import copy
#添加引用
# home_url = 'http://localhost:8000/api/papers/1/searchPaper/?'
# for root,dirs,files in os.walk('showmore/'):
#     for f in files[1:]:
#         wb=xlrd.open_workbook('showmore/'+f)
#         sh=wb.sheet_by_index(0)
#         value=sh.col_values(1,start_rowx=1)
#         filename=sh.cell_value(0,1)
#         print(filename)
#         for url in value:
#             # print(url)
#             try:
#                 title = (re.search('\d+_(.+)', url).group(1))
#                 title = title.replace('_', ' ')
#                 d = {'title': title, 'url': url}
#                 r = urllib.request.urlopen(home_url + 'source_url=' + filename + '&cit_url=' + url)
#                 print(home_url + 'source_url=' + filename + '&cit_url=' + url)
#                 # r = requests.post(home_url, data=d)
#                 print(r.read())
#             except:
#                 continue


# filename='273396871_Security_and_Reliability_Performance_Analysis_for_Cloud_Radio_Access_Networks_With_Channel_Estimation_Errors'
# with open(filename+'.txt','r') as f :
#     lines= f.readlines()
#     for l in lines:
#         title=(re.search('\d+_(.+)',l).group(1))
#         title=title.replace('_',' ')
#         url=l
#         d = {'title': title, 'url': url}
#         # r = requests.post(home_url, data=d)
#         try:
#             r=urllib.request.urlopen(home_url+'source_url='+filename+'&cit_url='+url)
#             print(home_url+'source_url='+filename+'&cit_url='+url)
#             print(r.read())
#         except:
#             continue


# print('Optimum_phase-only_discrete_broadcast_beamforming_with_antenna_and_user_selection_in_interference_limited_cognitive_radio_networks'.replace('_',' '))

data=urllib.request.urlopen('http://localhost:8000/api/papers/').read().decode('utf8')
data=json.loads(data)
data = data['results']
# data=[1,2]

#数据excel格式
wb = xlwt.Workbook()

for paper_index,paper in enumerate(data):

    author_list=[]
    styleBoldRed = xlwt.easyxf('font: color-index black, bold on')
    headerStyle = styleBoldRed
    # rb = xlrd.open_workbook('data.xlsx', formatting_info=True)
    # rs = rb.sheet_by_index(0)
    # wb = copy(rb)
    # ws = wb.get_sheet(0)
    ws = wb.add_sheet(str(paper_index),cell_overwrite_ok=True)
    ws.write(0, 0, "论文标题", headerStyle)
    ws.write(1, 0, paper['title'], headerStyle)
    ws.write(0, 1, "论文类型", headerStyle)
    ws.write(0, 2, "作者", headerStyle)
    for index,author in enumerate(paper['authors']):
        ws.write(index+1, 2, author['name'], headerStyle)
        author_list.append(author['name'])
    ws.write(0, 3, "引用论文", headerStyle)
    ws.write(0, 4, "引用作者", headerStyle)
    for cit_index,cit in enumerate(paper['cit_paper']):
        cit_author_list = []
        ws.write(cit_index+1, 3, cit['title'], headerStyle)
        for author_index,author in enumerate(cit['authors']):
            cit_author_list.append(author['name'])
        ws.write(cit_index+1, 4,','.join(cit_author_list), headerStyle)
        type = list(set(author_list).intersection(set(cit_author_list)))
        print(type)
        print(paper_index)
        if type:
            if author_list[0] ==cit_author_list[0]:
                ws.write(cit_index+1, 5, "自引", headerStyle)
            if author_list[0] != cit_author_list[0]:
                ws.write(cit_index + 1, 5, "严格他引", headerStyle)
        else:
            ws.write(cit_index + 1, 5, "全部他引", headerStyle)
    ws.write(0, 5, "引用类型", headerStyle)

wb.save('data.xlsx')

#展示90和11





# import MySQLdb
#
# # 打开数据库连接
# db = MySQLdb.connect("47.94.251.202","root","root","paper" )
#
# # 使用cursor()方法获取操作游标
# cursor = db.cursor()
#
# # 使用execute方法执行SQL语句
# cursor.execute("SELECT * FROM `api_paper_cit_paper` ORDER BY `api_paper_cit_paper`.`id` ASC")
# # 使用 fetchone() 方法获取一条数据
# data = cursor.fetchall()
# for i  in data:
#     print(cursor.execute("UPDATE `api_paper_cit_paper` SET `from_paper_id` = "+str(i[2])+",`to_paper_id`="+str(i[1])+" WHERE `api_paper_cit_paper`.`id` = "+str(i[0])+";")
#           )    # print(i)
#     db.commit()
# # break
# # (130, 188, 71)
#
# # 关闭数据库连接
# db.close()