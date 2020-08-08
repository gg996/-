
import pandas as pd

def process(file,file1):
    ##读取数据
    data = pd.read_csv(file)
    data_info = pd.read_csv(file1, encoding='gbk')
    index1 = data['dishes_name'].str.contains('\r\n')   #把含有\r\n的dishes_name找出来
    data.loc[index1,'dishes_name'] = data.loc[index1,
                                              'dishes_name'].str.replace('\r\n','')  #删除\r\n
    data.loc[:,'dishes_name'] = data.loc[:,'dishes_name'].str.strip()  #删除空格

    ##统计每个订单状态的占比
    order_tj = data_info['order_status'].value_counts()
    order_tj/order_tj.sum()
    # import matplotlib.pyplot as plt
    # plt.figure(figsize=(6,6))
    # plt.pie(order_tj,
    #         autopct='%.2f%%',explode=[0.3]+[0.2]+[0.1],labels=['1','0','2'],
    #         pctdistance=0.8)  #作订单状态的饼图
    # plt.title('订单状态占比')
    # plt.show()

    ##选取有效的订单数据
    #白饭并不能做为菜品推荐
    index2 = data['dishes_name'].str.contains('白饭/')   #检查出data中含有白饭/的dishes_name
    data.drop(data.loc[index2,'dishes_name'].index,inplace=True)  #删除含有白饭/的dishes_name
    data.shape
    #删除订单状态不为1的数据
    data_info.drop((data_info.loc[data_info['order_status']!=1].index),inplace=True)
    data_info.shape

    #提出对data_info的info_id、data的order_id去重后的数据
    data_info1 = data_info['info_id'].drop_duplicates()
    data1 = data['order_id'].drop_duplicates()

    #将info表中有而data表中没有，或info表中没有而data表中有的订单除去
    for i in list(data_info1):
        if i not in list(data1):
            del data_info[i]
    for j in list(data1):
        if j not in list(data_info1):
            data.drop((data.loc[(data['order_id'] == j)].index),inplace=True)
    data.shape
    #保留主要特征emp_id（用户id）和dishes_name（菜品名称）
    data_wash = data.loc[:,['emp_id','dishes_name']]
    return data_wash

