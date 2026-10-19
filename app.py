from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Sales Analytics Dashboard', page_icon='📊', layout='wide')
st.title('📊 Sales Analytics Dashboard')
st.caption('Explore revenue, profit, orders, and product performance.')

REQUIRED = {'Date', 'Order_ID', 'Product', 'Category', 'Quantity', 'Unit_Price', 'Unit_Cost'}
file = st.sidebar.file_uploader('Upload your sales CSV (optional)', type=['csv'])
try:
    df = pd.read_csv(file if file is not None else Path(__file__).parent / 'data' / 'sample_sales.csv')
    missing = REQUIRED - set(df.columns)
    if missing:
        st.error('Missing CSV columns: ' + ', '.join(sorted(missing)))
        st.stop()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    for col in ['Quantity', 'Unit_Price', 'Unit_Cost']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Date', 'Order_ID', 'Product', 'Category', 'Quantity', 'Unit_Price', 'Unit_Cost']).copy()
    df = df[(df['Quantity'] > 0) & (df['Unit_Price'] >= 0) & (df['Unit_Cost'] >= 0)].copy()
    if df.empty:
        st.warning('No valid sales rows found.')
        st.stop()
except Exception as exc:
    st.error(f'Could not load the CSV: {exc}')
    st.stop()

df['Sales'] = df['Quantity'] * df['Unit_Price']
df['Profit'] = df['Quantity'] * (df['Unit_Price'] - df['Unit_Cost'])

st.sidebar.header('Filters')
start, end = st.sidebar.date_input('Date range', value=(df['Date'].min().date(), df['Date'].max().date()), min_value=df['Date'].min().date(), max_value=df['Date'].max().date())
if start > end:
    st.error('Start date must be before end date.')
    st.stop()
categories = sorted(df['Category'].astype(str).unique())
selected = st.sidebar.multiselect('Categories', categories, default=categories)
filtered = df[df['Date'].dt.date.between(start, end) & df['Category'].isin(selected)].copy()
if filtered.empty:
    st.info('No sales match these filters.')
    st.stop()

currency = st.sidebar.text_input('Currency symbol', value='Rs.')
a, b, c, d = st.columns(4)
a.metric('Total Sales', f'{currency} {filtered["Sales"].sum():,.2f}')
b.metric('Total Profit', f'{currency} {filtered["Profit"].sum():,.2f}')
c.metric('Orders', f'{filtered["Order_ID"].nunique():,}')
d.metric('Units Sold', f'{filtered["Quantity"].sum():,.0f}')

filtered['Month'] = filtered['Date'].dt.to_period('M').astype(str)
monthly = filtered.groupby('Month', as_index=False)['Sales'].sum()
category = filtered.groupby('Category', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)
left, right = st.columns(2)
with left:
    st.plotly_chart(px.line(monthly, x='Month', y='Sales', markers=True, title='Monthly Sales Trend'), use_container_width=True)
with right:
    st.plotly_chart(px.bar(category, x='Category', y='Sales', title='Sales by Category'), use_container_width=True)

top = filtered.groupby('Product', as_index=False)['Sales'].sum().nlargest(10, 'Sales')
st.plotly_chart(px.bar(top, x='Sales', y='Product', orientation='h', title='Top 10 Products by Revenue'), use_container_width=True)
st.subheader('Sales Records')
st.dataframe(filtered.drop(columns=['Month']).sort_values('Date', ascending=False), use_container_width=True, hide_index=True)
st.download_button('⬇️ Download Filtered CSV', filtered.drop(columns=['Month']).to_csv(index=False).encode('utf-8'), 'filtered_sales.csv', 'text/csv')
