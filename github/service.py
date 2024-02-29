from github.scraper import GitHubDataScraper
from github.formatter import GitHubDataFormatter

import streamlit as st


class GitHubDataService:

    def __init__(_self):
        _self.scraper = GitHubDataScraper()
        _self.formatter = GitHubDataFormatter()
        print('New GitHubDataService created.')

    def create_table_user_info(_self, username):
        user_info_dict = _self.scraper.get_github_user_info(username)
        total_repos = int(user_info_dict.get('public_repos', 0))
        user_repos_list = _self.scraper.get_github_user_repos(username, total_repos)
        df_user = _self.formatter.create_table_report_user(user_info_dict, user_repos_list)

        return df_user

    @st.cache_data
    def create_file(_self, df):
        return df.to_csv(sep=';', index=False).encode('utf-8')


@st.cache_data
def create_github_data_service():
    return GitHubDataService()
