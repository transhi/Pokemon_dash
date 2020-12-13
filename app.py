#!/usr/bin/env python
# coding=utf-8

import dash
import dash_html_components as html
import dash_core_components as dcc
from pandas.io.formats import style
import plotly.graph_objects as go
import dash_table
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
df = pd.read_csv('./data/Pokedex_Ver6.csv')
type1_list = df['TYPE1'].unique().tolist()
tmps = df['TYPE2'].unique()
type2_list = [tmp for tmp in tmps if str(tmp) != 'nan']  # remove nan
all_types_tmp = type1_list+type2_list
all_types = []
# remove duplicate elements
[all_types.append(i) for i in all_types_tmp if not i in all_types]

feature_list = ['HP', 'ATK', 'DEF', 'SP_ATK', 'SP_DEF', 'SPD']

# Initialize the app

external_stylesheets = ['./assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True


def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


def get_type_options(list_stocks):

    dict_list = []

    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

def get_feature_options(list_stocks):

    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

app.layout = html.Div(
    children=[html.Div(className='four columns div-user-controls',
                       children=[
                                 html.H3('DASH - POKERDEX'),
                                 html.P(
                                     'Visualising pokeman observations with Plotly - Dash.'),

                                 html.Div(className='div-for-dropdown',
                                          children=[
                                              html.P(
                                                  'Pick one types from the dropdown below(default:All types), and it will return a table with observations of the type',style={'color':'white'}),
                                              dcc.Dropdown(id='selector1', options=get_type_options(all_types),
                                                           multi=False,
                                                           style={
                                                  'backgroundColor': '#1E1E1E'},
                                                  className='selector1'
                                              ),
                                               html.P(
                                                  'Pick one features from the dropdown below (default:HP), and it will return a figure with distribution of feature from the type choosed above',style={'color':'white'},),
                                              dcc.Dropdown(id='selector2', options=get_feature_options(feature_list),
                                                           multi=False,
                                                           style={
                                                  'backgroundColor': '#1E1E1E'},
                                                  className='selector2'
                                              ),
                                              html.P(
                                                  'top values of the type'),
                                              dcc.Graph(id='features',)

                                          ],

                                          style={'color': '#1E1E1E', 'height': '80vh'})
                       ]
                       ),
              # html.Div(className='four columns div-for-charts bg-grey',
              #         children=[
              #                      dcc.Graph(id='timeseries', config={'displayModeBar': False}, animate=True)
              #                  ],
              #         style={'color': '#1E1E1E','height': '40vh'}),
              html.Div(className='eight columns div-for-charts bg-grey',
                       children=[dash_table.DataTable(
                                 id='punchstats',
                                 columns=[{'name': i, 'id': i}
                                          for i in df.columns],
                                 # data = df.to_dict('records'),
                                 data=[],
                                 page_current=0,
                                 page_size=30,
                                 page_action='native',
                                 sort_action='native',
                                 column_selectable="single",
                                 row_selectable="single",
                                 sort_mode='multi',
                                 style_table={'overflowX': 'scroll',
                                              'maxHeight': '1600px'},
                                 style_header={
                                    'backgroundColor': 'rgb(30, 30, 30)'},
                                 style_cell={'backgroundColor': 'rgb(50,50,50)',
                                             'color': 'white'},
                                 sort_by=[]),
                                 ]),
              ])


# Callback for timeseries price
@app.callback([Output(component_id='punchstats', component_property='data'),
               Output(component_id='features', component_property='figure')],
              [Input(component_id='selector1', component_property='value'), Input(component_id='selector2', component_property='value')])
def update(selected_value1,selected_value2):
    if not selected_value1 :
        df_sub = df
        df_sub_dict = df.to_dict('records')
    else:
        df_sub1 = df.loc[df['TYPE1'] == selected_value1]
        df_sub2 = df.loc[df['TYPE2'] == selected_value1]
        df_sub = df_sub1.append(df_sub2)
        df_sub_dict = df_sub1.append(df_sub2).to_dict('records')
    if selected_value2:
        figure = px.histogram(df_sub, x=selected_value2, title='Maximum Values of Feature '+selected_value2)
    else:
        figure = px.histogram(df_sub, x='HP', title='Number Distributions of Feature HP')
    
    # figure={
    #         'data': [
    #             {'x': ['HP','ATK','DEF','SP_ATK','SP_DEF','SPD'], 'y': max_values, 'type': 'bar', 'name': 'Max'},
    #             {'x': ['HP','ATK','DEF','SP_ATK','SP_DEF','SPD'], 'y': min_values,'type': 'bar', 'name': 'Min'},
    #         ],
    #         'layout': {
    #             'title': 'Maximum Values of Features'
    #         }
    #     }
    return df_sub_dict, figure


if __name__ == '__main__':
    app.run_server(debug=True)
