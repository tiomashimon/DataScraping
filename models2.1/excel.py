import pandas as pd
from openpyxl import Workbook

df = pd.read_csv('models2.1/bicycle_offers.csv')

avg_prices = df.groupby(['Model', 'City'])['Price'].mean().reset_index()

avg_prices['Avg_Price_Model'] = avg_prices.groupby('Model')['Price'].transform('mean')

df['Above_Avg_Price'] = df['Price'] > df.merge(avg_prices, on=['Model', 'City'], how='left')['Avg_Price_Model']

def highlight_above_average(row):
    color = 'red' if row['Above_Avg_Price'] else 'white'
    return ['background-color: {}'.format(color) for _ in row]

styled_df = df.style.apply(highlight_above_average, axis=1)

excel_file = 'models2.1/bicycle_offers_highlighted.xlsx'
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    styled_df.to_excel(writer, index=False, sheet_name='Bicycle Offers')

    avg_prices.to_excel(writer, index=False, sheet_name='Average Prices')

    max_prices_chart = Workbook()
    max_prices_chart_sheet = max_prices_chart.active
    max_prices_chart_sheet.append(['Model', 'Max Price'])

    max_prices = df.groupby('Model')['Price'].max().reset_index()
    for _, row in max_prices.iterrows():
        max_prices_chart_sheet.append([row['Model'], row['Price']])

    max_prices_chart.save('models2.1/max_prices_chart.xlsx')
