import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

def run_app():

    df = pd.read_csv("puki.csv")
    legend = pd.read_csv("legend.csv")

    option = st.selectbox(
        'Select a country',
        df['Country'].unique())

    values = st.slider(
        'Select a range of years',
        1974, 2021, (1974, 2021))



    title = "Exchange Rate Regime of " + option
    st.markdown('### ' + title)

     #& df['Year'] < values[1] & df['Year'] > values[0]
    df_temp = df.loc[(df['Country'] == option) & (df['Year'] <= values[1]) & (df['Year'] >= values[0])][['Year','Final Classification','3-way','5-way']]

    # Para ocultar el nro de fila
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # Display a static table
    st.table(df_temp.sort_values(by=['Year'], ascending=False))

    st.sidebar.markdown('### Legend:')
    st.sidebar.write('5-way Classification: Fix, Crawling Peg, Dirty Float, Float, OVM,NON')
    st.sidebar.write('3-way Classification: Fix, Interm, Float, OVM,NON')
    st.sidebar.table(legend.iloc[2: , :])
