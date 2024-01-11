import pandas
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
# 样式
# plt.style.use('ggplot') 

# 读表
data1 = pd.read_csv('zhenjiang.csv')

# 画图
# 设置字体
plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号的乱码问题
plt.rcParams['axes.unicode_minus'] = False
# 读表
datalsit = pandas.read_csv('zhenjiang.csv', encoding='utf-8')

# 数据处理
# 利用split分裂字符串‘/’取出最高最低气温
datalsit['最低气温'] = datalsit['最低气温/最高气温'].str.split('/', expand=True)[0]
datalsit['最高气温'] = datalsit['最低气温/最高气温'].str.split('/', expand=True)[1]
# 取出温度中的℃符号
datalsit['最低气温'] = datalsit['最低气温'].map(lambda x: str(x.replace('℃', '')))
datalsit['最高气温'] = datalsit['最高气温'].map(lambda x: str(x.replace('℃', '')))

dates = datalsit['日期']
highs = datalsit['最高气温']
lows = datalsit['最低气温']

# 画图
# 设置可视化图形规格
fig = plt.figure(dpi=128,figsize=(10,6))
# 线形图的线条颜色粗细调整
plt.plot(dates,highs,c='red',alpha=0.5)
plt.plot(dates,lows,c='blue',alpha=0.5)
# 线条下方覆盖为蓝色
plt.fill_between(dates,highs,lows,facecolor='blue',alpha=0.2)

# 图表格式
# 设置图标的图形格式
plt.title('2023镇江市天气情况',fontsize=24)
plt.xlabel('日期',fontsize=12)
# x轴标签倾斜  默认30度 可通过rotation=30改变
fig.autofmt_xdate()
plt.ylabel('气温',fontsize=12)
# 刻度线样式设置
plt.tick_params(axis='both',which='major',labelsize=10)
# 修改刻度 数据每10组显示1个
plt.xticks(dates[::10])

plt.show()

print(" ------------------seaborn------------------------------")
# 读取数据
df = pd.read_csv("zhenjiang.csv")
# 数据清洗和类型转换
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日') #2023-01-01 2023-01-02
df[['最低气温', '最高气温']] = df['最低气温/最高气温'].str.split('/', expand=True)
df['最低气温'] = df['最低气温'].str.replace('℃', '').astype(int)
df['最高气温'] = df['最高气温'].str.replace('℃', '').astype(int)
# 使用 seaborn 设置美观的图表样式
sns.set_style('whitegrid',{'font.sans-serif':['simhei','Arial']})
# 设置画布
plt.figure(figsize=(12, 6))
# 使用 seaborn 绘制线图
sns.lineplot(x=df['日期'], y=df['最高气温'], label='最高气温', color='crimson')
sns.lineplot(x=df['日期'], y=df['最低气温'], label='最低气温', color='royalblue')
# 填充两条线之间的区域
plt.fill_between(df['日期'], df['最高气温'], df['最低气温'], color='lightgrey', alpha=0.5)
# 设置标题和标签
plt.title('2023年镇江市天气情况', fontsize=16)
plt.xlabel('日期', fontsize=14)
plt.ylabel('气温 (℃)', fontsize=14)
# 优化坐标轴刻度显示
plt.xticks(rotation=45)
plt.tight_layout()
# 显示图例
plt.legend()
# 显示图表
plt.show()
print("------------------------------pyecharts----------------------------")
from pyecharts.charts import Pie, Line, Radar # 饼图   线图 雷达图
from pyecharts import options as opts   # 图表选项
from pyecharts.globals import ThemeType # 更换主题
from pyecharts.charts import Page # 合成一个html
from collections import Counter
# 将最高气温和最低气温分割为两列，并去掉'℃'
df[['最低气温', '最高气温']] = df['最低气温/最高气温'].str.split('/', expand=True)
df['最低气温'] = df['最低气温'].str.replace('℃', '').astype(int)
df['最高气温'] = df['最高气温'].str.replace('℃', '').astype(int)
# 1.创建线图 
line_chart = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))#调用亮色主题 参考   https://pyecharts.org/
# 使用 strftime 对日期进行格式化，并转换为字符串列表
date_strings = df['日期'].dt.strftime('%m-%d').tolist()
line_chart.add_xaxis(date_strings)
line_chart.add_yaxis("最高气温", df['最高气温'].tolist(), is_smooth=True)
line_chart.add_yaxis("最低气温", df['最低气温'].tolist(), is_smooth=True)
# 设置全局选项
line_chart.set_global_opts(title_opts=opts.TitleOpts(title="2023年镇江市天气情况"),
                     xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),# x周转45^o
                     yaxis_opts=opts.AxisOpts(name="气温"),
                     legend_opts=opts.LegendOpts(is_show=True))

# 设置系列配置和样式
line_chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False),linestyle_opts=opts.LineStyleOpts(width=2))
# 2.饼图 - 天气状况
weather_conditions = df['天气状况'].value_counts().to_dict() #计算不同天气个数  
pie_chart = Pie()
pie_chart.add("", [list(z) for z in weather_conditions.items()])
pie_chart.set_global_opts(
    title_opts=opts.TitleOpts(title="天气状况分布"),
    legend_opts=opts.LegendOpts(is_show=False) # 不要图示
)
pie_chart.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

# 3.雷达图 - 风力出现次数
wind_directions = df['风力风向(夜间/白天)'].str.split('/', expand=True).stack()
wind_counts = Counter(wind_directions)

# 生成雷达图所需的数据格式
radar_data = [list(wind_counts.values())]
radar_schema = [{"name": wind, "max": max(wind_counts.values())} for wind in wind_counts.keys()]

# 创建雷达图
radar_chart = Radar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
radar_chart.add_schema(schema=radar_schema)
radar_chart.add("不同分力出现次数", radar_data, linestyle_opts=opts.LineStyleOpts(color="#f9713c", width=1))

# 设置全局配置
radar_chart.set_global_opts(title_opts=opts.TitleOpts(title="风力风向分布"))
# 创建一个 Page 实例
page = Page()
# 添加之前创建的所有图表
page.add(
    line_chart,
    pie_chart,
    radar_chart
)
# 渲染图表到一个 HTML 文件
page.render("charts.html")