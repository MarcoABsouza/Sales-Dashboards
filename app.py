import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title='Sales Dashboard',
    page_icon=':bar_chart:',
    layout='wide',
    
)

# Read EXCEL file
@st.cache_data
def get_data_from_excel():

    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl', # library used to read the excel file
        sheet_name='Sales', # Indicates the tab in the spreadsheet to be read
        skiprows=3, # Ignores the first desired lines
        usecols='B:R', # Indicates the columns to be loaded
        nrows=1000
    )
    # Add 'hour' column to dataframe
    df['hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour

    return df

df = get_data_from_excel()


# Sidebar
st.sidebar.header('Please Filter here:')
city = st.sidebar.multiselect(
    'Select the city:',
    options=df['City'].unique(), # City options to analyze
    default=df['City'].unique() 
)

customer_type = st.sidebar.multiselect(
    'Select the Customer Type:',
    options=df['Customer_type'].unique(), # Customer type options to analyze
    default=df['Customer_type'].unique() 
)

gender = st.sidebar.multiselect(
    'Select the Gender:',
    options=df['Gender'].unique(), # Gender options to analyze
    default=df['Gender'].unique() 
)

# Selects elements according to a search made using the city, customer type and gender parameters.
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# Main Page
st.title(':bar_chart: Sales Dashboard')
st.markdown('##')


# KPI's based on data
total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection['Total'].mean(), 2)

# Columns on the main page to view information
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader('Total Sales:')
    st.subheader(f'US $ {total_sales:,}')
with middle_column:
    st.subheader('Average Rating:')
    st.subheader(f'{average_rating} {star_rating}')
with right_column:
    st.subheader('Average Sales Per Transaction:')
    st.subheader(f'Us $ {average_sale_by_transaction}')

st.markdown('---')


# SALES BY PRODUCT LINE [BAR CHART]

# Groups sales by product line, adds up the totals, sorts in ascending order and resets the index
sales_by_product_line = (
    df_selection.groupby(by=['Product line'])[['Total']].sum().sort_values(by='Total').reset_index()
)

# bar chart
fig_product_sales = px.bar(
    sales_by_product_line,
    x='Total',
    y='Product line',
    orientation='h',
    title="<b>Sales by Product line </b>",
    color_discrete_sequence=['#0083B8'] * len(sales_by_product_line),
    template='plotly_white'
)

# SALES BY HOUR (BAR CHART)

# Groups sales by hour, adds up the totals, sorts in ascending order and resets the index
sales_by_hour = (
    df_selection.groupby(by=['hour'])[['Total']].sum().reset_index()
)

# Bar chart 
fig_hour_sales = px.bar(
    sales_by_hour,
    x='hour',
    y='Total',
    title="<b>Sales by hour</b>",
    color_discrete_sequence=['#0083B8'] * len(sales_by_hour),
    template='plotly_white'
)

# Plot chart
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales,use_container_width=True)
right_column.plotly_chart(fig_hour_sales, use_container_width=True)

st.markdown('---')

# GROSS INCOME BY CITY [HISTOGRAM CHART]
grossIncome_by_City = (
    df_selection.groupby(by=['City'])[['gross income']].sum().reset_index()
)

# Histogram chart
fig_gross_income_by_city = px.histogram(
    data_frame=grossIncome_by_City,
    x='City',
    y='gross income',
    title="<b>Gross Income by City</b>",
    color_discrete_sequence=['#0083B8'],
)

# PAYMENT METHODS [PIE CHART]
payment_methods = (
    df.groupby(by=['Payment'])[['Total']].sum().reset_index()
)
# Pie chart
fig_payment_methods = px.pie(
    data_frame=payment_methods,
    values='Total',
    names='Payment',
    title="<b>Types of payments in relation to the total </b>",
    color_discrete_sequence=['#0083B8', '#66C2FF', '#40E0D0'],
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_gross_income_by_city,use_container_width=True)
right_column.plotly_chart(fig_payment_methods, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)