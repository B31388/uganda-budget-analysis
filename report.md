Author
Mugimba Kakure Jude
B31388
REG No. J25M19/034

Objective
To conduct Sector allocation analysis: which areas receive the most? The objective is to dive into sector-level budget allocations to understand funding patterns, conduct fairness analysis, and model future shifts.

Data Sources and Wrangling:
I sourced data from https://www.budget.finance.go.ug/content/ covering the seven Financial Years from FY2015-2016 to FY2021-2022. I combined them into one data set, cleaned it and saved as "uganda_budget_cleaned" using 'data_wrangling.py'.
Trends Analysis; Which area recieved most:
Through 'eda.ipynb' then used a Line chart, Bar chart and Box plot  visualize the trends of sector allocation for all the historical data for the seven years,  It was revealed that Interests on payments recieved the most allocation. An interactive pie chart was done do demontrate this for the most recent year 2021/2022

Funding Patterns:
The visuals indicate a general increase in budget allocation in all sectors likely attributable to economic growth of the country. Budget allocations for interest on payments and works and transport indicate commitment by government to infrastrutural development with these two sectors taking more than a third of the pie.

Fairness analysis
Fairness analysis was conducted through the 'modeling.ipynb', per Capita allocations were calculated for fairness anlysis with an approximate population of 46,000,000 people in uganda. the findings revealed that Interest Payments consistently receive the highest allocations across all years.Education and Health are among the top-funded sectors after Interest Payments, with Education allocations growing from 2.346264e+12 UGX in 2015 to 3.398518e+12 UGX in 2019, and Health from 1.315735e+12 UGX to 2.595382e+12 UGX. However, their growth rates are modest compared to Interest Payments or Works and Transport, raising questions about whether these critical sectors are adequately prioritized relative to population needs.
Sectors like Social Development, ICT and National Guidance, and Tourism consistently receive lower allocations.he heavy allocation to Interest Payments and infrastructure (Works and Transport) may reflect fiscal constraints or strategic priorities but could compromise fairness if it limits resources for sectors like Health, Education, or Social Development, which directly impact human development and equity.

Predictive Modeling:

Challenges:
Uganda changed from sector based budgeting to program based budgeting (PBB) from the FY2022-2023. The data sets formats changed and some sectors were interacted making predictive patterns based on historical data difficult.
Action taken:
The seven years data was extraporated through Linear Regression and the model predicted the budget alocation for the financial year 2022-2023. The results were cosistent with the budget allocations of the same year with interest and payments and Works and transport continuing to that the lion's share.

Findings:
Highest Allocations:
Interest Payments (12.76T UGX) and Works and Transport (8.17T UGX) have the largest predicted budgets, reflecting significant government priorities in debt servicing and infrastructure development.
Education (4.12T UGX), Energy and Mineral Development (3.60T UGX), and Health (3.50T UGX) also show substantial allocations, emphasizing human capital and energy sectors.
Prediction Accuracy (R²):
Sectors like Energy and Mineral Development and Tourism have R² values of 1.0, indicating perfect model fit, though this could suggest overfitting or limited variability in the data.
Education (0.97), Health (0.95), and Interest Payments (0.95) have high R² values, showing strong predictive reliability.
Tourism, Trade and Industry (0.02) and Public Administration (0.23) have low R² values, indicating poor model fit and less reliable predictions.
Prediction Error (RMSE):
Security (622B UGX) and Works and Transport (304B UGX) have the highest RMSE, suggesting larger prediction errors, possibly due to volatile or complex budgeting factors.
Sectors like Tourism (0 UGX) and Energy and Mineral Development (0.03 UGX) have negligible RMSE, implying highly precise predictions.
Most sectors have RMSE in the range of 10B–200B UGX, indicating moderate prediction errors relative to their budget sizes.
Key Insights:
Sectors with high budgets (e.g., Interest Payments, Works and Transport) tend to have higher RMSE, reflecting challenges in predicting large, complex allocations.
Sectors like Education and Health show both high allocations and strong predictive accuracy (high R², moderate RMSE), suggesting stable budgeting patterns.
Smaller sectors like ICT and National Guidance (228B UGX) and Tourism, Trade and Industry (192B UGX) have lower budgets and relatively low RMSE, but their R² varies, indicating mixed reliability.

Recommended action:
Aggregate data into sector allocations from financial year, 2022-2023 to 2025-2026 approved budgets and use the combined datasets to predict 2026/2027 budget.


requirements.txt
dash==3.1.1
pandas==2.3.1
plotly==6.2.0
openpyxl==3.1.5
seaborn==0.13.2
matplotlib==3.10.3
numpy==2.3.1
scikit-learn==1.7.0
kaleido==1.0.0

Mugimba Kakure Jude
End.

