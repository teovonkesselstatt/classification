from webapp import app
from streamlit import cli as stcli
import streamlit as st
import sys

if __name__ == "__main__":
    if st._is_running_with_streamlit:
        app.run_app()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())