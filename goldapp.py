import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import plotly.express as px


# Replace 'sheet_name' with the actual sheet names in your Excel file
sheet_names = ['yearly', 'monthly', 'quarterly', 'daily']

# Load data for each sheet
df = pd.read_excel('goldprice.xlsx', sheet_name='daily')

# Conversion factor for ounces to grams
ounce_to_gram = 31.1035
# Streamlit app
st.title('Gold Price Explorer')

currency_options = df.columns[1:]
selected_currency = st.selectbox("Select Currency", currency_options)


weight_options = ["Per Ounce", "Per Gram"]
selected_weight = st.selectbox("Select Weight", weight_options)


date_range_buttons = ["7D", "1M", "3M", "1Y", "3Y", "Max"]
selected_date_range = st.radio("Select Date Range", date_range_buttons,index=0, format_func=lambda x: f"{x} ")
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)





# Determine start and end dates based on selected date range
end_date = max(df['date'])
if selected_date_range == "7D":
    start_date = end_date - timedelta(days=7)
elif selected_date_range == "1M":
    start_date = end_date - timedelta(days=30)
elif selected_date_range == "3M":
    start_date = end_date - timedelta(days=90)
elif selected_date_range == "1Y":
    start_date = end_date - timedelta(days=365)
elif selected_date_range == "3Y":
    start_date = end_date - timedelta(days=3*365)
else:
    start_date = min(df['date'])

# Filter data based on currency and date range
filtered_df = df.loc[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Function to filter data based on currency and weight
# Convert prices based on selected weight
if selected_weight == "Per Gram":
    # Convert prices from ounces to grams
    filtered_df[selected_currency] /= 31.1035

# Chart Generation
# Plotting the data
# Plotting the data with gold-like colors
# Create a line plot with hover data
# Plotting the data with gold-like colors
fig = px.line(filtered_df, x='date', y=selected_currency,
              labels={'date': 'Date', selected_currency: f"Price ({selected_weight})"},
              line_shape='linear', render_mode='svg')

# Customize the appearance with gold-like colors
fig.update_layout(
    title=f"Gold Price in {selected_currency} ({selected_weight})",
    xaxis_title="Date",
    yaxis_title=f"Price ({selected_weight})",
    hovermode="x",
    showlegend=True,
    template="plotly_dark",
    plot_bgcolor='#212121',  # Light Goldenrod Yellow
    paper_bgcolor='#2E2E2E',  # Light Goldenrod Yellow
    font=dict(color='#FFFFFF'),  # SaddleBrown
)

# Add a gold coin marker at the last data point
last_date = filtered_df['date'].iloc[-1]
last_price = filtered_df[selected_currency].iloc[-1]
fig.add_trace(
    px.scatter(x=[last_date],
               y=[last_price],
               ).update_traces(
                   marker=dict(symbol='circle', size=12, color='gold', line=dict(color='black', width=2))
               ).data[0]
)

# Display the graph
st.plotly_chart(fig)


# Additional info

