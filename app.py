import pandas as pd
from Connection import data_connect

import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.express as px


df_main = data_connect()
country_options = [{'label': i, 'value': i} for i in sorted(df_main.country.unique())]

app = dash.Dash(__name__)
app.title = "CORONA"

app.layout = html.Div(
    children = [
        html.H1(children="CORONA IN THE WORLD"),

        html.Div([
                dcc.Dropdown(
                    id = "country-dropdown",
                    options = country_options,
                    value = "World"
                )
            ]
        ),

        html.Div(
            dcc.Graph(
                id="corona-infected"
            )
        )
    ]
)

@app.callback(
    dash.dependencies.Output('corona-infected', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def select_country_infecte(value):
    df_plot = df_main[df_main["country"] == value]
    df_plot.set_index("date", inplace = True)
    df_plot = df_plot[["value_confirmed", "value_deaths"]].dropna().rolling(7).mean().dropna().round(0)
    df_plot.columns = ["Infection", "Death"]

    fig = px.line(
        df_plot
        , x=df_plot.index , y=["Infection", "Death"]
        ,labels= {"date":"Date", "value":"Count"}
        )
    
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)