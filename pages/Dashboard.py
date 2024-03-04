import streamlit as st
import pandas as pd
from github.service import create_github_data_service

########################################################################################################################
# Settings and configurations
########################################################################################################################
st.set_page_config(page_title='Dashboard - GitHub Profile', page_icon=':chart_with_upwards_trend:', layout='wide',
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
    st.title('Dashboard - GitHub Profile')

    if df_user.empty:
        st.warning('Enter a valid Github profile name or wait to make another request.')
    else:
        subtitle = f'Username: {username_input}'
        st.write(subtitle)
        st.divider()

        metrics_line = github_data_service.create_metrics_info(df_user)
        metrics_cols = st.columns(github_data_service.create_metrics_cols_size(metrics_line))

        for i in range(len(metrics_line)):
            with metrics_cols[i]:
                st.metric(label=metrics_line[i][0], value=metrics_line[i][1])

        st.divider()

        st_col_1, st_col_2 = st.columns(2)

        with st_col_1:
            fig_col_1 = github_data_service.plot_bar_prefixed_fields(df_user,
                                                                     field_prefix='Created repositories in ',
                                                                     is_reversed=False)
            if isinstance(fig_col_1, str):
                st.markdown(f"<h5 style='text-align: center;'>{fig_col_1}</h5>", unsafe_allow_html=True)
            else:
                st.plotly_chart(fig_col_1, use_container_width=True)

        with st_col_2:
            fig_col_2 = github_data_service.plot_bar_prefixed_fields(df_user,
                                                                     field_prefix='Forked repositories in ',
                                                                     is_reversed=True)
            if isinstance(fig_col_2, str):
                st.markdown(f"<h5 style='text-align: center;'>{fig_col_2}</h5>", unsafe_allow_html=True)

            else:
                st.plotly_chart(fig_col_2, use_container_width=True)

        st.divider()

        fig_col_3 = github_data_service.plot_line_repositories_creation(df_user)
        st.plotly_chart(fig_col_3, use_container_width=True)

        st.divider()
