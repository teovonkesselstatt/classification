import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import plotly.express as px
from scikit_learn.cluster import KMeans
from scipy.stats import zscore

def run_app():


    cluster_size = st.slider('##### Cluster number:', min_value=2, max_value=10, value=5, step=1)


    # Read the CSV file, separate NAs and Outliers, z-score
    df = pd.read_csv("base_entera.csv", encoding='latin-1')

    # Rename columns
    df.columns = ["Country.Name", "Year", "ER.Abs.Change.AVG", "ER.Volatility.Changes", "Avg.Delta.Reserves"]

    # Filter data for the desired years
    df = df[(df['Year'] > 1973) & (df['Year'] < 2023)]

    # Generate a new column "Country.Year"
    df['Country.Year'] = df['Country.Name'] + "_" + df['Year'].astype(str)

    # Select relevant columns
    df = df[["Country.Year", "ER.Abs.Change.AVG", "ER.Volatility.Changes", "Avg.Delta.Reserves"]]

    # Separate data into two dataframes: one without NAs and one with NAs
    df_sin_na = df.dropna()

    # Convert numeric columns to numeric type
    numeric_cols = ["ER.Abs.Change.AVG", "ER.Volatility.Changes", "Avg.Delta.Reserves"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Calculate quantiles
    qer = df_sin_na["ER.Abs.Change.AVG"].quantile(0.98)
    qde = df_sin_na["ER.Volatility.Changes"].quantile(0.98)
    qmr = df_sin_na["Avg.Delta.Reserves"].quantile(0.98)

    # Define the outlier condition
    outlier_condition = ~((df_sin_na["ER.Abs.Change.AVG"] < qer) & (df_sin_na["ER.Volatility.Changes"] < qde) & (df_sin_na["Avg.Delta.Reserves"] < qmr))

    # Separate data into two dataframes: one without outliers and one with outliers
    df_sin_out = df_sin_na[~outlier_condition]

    df_z = df_sin_out.copy()

    # Z-score normalize the numeric columns
    df_z[numeric_cols] = df_sin_out[numeric_cols].apply(zscore)

    ######################## Perform K-means clustering ###########################
    kmeans = KMeans(n_clusters=cluster_size, n_init=1, random_state=123).fit(df_z[numeric_cols])

    # Get cluster sizes and centroids
    cluster_sizes = pd.Series(kmeans.labels_).value_counts().sort_index()
    cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=numeric_cols)

    # Add cluster labels to the dataframe
    df_z['Cluster'] = kmeans.labels_
    df_sin_out['Cluster'] = kmeans.labels_

    # Creo el centroide des-z-score
    desc_stats = df_sin_out[numeric_cols].describe()
    cluster_centers_desz = cluster_centers * desc_stats.loc['std'] + desc_stats.loc['mean']

    # Add cluster sizes to cluster_centers_desz
    cluster_centers_desz['Size of Cluster'] = cluster_sizes.values

    inconclusive = (cluster_centers_desz['ER.Abs.Change.AVG'] +
                    cluster_centers_desz['ER.Volatility.Changes'] +
                    cluster_centers_desz['ER.Abs.Change.AVG']).idxmin()


    df_inconclusives = df_sin_out[df_sin_out['Cluster'] == inconclusive].drop('Cluster', axis=1)

    df_z2 = df_inconclusives.copy()

    # Z-score normalize the numeric columns
    df_z2[numeric_cols] = df_sin_out[numeric_cols].apply(zscore)

    ######################## Perform K-means clustering ###########################
    kmeans2 = KMeans(n_clusters=cluster_size, n_init=1, random_state=123).fit(df_z2[numeric_cols])

    # Get cluster sizes and centroids
    cluster_sizes2 = pd.Series(kmeans2.labels_).value_counts().sort_index()
    cluster_centers2 = pd.DataFrame(kmeans2.cluster_centers_, columns=numeric_cols)

    # Add cluster labels to the dataframe
    df_z2['Cluster'] = kmeans2.labels_
    df_inconclusives['Cluster'] = kmeans2.labels_

    # Creo el centroide des-z-score
    desc_stats2 = df_inconclusives[numeric_cols].describe()
    cluster_centers_desz2 = cluster_centers2 * desc_stats2.loc['std'] + desc_stats2.loc['mean']

    # Add cluster sizes to cluster_centers_desz
    cluster_centers_desz2['Size of Cluster'] = cluster_sizes2.values

    df_z[['Country', 'Year']] = df['Country.Year'].str.split('_', expand=True)
    # df_z.to_csv('Classification/output/cluster1.csv', index=False, encoding='latin-1')

    # Create an interactive 3D scatter plot using Plotly
    fig = px.scatter_3d(df_z, x='ER.Abs.Change.AVG', y='Avg.Delta.Reserves', z='ER.Volatility.Changes', color='Cluster', hover_data=['Country.Year'])
    # Customize the layout
    fig.update_layout(
        scene=dict(
            xaxis_title='Mean XR change',
            yaxis_title='Mean Reserves change',
            zaxis_title='Volatility XR Change'
        ),
    )

    st.plotly_chart(fig1, sharing="streamlit", theme="streamlit")

    df_z2[['Country', 'Year']] = df['Country.Year'].str.split('_', expand=True)
    # Create an interactive 3D scatter plot using Plotly
    # df_z2.to_csv('Classification/output/cluster2.csv', index=False, encoding='latin-1')
    fig1 = px.scatter_3d(df_z2, x='ER.Abs.Change.AVG', y='Avg.Delta.Reserves', z='ER.Volatility.Changes', color='Cluster', hover_data=['Country.Year'])
    # Customize the layout
    fig1.update_layout(
        scene=dict(
            xaxis_title='Mean XR change',
            yaxis_title='Mean Reserves change',
            zaxis_title='Volatility XR Change'
        ),
    )


    st.plotly_chart(fig1, sharing="streamlit", theme="streamlit")



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















    if False:
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
