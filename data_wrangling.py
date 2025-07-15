import pandas as pd
import numpy as np

# Define Excel file paths
file_paths = [
    '/workspaces/uganda-budget-analysis/budget_datasets/budget_fy_15_16.xlsx',
    '/workspaces/uganda-budget-analysis/budget_datasets/budget_fy_16_17.xlsx',
    '/workspaces/uganda-budget-analysis/budget_datasets/budget_fy_17_18.xlsx',
    '/workspaces/uganda-budget-analysis/budget_datasets/budget_fy_18_19.xlsx',
    '/workspaces/uganda-budget-analysis/budget_datasets/budget_fy_19_20.xlsx',
    '/workspaces/uganda-budget-analysis/budget_datasets/budget_fy_20_21.xlsx',
    '/workspaces/uganda-budget-analysis/budget_datasets/budget_fy_21_22.xlsx'
]

# Load and tag each DataFrame with the fiscal year
dfs = []
for path in file_paths:
    fy = path.split('_fy_')[1].split('.xlsx')[0].replace('_', '/')
    df_temp = pd.read_excel(path, engine='openpyxl')
    df_temp['FinancialYear'] = f'20{fy}'
    dfs.append(df_temp)

# Combine all years into one DataFrame
df = pd.concat(dfs, ignore_index=True)

# Map the observed unique sector values to standardized names
sector_mapping = {
    'agriculture': 'Agriculture',
    'lands, housing and urban development': 'Lands, Housing and Urban Development',
    'energy': 'Energy',
    'works and transport': 'Works and Transport',
    'information and communication technology': 'ICT and National Guidance',
    'tourism, trade and industry': 'Tourism, Trade and Industry',
    'education': 'Education',
    'health': 'Health',
    'water and environment': 'Water and Environment',
    'social development': 'Social Development',
    'security': 'Security',
    'justice, law and order': 'Justice, Law and Order',
    'public sector management': 'Public Sector Management',
    'accountability': 'Accountability',
    'public administration': 'Public Administration',
    'legislature': 'Legislature',
    'interest payments': 'Interest Payments',
    'trade and industry': 'Tourism, Trade and Industry',
    'energy and mineral development': 'Energy and Mineral Development',
    'ict and national guidance': 'ICT and National Guidance',
    'science, technology and innovation': 'Science, Technology and Innovation',
    'tourism': 'Tourism'
}

df['Sector'] = (
    df['Sector']
    .str.lower()
    .str.strip()
    .map(sector_mapping)
)

# Handle any unmapped or missing sectors
df = df.dropna(subset=['Sector'])


# Ensure 'Approved Budget' is numeric
df['Approved Budget'] = pd.to_numeric(df['Approved Budget'], errors='coerce')

# Fill missing budgets—no chained assignment
df['Approved Budget'] = df['Approved Budget'].fillna(df['Approved Budget'].mean())

# Normalize FinancialYear and convert to datetime (June 1 of fiscal year)
df['FinancialYear'] = (
    df['FinancialYear']
    .str.replace(r'[–‑]', '/', regex=True)
    .str.split('/', expand=True)[0]
    + '-06-01'
)
df['FinancialYear'] = pd.to_datetime(df['FinancialYear'], format='%Y-%m-%d', errors='coerce')

# Drop any records with invalid dates
df = df.dropna(subset=['FinancialYear'])

# Aggregate total approved budget by sector and fiscal year
df_cleaned = (
    df.groupby(['FinancialYear', 'Sector'], as_index=False)['Approved Budget']
    .sum()
)

# Save to CSV
output = '/workspaces/uganda-budget-analysis/uganda_budget_cleaned.csv'
df_cleaned.to_csv(output, index=False)
print(f"✅ Cleaned dataset saved to '{output}'")
