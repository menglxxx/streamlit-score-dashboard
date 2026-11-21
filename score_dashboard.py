import streamlit as st
import pandas as pd
import plotly.express as px

# ===================== 任务2：模拟数据集 =====================
data = {
    "班级":["一班","一班","一班","二班","二班","二班","三班","三班","三班","一班","二班","三班"],
    "姓名":["甲","乙","丙","丁","戊","己","庚","辛","壬","癸","子","丑"],
    "语文":[85,72,90,66,88,79,92,58,77,81,75,86],
    "数学":[92,68,83,75,94,62,88,70,55,80,73,91],
    "英语":[78,84,89,69,82,74,90,65,71,83,77,85]
}
df = pd.DataFrame(data)
# 预处理：新增总分
df["总分"] = df["语文"] + df["数学"] + df["英语"]

# ===================== 任务1：页面布局 =====================
st.set_page_config(page_title="学生成绩看板",layout="wide")
st.title("📊 班级学生成绩统计看板")

# 筛选组件【进阶2】
class_list = ["全部"] + df["班级"].unique().tolist()
selected_class = st.sidebar.selectbox("选择班级", class_list)
if selected_class != "全部":
    df_filter = df[df["班级"] == selected_class]
else:
    df_filter = df

# ===================== 任务3：数据卡片指标 =====================
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.metric("学生总数", len(df_filter))
with col2:
    st.metric("平均分", round(df_filter["总分"].mean(),2))
with col3:
    st.metric("最高分", df_filter["总分"].max())
with col4:
    st.metric("最低分", df_filter["总分"].min())

# ===================== 任务3：3种图表 =====================
colA,colB = st.columns(2)
# 柱状图：各班平均分对比
with colA:
    st.subheader("各科平均分柱状图")
    sub_df = df_filter[["语文","数学","英语"]].mean().reset_index()
    sub_df.columns=["科目","分数"]
    fig_bar = px.bar(sub_df, x="科目",y="分数",color="科目",range_y=[0,100])
    st.plotly_chart(fig_bar,use_container_width=True)

# 折线图：学生总分分布趋势
with colB:
    st.subheader("学生总分折线图")
    fig_line = px.line(df_filter, x="姓名",y="总分",markers=True)
    st.plotly_chart(fig_line,use_container_width=True)

# 饼图：班级人数占比
st.subheader("班级人数占比饼图")
pie_df = df.groupby("班级").size().reset_index(name="人数")
fig_pie = px.pie(pie_df,names="班级",values="人数")
st.plotly_chart(fig_pie,use_container_width=True)

# 明细表格
st.subheader("明细数据表")
st.dataframe(df_filter,use_container_width=True)
