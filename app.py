from langchain.chains import create_tagging_chain_pydantic
from langchain.chat_models import ChatOpenAI
from enum import Enum
from pydantic import BaseModel, Field
import streamlit as st
import pandas as pd
import os


def show_chart(chartType, column, df_now):
    if chartType == "bar_chart":
        st.bar_chart(df_now, x=column)
    elif chartType == "area_chart":
        st.area_chart(df_now, x=column)
    elif chartType == "line_chart":
        st.line_chart(df_now, x=column)
    elif chartType == "scatter_chart":
        # For scatter_chart, explicitly select the x and y columns
        if len(df_now.columns) > 20:
            st.scatter_chart(df_now,  y=df_now[20].values)
    return True


df_now = None
text_input = ''
openai_api_key = ''

st.title("AI Chart Generator")

# Add an input field for the user to enter their OpenAI API key
openai_api_key = st.text_input("Enter your OpenAI API key", "")

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

os.environ["OPENAI_API_KEY"] = st.secrets['open_api_key']

uploaded_file = st.file_uploader("Choose a dataset file", type=['csv'])
if uploaded_file is not None:
    df_now = pd.read_csv(uploaded_file)
    st.dataframe(df_now, use_container_width=True)
if df_now is None:
    st.stop()

with st.container:
    example_file = st.selectbox(
        'Select example dataset?',
        ('continuous_voltage_data.csv', 'monthly_statues_data.csv', 'regional_sales_data.csv'))
    df_now = pd.read_csv(example_file)
    st.dataframe(df_now, use_container_width=True)




text_input = df_now.to_string()


class DataFeature(BaseModel):
    chartType: str = Field(...,
                           enum=["scatter_chart", "bar_chart",
                                 "area_chart", "line_chart"],
                           description="""
        the chart type to visualize the dataframe strictly following rules:
        Use 'scatter_chart': if the dataframe contains categorical data many values with mixed types or if the  dataframe contains numerical data with multiple dimensions.

        Use 'scatter_chart' if the dataframe has more than 10 columns or if the dataframe has more than 3 diffrerent data types

        Use 'area_chart': if the dataframe is monthly-basis, daily-basis, or yearly-basis or if the dataframe shows changes over time, such as sales growth or customer churn or if dataframe shows comparisons between different categories.

        Use 'bar_chart': if the dataframe contains categorical data with related types, such as product categories or customer demographics or if the dataframe shows comparisons between different categories.

        Use 'line_chart': if the dataframe is seconds-basis or smaller periods, such as stock prices or website traffic or the dataframe shows comparisons between different categories.

        Use 'scatter_chart' if the data provided doesn't match any of the above criteria
     """)
    column: str = Field(...,
                        description="""
        the column name in the dataframe that is best for the x-axis
        """)


llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

tagging_chain = create_tagging_chain_pydantic(DataFeature, llm)
res = tagging_chain.run(text_input)

show_chart(res.chartType, res.column, df_now)
