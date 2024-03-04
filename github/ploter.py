import streamlit as st
import plotly.express as px


class GitHubDataPloter:
    _FIGURE_TITLE_LAYOUT = {'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
    _FIGURE_LEGEND = {'y': 1, 'x': 1, 'xanchor': 'right', 'yanchor': 'top'}
    _FIGURE_HEIGHT = 250
    _FIGURE_HEIGHT_2 = 350
    _COLOR_BARS = 'blue'
    _COLOR_LIST_DISCRETE = px.colors.qualitative.Plotly_r

    def __init__(_self):
        pass
        # print('New GitHubDataPloter created.')

    @st.cache_data
    def plot_hotizontal_bar(_self, df_count, col, title='Top Languages', is_reversed=False):
        fig = px.bar(df_count,
                     x='Quantity',
                     y=col,
                     color=col,
                     color_discrete_sequence=[GitHubDataPloter._COLOR_BARS],
                     title=title,
                     height=GitHubDataPloter._FIGURE_HEIGHT,
                     orientation='h'
                     )

        fig.update_layout(showlegend=False)
        fig.update_layout(title=GitHubDataPloter._FIGURE_TITLE_LAYOUT)
        fig.update_traces(textposition='inside')
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None)

        if is_reversed:
            fig.update_layout(xaxis=dict(autorange='reversed'), yaxis=dict(side='right'))

        return fig

    @st.cache_data
    def plot_line(_self, df, x_axis, y_axis, categories, title):
        fig = px.line(df,
                      x=x_axis,
                      y=y_axis,
                      color=categories,
                      color_discrete_sequence=GitHubDataPloter._COLOR_LIST_DISCRETE,
                      title=title,
                      height=GitHubDataPloter._FIGURE_HEIGHT_2,
                      markers=True)

        fig.update_layout(title=GitHubDataPloter._FIGURE_TITLE_LAYOUT, legend=GitHubDataPloter._FIGURE_LEGEND)

        return fig


@st.cache_data
def create_github_data_ploter():
    return GitHubDataPloter()
