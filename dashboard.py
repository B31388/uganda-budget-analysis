import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv('/workspaces/uganda-budget-analysis/uganda_budget_cleaned.csv')
pred_df = pd.read_csv('/workspaces/uganda-budget-analysis/sector_predictions_2022.csv')

# Initialize app
app = dash.Dash(__name__)

# Layout definition
app.layout = html.Div([
    html.H1(
        "Uganda Budget Analysis Dashboard (FY 2015/16 - 2021/22)",
        style={'textAlign': 'center'}
    ),
    html.Div([
        html.Label("Select Sector:"),
        dcc.Dropdown(
            id='sector-dropdown',
            options=[{'label': s, 'value': s} for s in df['Sector'].unique()],
            value=df['Sector'].unique()[0],
            multi=False,
            style={'width': '50%'}
        ),
    ], style={'padding': '20px'}),
    dcc.Graph(id='trend-graph'),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='prediction-bar'),
])

# Callback for interactivity
@app.callback(
    [
        dash.dependencies.Output('trend-graph', 'figure'),
        dash.dependencies.Output('pie-chart', 'figure'),
        dash.dependencies.Output('prediction-bar', 'figure'),
    ],
    [dash.dependencies.Input('sector-dropdown', 'value')]
)
def update_graphs(selected_sector):
    filtered_df = df[df['Sector'] == selected_sector]
    trend_fig = px.line(
        filtered_df, x='FinancialYear', y='Approved Budget',
        title=f'Allocation Trend for {selected_sector} (UGX)',
        labels={'Approved Budget': 'Allocation (UGX)', 'FinancialYear': 'Fiscal Year'},
        markers=True
    )
    
    df_2122 = df[df['FinancialYear'] == '2021-06-01']
    pie_fig = px.pie(
        df_2122, values='Approved Budget', names='Sector',
        title='FY 2021/22 Budget Share',
        labels={'Approved Budget': 'Allocation (UGX)'}
    )
    pie_fig.update_traces(textinfo='percent+label', pull=[0.1] + [0]*(len(pie_fig.data)-1))
    
    pred_fig = px.bar(
        pred_df, x='Sector', y='Predicted_2022_UGX',
        title='Predicted Budget Allocations for FY 2022/23 (UGX)',
        labels={'Predicted_2022_UGX': 'Predicted Allocation (UGX)'}
    )
    
    return trend_fig, pie_fig, pred_fig

# Launch the app using the updated method
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
