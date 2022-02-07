# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
sites = spacex_df['Launch Site'].unique().tolist()
siteslist = []
siteslist.append({'label':'All Sites', 'value': 'ALL'})
for site in sites:
    siteslist.append({'label':site, 'value':site})
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                               
                                dcc.Dropdown(id = 'site-dropdown',
                                            options=siteslist, placeholder='Select a launch site', searchable = True, value='All Sites'),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),


                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id = 'payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                marks = {0: '0 Kg',
                                                        1000: '1000 Kg',
                                                        2000: '2000 Kg',
                                                        3000: '3000 Kg',
                                                        4000: '4000 Kg',
                                                        5000: '5000 Kg',
                                                        6000: '6000 Kg',
                                                        7000: '7000 Kg',
                                                        8000: '8000 Kg',
                                                        9000: '9000 Kg',
                                                        10000: '10000 Kg'},
                                                        value = [min_payload,max_payload]
                                                        ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
            [Input(component_id='site-dropdown',component_property='value')])
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        fig = px.pie(filtered_df,values='class',
        names = 'Launch Site',title = 'Successful launches by site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.pie(filtered_df,
        names = 'class',title = 'Successful launches for lauch site' +entered_site)
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),Input(component_id='payload-slider',component_property='value')]
)

def update_scattergraph(entered_site,payload_slider):
    if entered_site == 'ALL':
        low, high = payload_slider
        df = spacex_df
        mask = (df['Payload Mass (kg)']>low) &(df['Payload Mass (kg)'] < high) 
        fig = px.scatter(
            df[mask], x = 'Payload Mass (kg)',y='class',
            color = 'Booster Version',
            size = 'Payload Mass (kg)',
            hover_data=['Payload Mass (kg)']
        )
    else:
        low, high = payload_slider
        df = spacex_df[spacex_df['Launch Site']==entered_site]
        mask = (df['Payload Mass (kg)']>low) &(df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask], x = 'Payload Mass (kg)',y='class',
            color = 'Booster Version',
            size = 'Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'] )     
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
