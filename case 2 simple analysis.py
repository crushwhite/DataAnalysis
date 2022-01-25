import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
# 导入csv文件
fp = pd.read_csv(r'F:\pythonProject\空气质量.csv', encoding='gbk')
# 将北京天津的数据区分开
fp1 = fp[fp['城市'] == '天津']
fp2 = fp[fp['城市'] == '北京']
print(fp1.info(), fp2.info())
# 运行结果如下
'''<class 'pandas.core.frame.DataFrame'>
RangeIndex: 98 entries, 0 to 97
Data columns (total 9 columns):
 #   Column  Non-Null Count  D type  
---  ------  --------------  -----  
 0   日期      98 non-null     object 
 1   AQI     98 non-null     int64  
 2   质量等级    90 non-null     object 
 3   PM2.5   98 non-null     int64  
 4   PM10    98 non-null     int64  
 5   NO2     98 non-null     int64  
 6   CO      98 non-null     float64
 7   SO2     98 non-null     float64
 8   O3_8h   98 non-null     int64  
dtypes: float64(2), int64(5), object(2)
memory usage: 7.0+ KB
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 98 entries, 0 to 97
Data columns (total 9 columns):
 #   Column  Non-Null Count  D type  
---  ------  --------------  -----  
 0   日期      98 non-null     object 
 1   AQI     98 non-null     int64  
 2   质量等级    95 non-null     object 
 3   PM2.5   98 non-null     int64  
 4   PM10    98 non-null     int64  
 5   SO2     98 non-null     float64
 6   NO2     98 non-null     float64
 7   CO      98 non-null     float64
 8   O3_8h   98 non-null     int64  
dtypes: float64(3), int64(4), object(2)
memory usage: 7.0+ KB
None None'''
# 由此可以看出在质量等级这一列有部分缺失值
# 查询得到可以通过AQI得到质量等级
'''0 - 50一级（优）;51 -100二级（良）;101-150三级（轻度污染）;151-200四级（中度污染）;201-300五级（重度污染）;300+六级（严重污染）'''


def value_change(column1, column2, file):
    file = file.copy()
    # 定义一个数据处理函数，通过column1的值的判断来改变column2的值
    a = 0
    lst = list(file[column1].index)
    # 获取column1 的索引
    for i in file[column1]:
        if (i > 0) and (i <= 50):
            file.loc[lst[a], column2] = '优'
        elif (i >= 51) and (i <= 100):
            file.loc[lst[a], column2] = '良'
        elif (i >= 101) and (i <= 150):
            file.loc[lst[a], column2] = '轻度污染'
        elif (i >= 151) and (i < 200):
            file.loc[lst[a], column2] = '中度污染'
        elif (i >= 201) and (i <= 300):
            file.loc[lst[a], column2] = '重度污染'
        else:
            file.loc[lst[a], column2] = np.nan
        a += 1
    return file


