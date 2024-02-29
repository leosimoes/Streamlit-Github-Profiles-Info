from datetime import datetime
import streamlit as st
import pandas as pd


class GitHubDataFormatter:

    _FIELDS_USER = ['login', 'name', 'email', 'id', 'bio', 'location', 'company', 'followers', 'following',
                    'created_at', 'public_repos']

    def __init__(_self):
        print('New GitHubDataFormatter created.')

    def _create_df_user_info(_self, user_info_dict):

        if len(user_info_dict) == 0:
            return pd.DataFrame()

        df_user = pd.DataFrame({field: str(user_info_dict[field]) for field in GitHubDataFormatter._FIELDS_USER},
                               index=[1])

        df_user = df_user.T
        df_user = df_user.reset_index()
        df_user.columns = ['Field', 'Value']

        df_user = df_user.dropna()
        df_user = df_user[df_user['Value'] != 'None']

        df_user['Field'] = df_user['Field'].str.replace('_', ' ').str.capitalize()
        df_user['Field'] = df_user['Field'].replace({'Login': 'Username',
                                                     'Created at': 'Profile creation date',
                                                     'Public repos': 'Public Repositories'})

        data_string = df_user[df_user['Field'] == 'Profile creation date']['Value'].iloc[0]
        data_obj = datetime.strptime(data_string, '%Y-%m-%dT%H:%M:%SZ')
        df_user.loc[df_user['Field'] == 'Profile creation date', 'Value'] = data_obj.strftime('%m/%d/%Y')

        return df_user

    def _filter_repos_list(_self, user_repos_list, filter_function):
        return list(filter(filter_function, user_repos_list))

    def _create_df_languages_count(_self, user_repos_list, type='created'):

        if len(user_repos_list) == 0:
            return pd.DataFrame()

        languages_set = set(map(lambda repo: repo.get('language'), user_repos_list))
        languages_list = list(filter(lambda language: language is not None, languages_set))

        languages_dict_0 = {f'Languages in {type} repositories': str(len(languages_list)),
                            f'{type.capitalize()} repositories': str(len(user_repos_list))}
        df_languages_count_0 = pd.DataFrame(languages_dict_0.items(), columns=['Field', 'Value'])
        df_languages_count_0['Value'] = df_languages_count_0['Value'].astype(str)

        languages_dict = {}
        for language in languages_list:
            field = f'{type.capitalize()} repositories in {language}'
            languages_dict[field] = len(list(filter(lambda repo: repo['language'] == language, user_repos_list)))

        df_languages_count_1 = pd.DataFrame(list(languages_dict.items()), columns=['Field', 'Value'])
        df_languages_count_1 = df_languages_count_1.sort_values(by='Value', ascending=False)
        df_languages_count_1['Value'] = df_languages_count_1['Value'].astype(str)

        df_languages_count_2 = pd.DataFrame()

        if None in languages_set:
            without_languages_list = list(filter(lambda repo: repo.get('language') is None, user_repos_list))
            languages_dict_2 = {f'{type.capitalize()} repositories without language': str(len(without_languages_list))}
            df_languages_count_2 = pd.DataFrame(list(languages_dict_2.items()), columns=['Field', 'Value'])

        df_languages_count = pd.concat([df_languages_count_0, df_languages_count_1, df_languages_count_2],
                                       ignore_index=True)

        return df_languages_count

    def create_table_report_user(_self, user_info_dict, user_repos_list):
        df_user = _self._create_df_user_info(user_info_dict)
        user_repos_created_list = _self._filter_repos_list(user_repos_list, lambda x: not x['fork'])
        user_repos_forked_list = _self._filter_repos_list(user_repos_list, lambda x: x['fork'])
        df_repos_cretated = _self._create_df_languages_count(user_repos_created_list, type='created')
        df_repos_forked = _self._create_df_languages_count(user_repos_forked_list, type='forked')
        df_report = pd.concat([df_user, df_repos_cretated, df_repos_forked], ignore_index=True)
        df_report.index = df_report.index + 1

        return df_report


@st.cache_data
def create_github_data_formatter():
    return GitHubDataFormatter()
