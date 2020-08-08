
import pandas as pd
import numpy as np

#读取数据
data = pd.read_csv('task1.csv',encoding='gbk')
data2 = pd.read_csv('task2.csv',encoding='gbk')
data1 = pd.merge(left=data,right=data2,on='商品')  #合并数据

data1['支付时间']=pd.to_datetime(data1['支付时间'],
                                    format='%Y-%m-%d', errors='coerce')  #把数据'支付时间'转换成时间类型，并把不合理的时间类型转换为nan值
data1.isnull().sum().sum()  #统计nan值
data1 = data1.dropna(subset=['支付时间'],how='any')   #删除’支付时间‘的nan值
print(data1.shape)  #观测data1的形状
data1.drop(labels=[i for i in data1[data1['实际金额'] == 0].index], axis=0, inplace=True)  #删除’实际金额‘为0的数据，即处理异常值

##数据分组并保存
data1_A = data1.loc[data1['地点']=="A",:]
data1_A.to_csv('H:/1706/线上实习/task1_1A.csv')
data1_B = data1.loc[data1['地点']=="B",:]
data1_B.to_csv('H:/1706/线上实习/task1_1B.csv')
data1_C = data1.loc[data1['地点']=="C",:]
data1_C.to_csv('H:/1706/线上实习/task1_1C.csv')
data1_D = data1.loc[data1['地点']=="D",:]
data1_D.to_csv('H:/1706/线上实习/task1_1D.csv')
data1_E = data1.loc[data1['地点']=="E",:]
data1_E.to_csv('H:/1706/线上实习/task1_1E.csv')

##五月销售额和订单量
#定义Calculation函数
def  Calculation(df):
        data_index = pd.PeriodIndex(df['支付时间'],freq='M') #’支付时间‘规范化
        data_may = df.loc[data_index=='2017-05',:]   #取出2017—05的数据
        sale_may = data_may['实际金额'].sum()     #求和
        order_may = data_may['订单号'].nunique()   #去重后求值
        sale = df['实际金额'].sum()
        order = df['订单号'].nunique()
        return sale_may,order_may,sale,order
A = pd.DataFrame(list(Calculation(data1_A)))
B = pd.DataFrame(list(Calculation(data1_B)))
C = pd.DataFrame(list(Calculation(data1_C)))
D = pd.DataFrame(list(Calculation(data1_D)))
E = pd.DataFrame(list(Calculation(data1_E)))

data_tab = pd.concat([A,B,C,D,E],axis=1).T   #合并数据并转置
data_tab.index = ['A','B','C','D','E']    #改索引名称
data_tab.columns = ['sale_may','order_may','sale','order']   #改列名称
data_tab


##各组平均交易额和订单号

#定义Each函数,计算各组平均交易额
def Each(df):
    time_index = pd.PeriodIndex(df['支付时间'],freq='M')
    data_gb = df.groupby(by=[time_index.month,'订单号']).agg({'实际金额':np.sum})   #按照月份、’订单号‘分组，并’实际金额‘求和
    data_sale = data_gb.groupby(by=[time_index.month]).agg({'实际金额':np.mean})    #按照月份分组，并’实际金额‘求均值
    return data_sale
A1 = pd.DataFrame(Each(data1_A))
B1 = pd.DataFrame(Each(data1_B))
C1 = pd.DataFrame(Each(data1_C))
D1 = pd.DataFrame(Each(data1_D))
E1 = pd.DataFrame(Each(data1_E))
data_con = pd.concat([A1,B1,C1,D1,E1],axis=1)   #合并数据
data_con.columns = ['A','B','C','D','E']
data_con

#定义Each1函数,计算各组日均订单量
def Each1(df):
    time_index = pd.PeriodIndex(df['支付时间'], freq='M')
    data_gb = df.groupby(by=[time_index.month]).agg({'订单号':lambda x :x.nunique()})   #按月份分组并让’订单号‘去重求值
    time = [31,28,31,30,31,30,31,31,30,31,30,31]
    data_order = pd.DataFrame(data_gb['订单号']/time)    #求出日均订单量
    return data_order
A1_1 = pd.DataFrame(Each1(data1_A))
B1_1 = pd.DataFrame(Each1(data1_B))
C1_1 = pd.DataFrame(Each1(data1_C))
D1_1 = pd.DataFrame(Each1(data1_D))
E1_1 = pd.DataFrame(Each1(data1_E))

data_con1 = pd.concat([A1_1,B1_1,C1_1,D1_1,E1_1],axis=1)  #合并数据
data_con1.columns = ['A','B','C','D','E']
data_con1








