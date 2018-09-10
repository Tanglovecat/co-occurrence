#!encoding=utf-8
# @Author: tangkangqi
# @Time: 2018-09-09 22:56:30

## 论文数> 200 或 作者数 >1000， 请使用本代码

import pandas as pd
## 从csv 文件读取所有论文的作者 数据
df = pd.read_csv('paper_author.csv', header=None).rename(columns = {0:'authors'})

## 得到所有论文作者列表
df['a_ls'] = df['authors'].apply(lambda x:x.split(', '))

## 求所有出现的作者的论文数
val_ls = []
for a_ls in df['a_ls'].values: 
    for a in a_ls: 
        val_ls.append(a)
adf = pd.DataFrame(pd.Series(val_ls).value_counts()).reset_index().rename(columns = {'index': 'author', 0:'paper_num'})

## 选取论文数多于1篇的作者为 ‘好作者’
## 显然， ‘好作者’ 之间才有计算相关系数的必要
good_author_ls = adf[adf['paper_num'] >1]['author'].values

## 如下是计算合作次数
author_pair_ls = []
for i in range(len(good_author_ls)):
    for j in range(i+1, len(good_author_ls)):
        ## 记录作者对，合作次数， 合作论文id 列表
        author_pair_ls.append({'author_pair':(good_author_ls[i], good_author_ls[j]), 'co-times':0, 'co-paper_id':[]})


paper_authors_ls = df['a_ls'].values # 所有论文的作者列表
for i, author_pair in enumerate(author_pair_ls):
    for j, a_ls in enumerate(paper_authors_ls):
        ## 两个作者同时出现在一篇论文作者列表中：
        ## 合作次数 +1
        ## 合作论文id列表记录该论文id
        if (author_pair['author_pair'][0] in a_ls) & (author_pair['author_pair'][1] in a_ls):
                author_pair_ls[i]['co-times'] +=1
                author_pair_ls[i]['co-paper_id'].append(j)

apdf = pd.DataFrame(author_pair_ls)
## 作者对中两位作者各自的论文数
apdf['authors_paper_num'] = apdf['author_pair'].apply(lambda x: (sum(map(lambda y:1 if x[0] in y else 0, paper_authors_ls)),
                                                                 sum(map(lambda y:1 if x[1] in y else 0, paper_authors_ls)))
                                                                )
## 求共现系数
## 共现系数 = 合作次数^2/（作者1论文数* 作者2论文数）
apdf['co-occurrence_val'] = apdf['co-times']**2/apdf['authors_paper_num'].apply(lambda x:x[0]*x[1])

## 存储“好作者” 之间的合作次数与共现系数
apdf.to_csv('good_co-occurrence.csv')
## 打印合作次数大于 1 的情况
print apdf[apdf['co-times'] >1]
