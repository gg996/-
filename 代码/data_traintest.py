

from 餐饮智能推荐服务.data_processing import process
data = process('meal_order_detail.csv','meal_order_info.csv')  #用自定义函数获取emp_id,dishes_name
# data.to_csv('H:/1706/线上实习/data_wash.csv')


def traintest(data,n):
    data_index = data['emp_id'].value_counts()   #找出emp_id的频数统计
    data_index1 = data_index[data_index> n].index #找出emp_id频数大于3的索引

    from random import sample
    #按用户id来划分训练集（80%）和测试集（20%）
    idTrain = sample(list(data_index1), int(len(data_index1) * 0.8))  # 训练集用户
    idTest = [i for i in list(data_index1) if i not in idTrain]  # 测试集用户


    index_tr = [i in idTrain for i in data['emp_id']]  # 训练用户订单记录索引
    index_te = [i in idTest for i in data['emp_id']]  # 测试用户订单记录索引

    dataTrain = data[index_tr]  # 训练集数据
    dataTest = data[index_te]  # 测试集数据
    return dataTrain,dataTest

