from datetime import datetime
import streamlit as st
import pandas as pd


class GitHubDataFormatter:

    _FIELDS_USER = ['login', 'name', 'email', 'id', 'bio', 'location', 'company', 'followers', 'following',
                    'created_at', 'public_repos']
    _MONTH_NUMBER_NAME_DICT = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
                               '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

    def __init__(_self):
        pass
        # print('New GitHubDataFormatter created.')

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
            languages_dict = {f'Languages in {type} repositories': '0',
                              f'{type.capitalize()} repositories': '0'}
            df_languages_count = pd.DataFrame(list(languages_dict.items()), columns=['Field', 'Value'])
            return df_languages_count

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

    def get_imagem_profile(_self, user_info_dict):
        return user_info_dict.get('avatar_url')

    def filter_remove_fields_prefix_df(_self, df_report, field_prefix):
        fields = df_report['Field'].unique().tolist()
        filtered_fields = [field for field in fields if field.startswith(field_prefix)]
        df_filtered_fields = df_report[df_report['Field'].isin(filtered_fields)].copy()
        df_filtered_fields['Field'] = df_filtered_fields.loc[:, 'Field'].str.replace(field_prefix, '')
        df_filtered_fields = df_filtered_fields.reset_index(drop=True)
        df_filtered_fields.index = df_filtered_fields.index + 1
        df_filtered_fields.columns = ['Language', 'Quantity']
        df_filtered_fields['Quantity'] = df_filtered_fields['Quantity'].astype(int)

        return df_filtered_fields

    def create_df_from_date(_self, user_repos_list, first_year, last_year):
        count_by_date = {}
        for year in range(first_year, last_year+1):
            for month in range(1, 10):
                key_date = '0' + str(month) + '/' + str(year)
                count_by_date[key_date] = 0

            for month in range(10, 13):
                key_date = str(month) + '/' + str(year)
                count_by_date[key_date] = 0

        for repo in user_repos_list:
            date_creation = repo.get('created_at')
            data_obj = datetime.strptime(date_creation, '%Y-%m-%dT%H:%M:%SZ')
            data_formated = data_obj.strftime('%m/%Y')
            count_by_date[data_formated] = count_by_date[data_formated] + 1

        df_count_by_date = pd.DataFrame(count_by_date.items(), columns=['Date', 'Quantity'])

        return df_count_by_date

    def format_month_column(_self, df_date):
        df_date['Month'] = df_date['Month'].map(GitHubDataFormatter._MONTH_NUMBER_NAME_DICT)
        return df_date


@st.cache_data
def create_github_data_formatter():
    return GitHubDataFormatter()
