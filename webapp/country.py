import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import plotly.express as px

def run_app():


    df_z = pd.read_csv("cluster1.csv", encoding='latin-1')

    # Create an interactive 3D scatter plot using Plotly
    #fig = px.scatter_3d(df_z[df_z['Country'] == 'United States'], x='ER.Abs.Change.AVG', y='Avg.Delta.Reserves', z='ER.Volatility.Changes', color='Cluster', hover_data=['Country.Year'])
    fig = px.scatter_3d(df_z, x='ER.Abs.Change.AVG', y='Avg.Delta.Reserves', z='ER.Volatility.Changes', color='Cluster', hover_data=['Country.Year'])
    # Customize the layout
    fig.update_layout(
        scene=dict(
            xaxis_title='Mean XR change',
            yaxis_title='Mean Reserves change',
            zaxis_title='Volatility XR Change'
        ),
    )
    # Show the interactive plo

    st.pyplot(fig)



    if False:
        df1 = df1[['Country', 'Year', 'FXI_spot','FXI_broad','Avg.Delta.Reserves']]

        country = st.selectbox(
        'Select a country',
        df1['Country'].unique(),
        index = 6)

        fig1, ax1 = plt.subplots(figsize=(12, 4))

        df1[(df1['Country'] == country)].plot(
            x = "Year", \
                y = ['FXI_spot', 'FXI_broad'], \
                    style=['-'], \
                        color=['r','b'], \
                            ax=ax1)

        df1[(df1['Country'] == country)].plot('Year','Avg.Delta.Reserves',secondary_y=True, ax=ax1)

        st.pyplot(fig1)


        fig, ax = plt.subplots(figsize=(8, 8))

        ax = plt.scatter(df1['Avg.Delta.Reserves'], df1['FXI_spot'])

        st.pyplot(fig)
















    df = pd.read_csv("LYS2022.csv")

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
     (df['Year'] >= values[0])][['Year','3-way','4-way','Reference Currency']] #'Final Classification' no incluído

    df_temp = df_temp.loc[df_temp['3-way'] != 'NON']

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
        with open("LYS2022.csv", "rb") as file:
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
    st.sidebar.write('4-way Classification: Fix, Crawling Peg, Dirty Float, Float, OVM (Unclassified One Variable Missing), NON (non-existing or non-independent country), Not Classified: Undisclosed Basket or too little volatility in variables (Low Volatility).')
    st.sidebar.write('3-way Classification: Fix, Interm, Float, OVM, NON, Undisclosed Basket, Low Volatility.')
    st.sidebar.write('*Industrial Countries')
    st.sidebar.write('**Emerging Economies')
    st.sidebar.write('#### Reference:')
    st.sidebar.write('[Classifying Exchange Rate Regimes: 20 Years Later](https://ideas.repec.org/p/sad/wpaper/166.html)')

    # Si no está la Final Classification, no tiene sentido que esté toda la tabla!
    # st.sidebar.table(legend.iloc[1: , :])
