from webapp import country
import streamlit as st

def run_app():
    st.title('Exchange Rate Regimes by country database, Levy Yeyaty Sturzenegger Classification 2022')
    #PAGES = {
    #        "Country": country,
    #        "Full Database": database,
    #        "Correlations": correlations,
    #        "References": references
    #    }

    #st.sidebar.title('Navigation')
    #selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    #page = PAGES[selection]
    page = country
    page.run_app()