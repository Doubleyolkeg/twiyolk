import os
import pandas as pd
import numpy as np

def calculate_BrayCurtis(array1, array2):
    # 计算两个数组的布雷柯蒂斯距离
    numerator = np.sum(np.abs(array1 - array2))
    denominator = np.sum(array1) + np.sum(array2)
    bray = numerator / denominator
    return bray


if __name__ == '__main__':
    path = r'D:\work\VOCs相似度方法比较\相似度计算20250401\相似度源数据20250401.xlsx'
    data1 = pd.read_excel(path, sheet_name='异味')
    data2 = pd.read_excel(path, sheet_name='VOC')
    # nan置0
    data1.fillna(0, inplace=True)
    data2.fillna(0, inplace=True)
    # split data1和data2，C到BP和BQ到CJ
    data1_1 = data1.iloc[:, 3:145]
    data1_2 = data1.iloc[:, 145:]
    data2_1 = data2.iloc[:, 3:146]
    data2_2 = data2.iloc[:, 146:]
    data_1_row_columns = data1_1.columns
    data_1_col_columns = data1_2.columns
    data_2_row_columns = data2_1.columns
    data_2_col_columns = data2_2.columns
    data1_1 = data1_1.values
    data1_2 = data1_2.values
    data2_1 = data2_1.values
    data2_2 = data2_2.values
    # 归一化，每列都除以该列的最大值
    data1_1 = data1_1 / data1_1.max(axis=0)
    data1_2 = data1_2 / data1_2.max(axis=0)
    data2_1 = data2_1 / data2_1.max(axis=0)
    data2_2 = data2_2 / data2_2.max(axis=0)
    # 计算data1_1和data1_2的相似度，用布雷柯蒂斯距离
    similarity1 = np.zeros((len(data_1_row_columns), len(data_1_col_columns)))
    similarity2 = np.zeros((len(data_2_row_columns), len(data_2_col_columns)))
    for i in range(len(data_1_row_columns)):
        for j in range(len(data_1_col_columns)):
            similarity1[i, j] = 1 - calculate_BrayCurtis(data1_1[:, i], data1_2[:, j])

    for i in range(len(data_2_row_columns)):
        for j in range(len(data_2_col_columns)):
            similarity2[i, j] = 1 - calculate_BrayCurtis(data2_1[:, i], data2_2[:, j])

    # 保存相似度矩阵,分两个sheet存到1个excel中
    similarity1_df = pd.DataFrame(similarity1, index=data_1_row_columns, columns=data_1_col_columns)
    similarity2_df = pd.DataFrame(similarity2, index=data_2_row_columns, columns=data_2_col_columns)
    with pd.ExcelWriter(r'D:\work\VOCs相似度方法比较\相似度计算20250401\相似度结果20250401.xlsx') as writer:
        similarity1_df.to_excel(writer, sheet_name='异味相似度')
        similarity2_df.to_excel(writer, sheet_name='VOC相似度')
    print('相似度矩阵已保存到D:\work\VOCs相似度方法比较\相似度计算20250401\相似度结果20250401.xlsx')






    print('-')

