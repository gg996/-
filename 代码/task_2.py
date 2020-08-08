import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'SimHei'   #显示中文
plt.rcParams['axes.unicode_minus'] = False    #显示符号


data = pd.read_csv('task1.csv',encoding='gbk')
data2 = pd.read_csv('task2.csv',encoding='gbk')
data1 = pd.merge(left=data,right=data2,on='商品')    #合并数据

data1.loc[:,'支付时间']=pd.to_datetime(data1.loc[:,'支付时间'],
                                    format='%Y-%m-%d', errors='coerce')   #把数据'支付时间'转换成时间类型，并把不合理的时间类型转换为nan值
data1.isnull().sum()   #统计nan值
data1 = data1.dropna(subset=['支付时间'],how='any')   #删除’支付时间‘的nan值
data1.drop(labels=[i for i in data1[data1['实际金额'] == 0].index], axis=0, inplace=True)    #删除’实际金额‘为0的数据，即处理异常值



#数据分组
data1_A = data1.loc[data1['地点']=="A",:]
data1_B = data1.loc[data1['地点']=="B",:]
data1_C = data1.loc[data1['地点']=="C",:]
data1_D = data1.loc[data1['地点']=="D",:]
data1_E = data1.loc[data1['地点']=="E",:]



##2017-06商品销售前五柱状图

data1_index = pd.PeriodIndex(data1['支付时间'],freq='M')   #时间规范化
data1_jun = data1.loc[data1_index=='2017-06',:]   #取出2017-06的数据
sales = data1_jun['商品'].value_counts().head()   #取出频数统计的前五行
data_sales = pd.DataFrame(sales)
data_sales


plt.style.use('ggplot')   #采用绘画格式
plt.figure(figsize=(8,6))  #设置画布
plt.bar(range(5),data_sales['商品'],width=0.4)   #画柱状图
plt.plot(range(5),data_sales['商品'],'D--')    #画折线图
plt.xticks(range(5),data_sales.index)    #设置x刻度
for i, j in zip(range(5),data_sales['商品']):
    plt.text(i, j, j, ha='center', va='bottom')    #文本展示
plt.title('2017-06商品销售前五示意图')
plt.xlabel('商品')
plt.ylabel('销量')
plt.show()



##每月总交易额折线图
#定义line函数，计算每月新交易额
def line(df):
    time_index = pd.PeriodIndex(df['支付时间'],freq='M')
    data_total = df.groupby(by=[time_index.month]).agg({'实际金额':np.sum})   #按月分组，求’实际金额‘的和
    return data_total

line_A = line(data1_A)
line_B = line(data1_B)
line_C = line(data1_C)
line_D = line(data1_D)
line_E = line(data1_E)

plt.figure(figsize=(10,5))
for z in [line_A,line_B,line_C,line_D,line_E]:
    plt.plot(z.index,z['实际金额'])    #画折线图
    plt.legend(['A','B','C','D','E'])
    plt.xticks(z.index)
    plt.title('各售货机每月总交易额折线图')
    plt.xlabel('月份')
    plt.ylabel('总交易额')
plt.show()

##交易额月环比增长率柱状图

data1_con_line = pd.concat([line_A,line_B,line_C,line_D,line_E],axis=1)   #合并数据
data_ring = data1_con_line.pct_change()    #计算月环比增长率
data_ring.columns = ['环比增长率']*5   #改列名
width = 0.15   #设置柱宽
plt.figure(figsize=(10,8))
x = np.arange(len(data_ring))+1
for i in range(0,5):
    plt.bar(x+width*i,data_ring.iloc[:,i],width=0.15)
plt.xticks(x)
plt.legend(['A','B','C','D','E'])
plt.title('各售货机交易额月环比增长率柱状图')
plt.xlabel('月份')
plt.ylabel('月环比增长率')
plt.show()


##每台售货机毛利润占总毛利润比例饼图

def classification(df):
    data_drink = df.loc[df['大类']=='饮料',:]   #取出’饮料类‘商品
    data_nodrink = df.loc[df['大类']=='非饮料',:]   #取出’非饮料类‘商品
    data_1 = data_drink['实际金额'].sum()*0.25   #求饮料类的毛利润
    data_2 = data_nodrink['实际金额'].sum()*0.2    #求非饮料类的毛利润
    data_Total = data_1 + data_2   #求和
    return data_Total

plt.figure(figsize=(8,8))
plt.pie([classification(i) for i in [data1_A,data1_B,data1_C,data1_D,data1_E]],
        autopct='%.2f%%',   #设置展示的数据
        explode=[0.02]*len(list('ABCDE')),
        wedgeprops=dict(width=0.6, edgecolor='w'),   #设置环
        labels=list('ABCDE'))
plt.legend(['A','B','C','D','E'])
plt.title('各售货机毛利润占比情况示意图')
plt.show()


##每月交易额均值气泡图

data1['month']=data1['支付时间'].dt.month   #在data1数据框中新增一列’month‘
data1_p = pd.pivot_table(data=data1,index=['二级类'],columns=['month'],
                         values=['实际金额'],fill_value=0,aggfunc=np.mean,)   #做行是’二级类‘，列是’month‘，值为’实际金额‘的透视表
data_index1 = pd.Series(np.arange(len(data1_p)), index = data1_p.index)   #建立Series
plt.figure(figsize=(10,10))
for i in data1_p.index:
    x = list(range(1,13))   #设置x
    y = list(np.ones(12) * data_index1[i])    #设置y
    cm = plt.cm.get_cmap('RdYlBu')  # 设置气泡颜色
    size = data1_p.loc[i].rank()   #设置气泡大小
    plt.scatter(x, y, s=100 * size, cmap=cm, alpha=0.3)
    plt.xticks(range(1,13))
    plt.yticks(range(len(data1_p)), list(data1_p.index))
    plt.title('每月交易额均值气泡图')
    plt.xlabel('月份')
    plt.ylabel('二级类目')
plt.show()


##售货机C6、7、8三个月订单量热力图

import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = 'SimHei'   #中文显示
plt.rcParams['axes.unicode_minus'] = False   #符号显示
data_timeindex = pd.PeriodIndex(data1_C['支付时间'],freq='M')
data1_C['month'] = data_timeindex.month    #添加一列’month‘
#取出数据
data1_C_jun = data1_C.loc[data_timeindex=='2017-06',:]
data1_C_july = data1_C.loc[data_timeindex=='2017-07',:]
data1_C_aug = data1_C.loc[data_timeindex=='2017-08',:]
#定义heatmap函数，绘制热力图
def heatmap(df):
    df['day']=df['支付时间'].dt.day    #添加’day‘一列
    df['hour']=df['支付时间'].dt.hour   #添加’hour‘一列
    data1_C_pit = pd.pivot_table(df,index=['hour'],columns=['day'],values=['订单号'],
                            aggfunc={'订单号':np.size},fill_value=0)     #做透视表
    plt.figure(figsize= (16,8))
    heap = sns.heatmap(data1_C_pit, annot=True,cmap="Purples")   #画图
    plt.xticks(rotation=90)   #x刻度旋转90度
    plt.xlabel('day')
    plt.ylabel('hour')
    if df['month'].max()==6:
        plt.title('售货机C六月订单量热力图')     #设置标题
    if df['month'].max()==7:
        plt.title('售货机C七月订单量热力图')
    if df['month'].max()==8:
        plt.title('售货机C八月订单量热力图')
    plt.show()
    return heap
heatmap(data1_C_jun)
heatmap(data1_C_july)
heatmap(data1_C_aug)


