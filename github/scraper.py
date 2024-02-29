import streamlit as st
import requests


class GitHubDataScraper:

    def __init__(_self):
        print('New GitHubDataScraper created.')

    def get_github_user_info(_self, username):
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)

        if response.status_code == 200:
            user_info = response.json()
            return user_info
        else:
            return {}

    def get_github_user_repos(_self, username, total_repos):
        user_repos_list = []
        per_page = 100
        total_pages = total_repos//per_page + 1

        for page_number in range(1, total_pages+1):
            if total_repos < per_page:
                per_page = total_repos

            url = f"https://api.github.com/users/{username}/repos?page={page_number}&per_page={per_page}"
            response = requests.get(url)

            if response.status_code == 200:
                user_repos_list.extend(response.json())
            else:
                return []

        return user_repos_list


@st.cache_data
def create_github_data_scraper():
    return GitHubDataScraper()
