import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv('/workspaces/uganda-budget-analysis/uganda_budget_cleaned.csv')
pred_df = pd.read_csv('/workspaces/uganda-budget-analysis/sector_predictions_2022.csv')

# Debug: Check unique FinancialYear values
print("Unique FinancialYear values:", df['FinancialYear'].unique())

# Compute min and max fiscal years dynamically
if not df.empty:
    min_year_str = df['FinancialYear'].min()
    max_year_str = df['FinancialYear'].max()
    min_year = int(min_year_str[:4])
    max_year = int(max_year_str[:4])
    min_fy = f"{min_year}/{ (min_year + 1) % 100 :02d}"
    max_fy = f"{max_year}/{ (max_year + 1) % 100 :02d}"
    dashboard_title = f"Uganda Budget Analysis Dashboard (FY {min_fy} - {max_fy})"
    latest_year_str = max_year_str
    latest_fy = max_fy
else:
    dashboard_title = "Uganda Budget Analysis Dashboard (No Data Available)"
    latest_year_str = None
    latest_fy = "N/A"

# Initialize app
app = dash.Dash(__name__)

# Layout definition
app.layout = html.Div([
    html.H1(
        dashboard_title,
        style={'textAlign': 'center'}
    ),
    html.Div([
        html.Label("Select Sector:"),
        dcc.Dropdown(
            id='sector-dropdown',
            options=[{'label': s, 'value': s} for s in df['Sector'].unique()],
            value=df['Sector'].unique()[0] if not df.empty else None,
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
    # Trend figure
    if selected_sector:
        filtered_df = df[df['Sector'] == selected_sector]
        trend_fig = px.line(
            filtered_df, x='FinancialYear', y='Approved Budget',
            title=f'Allocation Trend for {selected_sector} (UGX)',
            labels={'Approved Budget': 'Allocation (UGX)', 'FinancialYear': 'Fiscal Year'},
            markers=True
        )
        # Optional: Format x-axis ticks to FY labels for better readability
        fy_labels = [f"{int(year[:4])}/{(int(year[:4]) + 1) % 100 :02d}" for year in filtered_df['FinancialYear']]
        trend_fig.update_layout(xaxis={'tickvals': filtered_df['FinancialYear'], 'ticktext': fy_labels})
    else:
        trend_fig = px.line(title='No Sector Selected')

    # Pie chart figure using dynamic latest year
    if latest_year_str:
        df_latest = df[df['FinancialYear'] == latest_year_str]
        if not df_latest.empty:
            pie_fig = px.pie(
                df_latest, values='Approved Budget', names='Sector',
                title=f'FY {latest_fy} Budget Share',
                labels={'Approved Budget': 'Allocation (UGX)'}
            )
            num_sectors = len(df_latest['Sector'].unique())
            pie_fig.update_traces(textinfo='percent+label', pull=[0.1] + [0] * (num_sectors - 1))
        else:
            pie_fig = px.pie(
                names=['No Data'], values=[1],
                title=f'FY {latest_fy} Budget Share (No Data Available)'
            )
            pie_fig.update_traces(textinfo='label', showlegend=False)
            pie_fig.update_layout(annotations=[dict(text=f'No data for FY {latest_fy}', x=0.5, y=0.5, showarrow=False)])
    else:
        pie_fig = px.pie(
            names=['No Data'], values=[1],
            title='Budget Share (No Data Available)'
        )
        pie_fig.update_traces(textinfo='label', showlegend=False)
        pie_fig.update_layout(annotations=[dict(text='No budget data available', x=0.5, y=0.5, showarrow=False)])

    # Prediction bar figure
    pred_fig = px.bar(
        pred_df, x='SectorName', y='Predicted_2022_UGX',
        title='Predicted Budget Allocations for FY 2022/23 (UGX)',
        labels={'Predicted_2022_UGX': 'Predicted Allocation (UGX)'}
    )
    
    return trend_fig, pie_fig, pred_fig

# Launch the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)