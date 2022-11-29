# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
#print(spacex_df.dtypes)
#print(spacex_df.value_counts())

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                html.Div([
                    html.Div(
                         [html.H2('Lanuch Site:', style={'margin-right': '2em'})]
                    ),
                    dcc.Dropdown(id='site-dropdown', 
                    # Update dropdown values using list comphrehension
                        options=[{'label': 'All Sites','value':'ALL Sites'},
                                {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}
                        ],
                        value='ALL Sites',
                        placeholder="place holder here",
                        searchable=True
                    )
                ]),
                
                html.Br(),

                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                html.Div(dcc.Graph(id='success-pie-chart')),

                html.Br(),

                # html.P("Payload range (Kg):"),

                # TASK 3: Add a slider to select payload range
                #dcc.RangeSlider(id='payload-slider',...)

                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                # html.Div(dcc.Graph(id='success-payload-scatter-chart')),
            ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, 
# `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

# Add computation to callback function and return graph
def get_graph(site):
    print('get_graph site: ',site) 
    # Select data
    
    if site == 'ALL Sites':
        #pie_df = df.groupby(['Launch Site'])['class'].sum().reset_index()
        #print(spacex_df.dtypes)
        pie_fig = px.pie(spacex_df, values='class', names='Launch Site', 
                title='ALL Sites % on Total Success Outcome')
    else:
        df = spacex_df[spacex_df['Launch Site']==site][['Launch Site','class']].reset_index()
        df['classx'] = df['class'].astype('string')
        df['class'] = 1
        #print("site:\n",df)
        #print(df.dtypes)
        print(df.shape)
        #pie_df = df.groupby(['Launch Site','Booster Version'])['class'].sum().reset_index()
        pie_fig = px.pie(df, values='class', names='classx', 
                title='Site:'+site)
    return pie_fig        
    #return [dcc.Graph(figure=pie_fig)]
        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