fp1 = value_change('AQI', '质量等级', file=fp1)
fp2 = value_change('AQI', '质量等级', file=fp2)
print(fp1.info(), fp2.info())
'''<class 'pandas.core.frame.DataFrame'>
RangeIndex: 98 entries, 0 to 97
Data columns (total 9 columns):
 #   Column  Non-Null Count  D type  
---  ------  --------------  -----  
 0   日期      98 non-null     object 
 1   AQI     98 non-null     int64  
 2   质量等级    98 non-null     object 
 3   PM2.5   98 non-null     int64  
 4   PM10    98 non-null     int64  
 5   NO2     98 non-null     int64  
 6   CO      98 non-null     float64
 7   SO2     98 non-null     float64
 8   O3_8h   98 non-null     int64  
dtypes: float64(2), int64(5), object(2)
memory usage: 7.0+ KB
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 98 entries, 0 to 97
Data columns (total 9 columns):
 #   Column  Non-Null Count  D type  
---  ------  --------------  -----  
 0   日期      98 non-null     object 
 1   AQI     98 non-null     int64  
 2   质量等级    98 non-null     object 
 3   PM2.5   98 non-null     int64  
 4   PM10    98 non-null     int64  
 5   SO2     98 non-null     float64
 6   NO2     98 non-null     float64
 7   CO      98 non-null     float64
 8   O3_8h   98 non-null     int64  
dtypes: float64(3), int64(4), object(2)
memory usage: 7.0+ KB
None None'''
# 对质量等级分组
fp1_group = fp1.groupby(by='质量等级')
fp2_group = fp1.groupby(by='质量等级')
# 利用len函数得到九月到十二月七日中各个质量等级对应的天数
fp1_group_quality = fp1_group.agg(len)
fp2_group_quality = fp1_group.agg(len)
# 去除其他列仅保留一列方便自己查看
fp1_group_quality.drop(fp1_group_quality.iloc[:, 1::], axis=1, inplace=True)
fp1_group_quality_1 = fp1_group_quality.rename(columns={'日期': '天数'})
print(fp1_group_quality_1)
'''     天数
质量等级    
中度污染   3
优     23
良     55
轻度污染  15
重度污染   1'''
fp2_group_quality.drop(fp2_group_quality.iloc[:, 1::], axis=1, inplace=True)
fp2_group_quality_1 = fp2_group_quality.rename(columns={'日期': '天数'})
print(fp2_group_quality_1)
'''      天数
质量等级    
中度污染   3
优     24
良     55
轻度污染  15
重度污染   1
'''


def lst_va_change(lst):
    first_lst = []
    for i in lst:
        i = i.replace('(', '')
        i = i.replace(')', '')
        i = i.replace(',', '')
        i = i.replace('\'', '')
        first_lst.append(i)
    return first_lst


# 去除字符串的（,'以求美观


def pie_draw(y, name, file):
    # 设置一个画饼图的函数
    lst = [str(i) for i in file.index]
    label = lst_va_change(lst)
    # 绘图
    plt.pie(x=file[y], labels=label, autopct='%.2f', textprops={'fontsize': '10', 'color': 'k'})
    # 添加标题
    plt.title(name)


def two_pie_draw(y, name1, name2, name3, file1, file2):
    # 设置中文字体
    font = {'family': 'MicroSoft YaHei',
            'size': '12'}
    matplotlib.rc('font', **font)
    plt.figure(figsize=(20, 8), dpi=80)
    plt.subplot(1, 2, 1)
    pie_draw(y, name1, file1)
    plt.subplot(1, 2, 2)
    pie_draw(y, name2, file2)
    # 保存图片
    plt.savefig(r'C:\Users\HP\Desktop\{}.png'.format(name3))
    plt.show()


two_pie_draw('天数', r'天津9/1-12/7空气质量', r'北京9/1-12/7空气质量', '北京天津两市空气质量对比（总）', fp1_group_quality_1,
             fp2_group_quality_1)
