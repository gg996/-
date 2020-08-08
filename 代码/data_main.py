
import pandas as pd
import numpy as np
from 餐饮智能推荐服务.data_traintest import traintest #导入前一个脚本的自定义函数
from 餐饮智能推荐服务.data_processing import process
data = process('meal_order_detail.csv','meal_order_info.csv')  #用自定义函数获取emp_id,dishes_name
datatr,datate = traintest(data,3) #读取除去了只点过3次菜的用户id的数据
# datatr.to_csv('H:/1706/线上实习/训练集数据.csv')
# datate.to_csv('H:/1706/线上实习/测试集数据.csv')

##构建训练集数据客户-菜品二元矩阵
id_train = list(set(datatr['emp_id']))   #对训练集datatr的用户id进行集合唯一性去重
dishes_train = list(set(datatr['dishes_name']))   #对训练集datatr的菜品名称进行集合唯一性去重
#建立值为0，行索引为去重后的用户id，列索引为去重后的菜品名称的数据框
ter = pd.DataFrame(0, index=id_train, columns=dishes_train)
#把用户点过的菜品在数据框中的值转换为1
for i in datatr.index:
    ter.loc[datatr.loc[i, 'emp_id'], datatr.loc[i, 'dishes_name']] = 1
# ter.to_csv('H:/1706/线上实习/客户-菜品二元矩阵.csv')


## 构建测试集用户id点菜的字典
id_test = list(set(datate['emp_id']))   #对测试集的emp_id去重
dict_ter = {id: list(datate.loc[datate['emp_id'] == id, 'dishes_name']) for id in id_test}



##利用jaccard相似系数构建物品相似度函数矩阵
def jaccard(data=None):
    '''
    构建物品相似度矩阵(杰卡德相似系数)
    :param data: 用户物品矩阵,0-1矩阵;行为用户,列为物品
    :return: jaccard相似系数矩阵
    '''
    te = -(data - 1)  # 将用户物品矩阵的值反转
    dot1 = np.dot(data.T, data)  # 任意两菜品同时被点次数
    dot2 = np.dot(te.T, data)  # 任意两个菜品中只有一个被点的次数（上三角表示前一个被点，下三角表示后一个被点）
    dot3 = dot2.T + dot2  # 任意两个菜品中随意一个被点的次数
    cor = dot1 / (dot3 -dot1)  # 杰卡德相似系数公式
    for i in range(len(cor)):  # 将对角线值处理为零
        cor[i, i] = 0
    return cor
cor = jaccard(ter)
cor = pd.DataFrame(cor, index=dishes_train, columns=dishes_train)  #构建物品相似度矩阵
# cor.to_csv('H:/1706/线上实习/jaccard系数的相似度矩阵.csv')

##同现计算相似度矩阵
def Cooccurrence(data=None):
    te = -(data - 1)  # 将用户物品矩阵的值反转
    dot1 = np.dot(data.T, data)  # 任意两菜品同时被点次数
    dot2 = np.dot(te.T, data)  # 任意两个菜品中只有一个被点的次数（上三角表示前一个被点，下三角表示后一个被点）
    cor1 = dot1 / np.sqrt(dot2 * dot2.T)  # 同现相似度计算
    for i in range(len(cor)):  # 将对角线值处理为零
        cor1[i, i] = 0
    return cor1
cor1 = Cooccurrence(ter)
cor1 = pd.DataFrame(cor1, index=dishes_train, columns=dishes_train)
# cor1.to_csv('H:/1706/线上实习/同现相似度矩阵.csv')

    ##开始推荐,rem第一列为测试集用户id,第二列为用户已点过的菜品,第三列为相应推荐菜品,第四列为推荐是否有效
rem = pd.DataFrame(index=range(len(datate)), columns=['id', 'dishes_name', 'dish', 'T/F'])
rem['id'] = list(datate['emp_id'])  #在id列加入datate的emp_id
rem['dishes_name'] = list(datate['dishes_name'])  #在dishes_name列加入datate的dishes_name


for i in rem.index:
    if rem.loc[i, 'dishes_name'] in dishes_train:
        rem.loc[i, 'dish'] = cor.loc[rem.loc[i, 'dishes_name'], :].idxmax()  # 推荐的菜品
        rem.loc[i, 'T/F'] = rem.loc[i, 'dish'] in dict_ter[rem.loc[i, 'id']]  # 判定推荐是否准确
# rem.to_csv('H:/1706/线上实习/jaccard系数的推荐表.csv')
# rem.to_csv('H:/1706/线上实习/同现相似度的推荐表.csv')

sum(rem['T/F'] == True) / (len(rem) - sum(rem['T/F'] == 'NAN'))  #模型评价



