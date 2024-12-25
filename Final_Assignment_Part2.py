import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

app = dash.Dash(__name__)

app.title = "Automobile Statistics Dashboard"

dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in range(1980, 2024, 1)]

app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard",style={'textAlign':'center','color':'#503D36','font-size':24}),#May include style for title
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
           id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type',style={'textAlign':'center','width':'80%','padding':'3px','font-size':20}
        )
    ]), 

    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select Year',
                  style={'textAlign':'center','width':'80%','padding':'3px','font-size':20})
            
        ),

    html.Div([
    html.Div(id='output-container', className='chart-grid', style={'display':'flex'}),])
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True


@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
     Input(component_id='select-year', component_property='value')])


def update_output_container(selected_statistics,input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))

        average_sales = recession_data.groupby(['Year','Vehicle_Type'])['Automobile_Sales'].mean().reset_index()                           
        R_chart2  = dcc.Graph(
            figure=px.bar(average_sales,
            x='Year',
            y='Automobile_Sales',
            color='Vehicle_Type',
            title='Average Automobile Sales by Vehicle Type over Recession Period'
        )
        )
        exp_rec=recession_data.groupby('Advertising_Expenditure').sum().reset_index()
        R_chart3 = dcc.Graph(
        figure=px.pie(exp_rec,
        values = 'Recession',
        names = 'Vehicle_Type',
        title='Total Advertising Expenditure Share by Vehicle Type during Recessions'
        )
        )

        unemp_rate = recession_data.groupby(['Vehicle_Type','Automobile_Sales'])['unemployment_rate'].sum().reset_index()
        R_chart4  = dcc.Graph(
            figure=px.bar(unemp_rate,
            x='Vehicle_Type',
            y='Automobile_Sales',
            color='unemployment_rate',
            title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)])
            ]
                           
    elif (input_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == 0 ]
                              
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, 
        x='Year',
        y='Automobile_Sales',
        title="Yearly Automobile Sales"
        )
            )
            
        mon_sales = data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mon_sales, 
            x='Month',
            y='Automobile_Sales',
            title="Monthly Automobile Sales"
        ))

        avr_vdata=yearly_data.groupby(['Month','Vehicle_Type'])['Automobile_Sales'].mean().reset_index() 
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
            x='Month',
            y='Automobile_Sales',
            color='Vehicle_Type',title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

        exp_data=yearly_data.groupby('Advertising_Expenditure').sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data,
            values = 'Advertising_Expenditure',
            names = 'Vehicle_Type',
            title='Total Advertisement Expenditure for each Vehicle Type in the year {}'.format(input_year))
        )

        return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)])
                ]
        
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)