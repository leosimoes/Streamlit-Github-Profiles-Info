import streamlit as st
import pandas as pd
from github.service import create_github_data_service


########################################################################################################################
# Settings and configurations
########################################################################################################################
st.set_page_config(page_title='Report - GitHub Profile', page_icon=':bookmark_tabs:', layout='centered',
                   initial_sidebar_state='expanded')

github_data_service = create_github_data_service()
df_user = pd.DataFrame()


########################################################################################################################
# Sidebar and Form
########################################################################################################################
with st.sidebar:
    st.header('GitHub Profile Informations')
    st.subheader('Author: Leonardo Simões')

    with st.form('form_github_username'):
        username_input = st.text_input('Username:', value='')
        if st.form_submit_button('Search', use_container_width=True):
            df_user = github_data_service.create_table_user_info(username_input)


########################################################################################################################
# Dashboard Screen
########################################################################################################################
with st.container():
    st.title('Report - GitHub Profile')

    if df_user.empty:
        st.warning('Enter a valid Github profile name or wait to make another request.')
    else:
        st.table(df_user)

        csv = github_data_service.create_file(df_user)

        st.download_button(
            label="Download Report as CSV File",
            data=csv,
            file_name='report.csv',
            mime='text/csv',
            use_container_width=True
        )
