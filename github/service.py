from github.scraper import create_github_data_scraper
from github.formatter import create_github_data_formatter
from github.ploter import create_github_data_ploter

import streamlit as st
import pandas as pd
from datetime import datetime


class GitHubDataService:
    _FIELDS_METRICS_LIST = ['Public Repositories', 'Created repositories', 'Forked repositories',
                            'Followers', 'Following']
    _NUMBER_OF_BARS_RECOMMENDED = 5

    def __init__(_self):
        _self.scraper = create_github_data_scraper()
        _self.formatter = create_github_data_formatter()
        _self.ploter = create_github_data_ploter()
        # print('New GitHubDataService created.')

    @st.cache_data
    def create_table_user_info(_self, username):
        user_info_dict = _self.scraper.get_github_user_info(username)

        if not user_info_dict:
            return pd.DataFrame()

        total_repos = int(user_info_dict.get('public_repos', 0))
        user_repos_list = _self.scraper.get_github_user_repos(username, total_repos)

        df_user = _self.formatter.create_table_report_user(user_info_dict, user_repos_list)

        return df_user

    @st.cache_data
    def create_file(_self, df):
        return df.to_csv(sep=';', index=False).encode('utf-8')

    @st.cache_data
    def create_metrics_info(_self, df_user):
        if df_user.empty:
            return []

        fields_list = df_user['Field'].unique().tolist()
        metrics_info_list = []
        for field in GitHubDataService._FIELDS_METRICS_LIST:
            if field in fields_list:
                metrics_info_list.append((field, df_user[df_user['Field'] == field]['Value'].iloc[0]))

        return metrics_info_list

    @st.cache_data
    def create_metrics_cols_size(_self, metrics_line):
        return [1] * len(metrics_line)

    @st.cache_data
    def get_image_profile(_self, username):
        return _self.scraper.get_github_image_profile(username)

    @st.cache_data
    def plot_bar_prefixed_fields(_self, df_report, field_prefix, is_reversed):
        df_filtered_fields = _self.formatter.filter_remove_fields_prefix_df(df_report, field_prefix=field_prefix)

        if df_filtered_fields.empty:
            return f'No languages detected in {field_prefix[:-4]}.'

        num_bars = min(GitHubDataService._NUMBER_OF_BARS_RECOMMENDED, df_filtered_fields.shape[0])
        df_filtered_fields = df_filtered_fields.head(num_bars)

        fig = _self.ploter.plot_hotizontal_bar(df_filtered_fields, 'Language',
                                               f'Top {num_bars} language(s) in {field_prefix[:-4]}',
                                               is_reversed)

        return fig

    @st.cache_data
    def plot_line_repositories_creation(_self, df_report):
        firt_date = df_report[df_report['Field'] == 'Profile creation date']['Value'].iloc[0]
        first_year = int(firt_date.split('/')[-1])
        last_year = datetime.now().year

        total_repos = int(df_report[df_report['Field'] == 'Public Repositories']['Value'].iloc[0])
        username = df_report[df_report['Field'] == 'Username']['Value'].iloc[0]
        user_repos_list = _self.scraper.get_github_user_repos(username, total_repos)

        df_count = _self.formatter.create_df_from_date(user_repos_list, first_year, last_year)
        df_count['Month'] = df_count['Date'].str.split('/').str[0]
        df_count['Month'] = df_count['Month'].astype(str)
        df_count['Year'] = df_count['Date'].str.split('/').str[1]
        df_count['Year'] = df_count['Year'].astype(str)
        df_count = df_count.sort_values(by=['Year', 'Month'])
        df_count = _self.formatter.format_month_column(df_count)

        fig = _self.ploter.plot_line(df_count, x_axis='Month', y_axis='Quantity', categories='Year',
                                     title='Created/Forked Repositories by Date')
        return fig


@st.cache_data
def create_github_data_service():
    return GitHubDataService()