# 为了不改变fp1，fp2将其进行新的赋值
new_fp1 = fp1.copy()
new_fp2 = fp2.copy()
# 对new_fp1,new_fp2的日期进行处理方便分组
new_fp1['日期'] = new_fp1['日期'].apply(lambda x: x.split('/')[1] + '月')
new_fp2['日期'] = new_fp2['日期'].apply(lambda x: x.split('/')[1] + '月')
# 对日期进行分组
new_fp1_group = new_fp1.groupby(by='日期')
new_fp2_group = new_fp2.groupby(by='日期')
# 对数据求平均值
new_fp1_group_mean = new_fp1_group.agg('mean')
new_fp2_group_mean = new_fp2_group.agg('mean')
# 利用已设置的函数将AQI变成质量等级
new_fp1_group_mean = value_change(column1='AQI', column2='AQI', file=new_fp1_group_mean)
new_fp1_group_mean.loc[:, 'sort'] = [2, 3, 4, 1]
new_fp1_group_mean = new_fp1_group_mean.sort_values(by='sort')
print(new_fp1_group_mean)
'''  AQI      PM2.5       PM10        NO2         CO       SO2      O3_8h  sort
日期                                                                            
9月    良  55.366667  55.933333  63.600000  46.200000  1.023333  58.733333     1
10月   良  66.166667  71.666667  66.733333  54.800000  1.000000  55.366667     2
11月   良  47.366667  87.200000  47.900000   0.910000  9.500000  43.600000     3
12月   良  63.571429  75.571429  86.571429  64.714286  1.142857  62.000000     4
'''
new_fp2_group_mean = value_change(column1='AQI', column2='AQI', file=new_fp2_group_mean)
new_fp2_group_mean.loc[:, 'sort'] = [2, 3, 4, 1]
new_fp2_group_mean = new_fp2_group_mean.sort_values(by='sort')
print(new_fp2_group_mean)
'''  AQI      PM2.5       PM10        SO2        NO2         CO      O3_8h  sort
日期                                                                             
9月    良  18.233333  36.200000   2.533333  20.566667   0.630000  98.533333     1
10月   优  62.774194  66.387097  54.774194   1.000000  56.612903  60.032258     2
11月   良  44.100000  64.733333   0.643333   2.700000  35.533333  41.700000     3
12月   优  49.428571  49.285714  74.714286  60.142857   1.385714  48.857143     4
'''
# 在此处绘制直方图将天津市PM2.5,PM10,NO2,CO,SO2,O3月平均含量表示出来
# 设置中文字体
font = {'family': 'MicroSoft YaHei',
        'size': '12'}
matplotlib.rc('font', **font)
# 设置x的刻度
_x = ['9月', '', '10月', '', '11月', '', '12月']
# 设置y
y_pm25 = new_fp1_group_mean['PM2.5']
y_pm10 = new_fp1_group_mean['PM10']
y_no2 = new_fp1_group_mean['NO2']
y_co = new_fp1_group_mean['CO']
y_so2 = new_fp1_group_mean['SO2']
y_o3 = new_fp1_group_mean['O3_8h']

y2_pm25 = new_fp2_group_mean['PM2.5']
y2_pm10 = new_fp2_group_mean['PM10']
y2_no2 = new_fp2_group_mean['NO2']
y2_co = new_fp2_group_mean['CO']
y2_so2 = new_fp2_group_mean['SO2']
y2_o3 = new_fp2_group_mean['O3_8h']
# 设置图片大小
plt.figure(figsize=(20, 8), dpi=80)
# 多次绘图将PM2.5,PM10,NO2,CO,SO2,O3月平均含量均在图中画出来
plt.bar(range(3, 34, 10), y_co, label='天津', color='g', alpha=0.5)
plt.bar(range(4, 35, 10), y_so2, color='g', alpha=0.5)
plt.bar(range(5, 36, 10), y_o3, color='g', alpha=0.5)
plt.bar(range(6, 37, 10), y_no2, color='g', alpha=0.5)
plt.bar(range(7, 38, 10), y_pm10, color='g', alpha=0.5)
plt.bar(range(8, 39, 10), y_pm25, color='g', alpha=0.5)

plt.bar(range(3, 34, 10), y2_co, label='北京', color='y', alpha=0.5)
plt.bar(range(4, 35, 10), y2_so2, color='y', alpha=0.5)
plt.bar(range(5, 36, 10), y2_o3, color='y', alpha=0.5)
plt.bar(range(6, 37, 10), y2_no2, color='y', alpha=0.5)
plt.bar(range(7, 38, 10), y2_pm10, color='y', alpha=0.5)
plt.bar(range(8, 39, 10), y2_pm25, color='y', alpha=0.5)
# 设置xy轴刻度
plt.xticks(range(5, 36, 5), _x)
plt.yticks(range(0, 102, 3))
# 添加描述信息
plt.xlabel('月份(从左到右依次为CO,SO2,O3,NO2,PM10,PM2.5)')
plt.ylabel('浓度μg/m3（CO为mg/m3）')
plt.title('北京天津PM2.5,PM10,NO2,CO,SO2,O3月平均含量')
# 设置网格
plt.grid(alpha=0.4)
# 设置图例
plt.legend(loc='upper left')
plt.savefig(r'C:\Users\HP\Desktop\北京天津PM2.5,PM10,NO2,CO,SO2,O3月平均含量.png')
plt.show()

