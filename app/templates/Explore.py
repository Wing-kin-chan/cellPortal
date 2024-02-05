from dash import Dash, html, dcc, Input, Output

def explore_content():
    return html.Div([
        dcc.Input(id = 'search-bar', type = 'text', placeholder = 'Search...'),
        html.Button('Search', id = 'search-button'),
        html.Div(id = 'search-results')
    ])
