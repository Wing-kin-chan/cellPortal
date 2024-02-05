from dash import Dash, html, dcc, Input, Output

app = Dash(__name__, title = 'cellPortal')
app.layout = html.Div([
    html.Div(
        className = 'application-header',
        children = [html.H1('cellPortal', className = 'application-header--title'),
                    html.H4('Explore, visualize, and publish your single-cell and spatial transcriptomics data.', 
                            className = 'application-header--subtitle')]
    ),
    html.Br(),
    html.Div([
        dcc.Tabs(
            id = 'application-tabs',
            #value = 'explore',
            parent_className = 'hometabs',
            className = 'hometabs-container',
            children = [
                dcc.Tab(
                    label = 'Explore',
                    value = 'explore',
                    className = 'tab',
                    selected_className = 'tab-selected'
                ),
                dcc.Tab(
                    label = 'Publish',
                    value = 'publish',
                    className = 'tab',
                    selected_className = 'tab-selected'
                ),
                dcc.Tab(
                    label = 'About',
                    value = 'about',
                    className = 'tab',
                    selected_className = 'tab-selected'
                ),
            ]),
        ]),
    html.Div(id = 'tab-contents')
])

@app.callback(
        Output(component_id = 'tab-contents', component_property = 'children'), 
        [Input(component_id = 'application-tabs', component_property = 'value')]
        )
def render_content(tab):
    if tab == 'explore':
        return html.Div([
            html.H3('Explore content')
        ])
    elif tab == 'publish':
        return html.Div([
            html.H3('Publish content')
        ])
    elif tab == 'about':
        return html.Div([
            html.H3('About content')
        ])

if __name__ == '__main__':
    app.run()