# 对日期和质量等级分组
ano_new_fp1_group = new_fp1.groupby(by=['日期', '质量等级'])
ano_new_fp1_group = ano_new_fp1_group.agg(len)
ano_new_fp2_group = new_fp2.groupby(by=['日期', '质量等级'])
ano_new_fp2_group = ano_new_fp2_group.agg(len)
# 对数据进行简单处理让其直观
ano_new_fp1_group.drop(ano_new_fp1_group.iloc[:, 1::], axis=1, inplace=True)
ano_new_fp1_group = ano_new_fp1_group.rename(columns={'AQI': '天数'})
print(ano_new_fp1_group)
'''         天数
日期  质量等级    
10月 中度污染   2
    优      8
    良     18
    轻度污染   1
    重度污染   1
11月 中度污染   1
    优      7
    良     15
    轻度污染   7
12月 良      6
    轻度污染   1
9月  优      8
    良     16
    轻度污染   6'''

ano_new_fp2_group.drop(ano_new_fp2_group.iloc[:, 1::], axis=1, inplace=True)
ano_new_fp2_group = ano_new_fp2_group.rename(columns={'AQI': '天数'})
print(ano_new_fp2_group)
'''         天数
日期  质量等级    
10月 中度污染   1
    优     19
    良     10
    轻度污染   1
11月 中度污染   2
    优      9
    良     14
    轻度污染   5
12月 优      5
    良      2
9月  优     17
    良     10
    轻度污染   3
'''
two_pie_draw('天数', r'天津9,10,11,12月空气质量', r'北京9,10,11,12月空气质量', '北京天津两市空气质量对比（分）', ano_new_fp1_group,
             ano_new_fp2_group)
# 对天津市9，10，11，12月的数据进行分析得出以上结论

# 开始绘图，初步分析数据，绘制折线图较为直观。
# 定义一个函数绘制该折线图


def draw_api(x, y, name, file1, file2):
    # 设置中文字体
    font = {'family': 'MicroSoft YaHei',
            'size': '12'}
    matplotlib.rc('font', **font)
    # 设置图片大小
    plt.figure(figsize=(27, 20), dpi=80)
    x_zhou = range(2, 2*len(fp1[x]) + 2, 2)
    y1_zhou = file1[y]
    y2_zhou = file2[y]
    plt.plot(x_zhou, y1_zhou, label='天津')
    plt.plot(x_zhou, y2_zhou, label='北京')
    # 设置x，y轴刻度
    x_ticks = file1[x].agg(lambda a: a.replace('2021/', ''))
    plt.xticks(x_zhou, x_ticks, rotation=60)
    lst = [min(y1_zhou), max(y1_zhou), min(y2_zhou), max(y2_zhou)]
    y_ticks = range(min(lst), max(lst) + 1, 4)
    plt.yticks(y_ticks)
    # 添加描述信息
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(name)
    # 添加网格
    plt.grid(visible=True)
    # 设置图例
    plt.legend(loc='upper left')
    plt.savefig(r'C:\Users\HP\Desktop\{}.png'.format(name))
    plt.show()


draw_api('日期', 'AQI', 'AQI折线图', file1=fp1, file2=fp2)

