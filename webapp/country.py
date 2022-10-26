import streamlit as st
import pandas as pd
import io

buffer = io.BytesIO()

def run_app():

    df = pd.read_csv("puki.csv")
    legend = pd.read_csv("legend.csv")

    # Dropdown para elegir país
    option = st.selectbox(
        'Select a country',
        df['Country'].unique(),
        index = 6)

    # Slider para elegir años
    values = st.slider(
        'Select a range of years',
        1974, 2021, (1974, 2021))

    # Dataframe que se queda con solo el país elegido en los años elegidos
    df_temp = df.loc[(df['Country'] == option) & (df['Year'] <= values[1]) &
     (df['Year'] >= values[0])][['Year','3-way','5-way','Reference Currency']] #'Final Classification' no incluído

    title = "Exchange Rate Regime of " + option
    st.markdown('### ' + title)

    col1, col2 = st.columns([1,3.5])

    with col1:
        csv1 = df_temp.to_csv(index=0)

        st.download_button(
        label = "Download as CSV",
        data = csv1,
        file_name = option + '.csv',
        mime = 'text/csv',
        )

    with col2:
        with open("puki.csv", "rb") as file:
            st.download_button(
            label="Download whole database as CSV",
            data=file,
            file_name = 'LYSclassification.csv',
            mime='text/csv'
            )

    # Para ocultar el nro de fila en el output
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
    st.sidebar.table(legend.iloc[1: , :])
