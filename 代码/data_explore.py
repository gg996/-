import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'SimHei'   #显示中文
plt.rcParams['axes.unicode_minus'] = False    #显示符号

##读取数据
data = pd.read_csv('meal_order_detail.csv')
data_info = pd.read_csv('meal_order_info.csv',encoding='gbk')

#探索数据
data.shape  #查看数据形状
data.info()   #查看数据类型
index1 = data['dishes_name'].str.contains('\r\n')
data.loc[index1,'dishes_name']   #查看带有\r\n的菜品名称

da = data_info.describe()

data_info['accounts_payable'].min()   #查看消费金额的最小值
data_info['accounts_payable'].max()   #查看消费金额的最大值
data_info['dishes_count'].min()    #查看菜品份数的最小值
data[['dishes_name','order_id']].isnull().sum()  #检查缺失值
data_info[['emp_id','order_status']].isnull().sum()   #检查缺失值

data['place_order_time'] = pd.to_datetime(data['place_order_time'],
                                          format='%Y-%m-%d')  #把时间转换成时间类型
data.loc[index1,'dishes_name'] = data.loc[index1,
                                          'dishes_name'].str.replace('\r\n','')  #删除\r\n
data.loc[:,'dishes_name'] = data.loc[:,'dishes_name'].str.strip()  #删除空格

##构建热销度评分指标
dish_num = data.groupby(['dishes_name']).agg({'counts':np.sum})   #data按dishes_name分组,counts求和
dish_sco = pd.DataFrame(index=dish_num.index)   #创建空的数据框
#定义maxmin函数，求热销度评分
def maxmin(df):
        dish_sco['热销评分'] = (df - df.min())/(df.max() - df.min())
        return dish_sco
dish_sco1 = maxmin(dish_num).sort_values('热销评分',ascending=False)
# dish_sco1.to_csv('H:/1706/线上实习/热销度评分.csv')


##绘制柱状图展示热销top10
dish_top10 = dish_num.sort_values('counts',ascending=False).head(10)
plt.figure(figsize=(12,6))
plt.style.use('ggplot')   #采用绘画格式
plt.barh(range(1,11),dish_top10['counts'])
plt.yticks(range(1,11),dish_top10.index)
plt.xlabel('销量')
plt.ylabel('菜品')
plt.title('2016-08菜品热销度top10')
plt.show()
# dish_top10.to_csv('H:/1706/线上实习/热销top10.csv')



