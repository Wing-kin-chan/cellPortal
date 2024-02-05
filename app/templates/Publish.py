from dash import Dash, dcc, html, Input, Output, State
import hashlib

def publish_content(logged_in = False):
    if logged_in:
        return html.Div([
            html.H3('New Page')
        ])
    else:
        return html.Div([
            dcc.Input(id = 'username-input', type = 'text', placeholder = 'Username'),
            dcc.Input(id = 'password-input', type = 'password', placeholder = 'Password'),
            html.Button('Login', id = 'login-button'),
            html.Button('Register', id = 'register-button'),
            html.Div(id = 'Login-status')
        ])
    
def login_callback(app):
    @app.callback(
        [Output('login-status', 'children'),
         Output('url', 'pathname')],
        [Input('login-button', 'n-clicks')],
        [State('username-input', 'value'),
         State('password-input', 'value')]
    )
    def login(n_clicks, username, password):
        pass

    @app.callback(
        [Output('login-status', 'children'),
         Output('url', 'pathname')],
        [Input('register-button', 'n_clicks')],
        [State('username-input', 'value'),
         State('password-input', 'value')]
    )
    def register(n_clicks, username, password):
        pass

    @app.callback(
        Output('url', 'pathname'),
        [Input('login-status', 'children')]
    )
    def account_page():
        pass