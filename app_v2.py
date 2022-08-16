import streamlit as st
import pandas as pd
import codecs
from pandas_profiling import ProfileReport
import time
from streamlit_lottie import st_lottie
import json
import klib
import requests
import numpy as np
from st_aggrid import AgGrid

import streamlit.components.v1 as components
from streamlit_pandas_profiling import st_profile_report

#Custom components
import sweetviz as sv
import os

st.config.set_option("server.maxUploadSize", 10000)

def st_display_sweetviz(report_html, width=2000, height= 1000):
    report_file = codecs.open(report_html, 'r')
    page = report_file.read()
    components.html(page, width= width, height=height, scrolling=True)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


st.set_page_config(layout='wide')

st.cache(allow_output_mutation=True)
def main():
    #Headers
    with st.container():
        st.title('Descriptive Analytics Tool')

    #Description of the tool
    with st.container():
        st.write('---')
        left_column, right_column = st.columns(2)
        with left_column:
            st.header('How to use the tool')
            st.write('##')
            st.write(
            '''
            This tool is designed to help provide a high-level overview of your dataset, it will help you analyse the following:
            - Null Values
            - Duplication
            - Distribution chart to help visualise the data
            - Correlation Analysis
            - Interaction within variables

            To use the tool:
            - Simply upload any CSV file
            - You would get 3 check boxes to view / evaluate your data:
            1) You would have an option to view the dataframe
            2) You would have an option to view the data types in the dataframe
            3) You would have the option to convert the data type for "date", if your dataset has that column (Only use this option if you have a date dimension in the dataset)
            - Once you have made your selection click on generate report

            '''
            )
        with right_column:
            lottie_hello = load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_hx7ddrx9.json')
            st_lottie(
            lottie_hello,
            speed=1,
            height = 600,
            key='coding'
            )

    with st.container():
        st.write('---')

        data_file = st.file_uploader("Upload Your CSV", type=['CSV'])

        if data_file is not None:
            df = pd.read_csv(data_file)
            check_dataframe = st.checkbox('View dataframe')

            if check_dataframe:
                AgGrid(df)

            #viewing the datatypes
            view_datatype = st.checkbox('View data type')
            if view_datatype:
                df_1 = df.dtypes
                st.markdown(''' Here is an overview of your datatypes in the dataset''')
                st.dataframe(df_1.astype(str))


            # if date column exist in dataset the convert to date time
            date_exist = st.checkbox('Only check this box if you have a date dimension in the dataset')
            if date_exist:
                df.columns = df.columns.str.lower() #making all column header lower case
                df['date'] = pd.to_datetime(df['date'])
                st.dataframe(df.head(1))

            # We can pick up the processed data with converted date columns and generate report
            profile = ProfileReport(df)
            if st.button("Generate Report"):
                st_profile_report(profile)


if __name__=='__main__':
    main()