# 绘制天津市9/1-12/7日每天的各个物质的浓度
# 设置x的刻度
fp1_x_ = fp1['日期'].agg(lambda a: a.replace('2021/', ''))
fp1_y_pm25 = fp1['PM2.5']
fp1_y_pm10 = fp1['PM10']
fp1_y_no2 = fp1['NO2']
fp1_y_co = fp1['CO']
fp1_y_so2 = fp1['SO2']
fp1_y_o3 = fp1['O3_8h']
# 设置图片大小
plt.figure(figsize=(27, 20), dpi=80)
# 多次绘图将PM2.5,PM10,NO2,CO,SO2,O3月平均含量均在图中画出来
plt.plot(fp1_x_, fp1_y_co, label='CO')
plt.plot(fp1_x_, fp1_y_so2, label='SO2')
plt.plot(fp1_x_, fp1_y_o3, label='O3')
plt.plot(fp1_x_, fp1_y_no2, label='NO2')
plt.plot(fp1_x_, fp1_y_pm10, label='PM10')
plt.plot(fp1_x_, fp1_y_pm25, label='PM25')
# 设置XY轴
plt.xticks(rotation=60)
plt.yticks(range(0, 200, 4))
# 添加描述信息
plt.xlabel('日期', fontsize=12)
plt.ylabel('浓度μg/m3（CO为mg/m3）', fontsize=12)
plt.title('天津市每日PM2.5,PM10,NO2,CO,SO2,O3含量', fontsize=12)
# 设置网格
plt.grid(alpha=0.4)
# 设置图例
plt.legend(loc='upper left')
plt.savefig(r'C:\Users\HP\Desktop\天津PM2.5,PM10,NO2,CO,SO2,O3日含量.png')
plt.show()


# 绘制北京市9/1-12/7日每天的各个物质的浓度
# 设置x的刻度
fp2_x_ = fp2['日期'].agg(lambda a: a.replace('2021/', ''))
fp2_y_pm25 = fp2['PM2.5']
fp2_y_pm10 = fp2['PM10']
fp2_y_no2 = fp2['NO2']
fp2_y_co = fp2['CO']
fp2_y_so2 = fp2['SO2']
fp2_y_o3 = fp2['O3_8h']
# 设置图片大小
plt.figure(figsize=(27, 20), dpi=80)
# 多次绘图将PM2.5,PM10,NO2,CO,SO2,O3月平均含量均在图中画出来
plt.plot(fp2_x_, fp2_y_co, label='CO')
plt.plot(fp2_x_, fp2_y_so2, label='SO2')
plt.plot(fp2_x_, fp2_y_o3, label='O3')
plt.plot(fp2_x_, fp2_y_no2, label='NO2')
plt.plot(fp2_x_, fp2_y_pm10, label='PM10')
plt.plot(fp2_x_, fp2_y_pm25, label='PM25')
# 设置XY轴
plt.xticks(rotation=60)
plt.yticks(range(0, 200, 4))
# 添加描述信息
plt.xlabel('日期', fontsize=12)
plt.ylabel('浓度μg/m3（CO为mg/m3）', fontsize=12)
plt.title('北京市每日PM2.5,PM10,NO2,CO,SO2,O3含量', fontsize=12)
# 设置网格
plt.grid(alpha=0.4)
# 设置图例
plt.legend(loc='upper left')
plt.savefig(r'C:\Users\HP\Desktop\北京PM2.5,PM10,NO2,CO,SO2,O3日含量.png')
plt.show()

'''
反思：
1.数据问题
找到的数据与所学营销专业并无太大关联，仅仅是凭自己的兴趣找的这组数，这组数据相对简单，数据内容少，数据处理过程相对简单，难度较低。
2.写代码时遇到的问题
在导入文件时出现了部分未见过的问题：
（1.文件编码问题UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd0 in position 0: invalid continuation byte
（2.csv文件打开错误_csv.Error: line contains NULL byte
解决办法
（1.utf-8没办法成功换用gbk
（2.csv文件打开错误是由于保存时扩展名为xls或xlsx,而将其改为csv文件，因此将文件另存为
csv文件即可。
在绘图时，
汉字无法在图中显示出来，使用matplotlib.rc函数声明字体
折线图：因为xy轴刻度太过密集无法看清，改变y轴刻度步长，将x轴刻度删除不必要的内容并进行
旋转
饼状图：由于部分内容占比太少导致文字重合，暂未找到好的方法解决
'''