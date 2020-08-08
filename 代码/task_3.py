import pandas as pd
import numpy as np

data = pd.read_csv('task1.csv',encoding='gbk')
data2 = pd.read_csv('task2.csv',encoding='gbk')
data1 = pd.merge(left=data,right=data2,on='商品')  #合并数据

data1.loc[:,'支付时间']=pd.to_datetime(data1.loc[:,'支付时间'],
                                    format='%Y-%m-%d', errors='coerce')     #把数据'支付时间'转换成时间类型，并把不合理的时间类型转换为nan值
data1.isnull().sum()     #统计nan值
data1 = data1.dropna(subset=['支付时间'],how='any')    #删除’支付时间‘的nan值
data1.drop(labels=[i for i in data1[data1['实际金额'] == 0].index], axis=0, inplace=True)      #删除’实际金额‘为0的数据，即处理异常值
#数据分组
data1_A = data1.loc[data1['地点']=='A',:]
data1_B = data1.loc[data1['地点']=='B',:]
data1_C = data1.loc[data1['地点']=='C',:]
data1_D = data1.loc[data1['地点']=='D',:]
data1_E = data1.loc[data1['地点']=='E',:]


##售货机商品标签
def lab(df):
    data1_drink = df.loc[df['大类']=='饮料',:]   #取出饮料类数据
    data1_drink['毛利润'] = data1_drink['实际金额'] * 0.25    #计算毛利润
    data1_drink_T = data1_drink.groupby(by=['商品'],as_index=True).agg({'订单号':'count','毛利润':'sum'})    #按商品分组并订单号求值，脑利润求和
    lab1 = []   #设置列表lab1
    data1_drink_T = data1_drink_T.rename(columns={'订单号': '销量'})   #把订单号改为销量
    for i,j in zip(data1_drink_T['销量'],data1_drink_T['毛利润']):      #求在四分位数方法下的热销
        if i >= np.percentile(data1_drink_T['销量'],
                            (75)).astype(int) and j >= np.percentile(data1_drink_T['毛利润'],
                            (75)).astype(int):
            lab1.append('热销')
        elif  i <= np.percentile(data1_drink_T['销量'],     #求在四分位数方法下的热销
                          (25)).astype(int) and j <= np.percentile(data1_drink_T['毛利润'],
                          (25)).astype(int):
            lab1.append('滞销')
        else:lab1.append('正常')
    lab1 = pd.DataFrame(lab1)
    lab1.columns = ['标签']
    lab1.insert(0,'饮料类商品',data1_drink_T.index)    #在数据框左边添加一列饮料类商品
    lab1.insert(0,'序号',range(1,len(lab1)+1))     #在数据框左边添加一列序号
    return lab1
lab_A = lab(data1_A)     #求出分类标签并保存
lab_A.to_csv('H:/1706/线上实习/task3_1A.csv')
lab_B = lab(data1_B)
lab_B.to_csv('H:/1706/线上实习/task3_1B.csv')
lab_C = lab(data1_C)
lab_C.to_csv('H:/1706/线上实习/task3_1C.csv')
lab_D = lab(data1_D)
lab_D.to_csv('H:/1706/线上实习/task3_1D.csv')
lab_E = lab(data1_E)
lab_E.to_csv('H:/1706/线上实习/task3_1E.csv')




##标签拓展
def num_set(df,output):
    for i in df.index:
        if(df.loc[i,'标签']=='滞销'):
            df.loc[i,'销售情况'] = '低档'
        elif(df.loc[i,'标签']=='正常'):
            df.loc[i,'销售情况'] = '中档'
        else:df.loc[i,'销售情况'] = '高档'
        df.to_csv(output)
num_set(lab_A,'H:/1706/线上实习/task3_2A.csv')
num_set(lab_B,'H:/1706/线上实习/task3_2B.csv')
num_set(lab_C,'H:/1706/线上实习/task3_2C.csv')
num_set(lab_D,'H:/1706/线上实习/task3_2D.csv')
num_set(lab_E,'H:/1706/线上实习/task3_2E.csv')


##绘制各销售机画像
from pyecharts import options as opts
from pyecharts.charts import WordCloud

#定义Portrait函数，求词云图并保存
def Portrait(df,output):
    data1_drink = df.loc[df['大类'] == '饮料', :]
    data1_drink['毛利润'] = data1_drink['实际金额'] * 0.25
    data1_drink_T = data1_drink.groupby(by=['商品'], as_index=True).agg({'订单号': 'count', '毛利润': 'sum'})
    data1_drink_T = data1_drink_T.rename(columns={'订单号': '销量'})
    data1_drink_T['盈利'] = data1_drink_T['销量'] * data1_drink_T['毛利润']
    wordcloud = (
        WordCloud()
        .add("",data_pair = [(str(i),int(j)) for i,j in zip(data1_drink_T.index,
                                                            data1_drink_T['盈利'])])
        .set_global_opts(title_opts=opts.TitleOpts(title="售货机画像"))
    )
        wordcloud.render(output)
Portrait(data1_A,'H:/1706/线上实习/task3_2A.html')
Portrait(data1_B,'H:/1706/线上实习/task3_2B.html')
Portrait(data1_C,'H:/1706/线上实习/task3_2C.html')
Portrait(data1_D,'H:/1706/线上实习/task3_2D.html')
Portrait(data1_E,'H:/1706/线上实习/task3_2E.html')











