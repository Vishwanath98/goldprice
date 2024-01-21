import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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

# Date range selector
start_date = pd.to_datetime(st.date_input("Select Start Date", min(df["date"])))
end_date = pd.to_datetime(st.date_input("Select End Date", max(df["date"])))


# Filter data based on currency and date range
filtered_df = df.loc[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Function to filter data based on currency and weight
# Convert prices based on selected weight
if selected_weight == "Per Gram":
    # Convert prices from ounces to grams
    filtered_df[selected_currency] *= 31.1035

# Chart Generation
# Plotting the data
# Plotting the data with gold-like colors
plt.figure(figsize=(10, 6))
plt.plot(filtered_df['date'], filtered_df[selected_currency], color="#FFD700", label="Gold Price")
plt.title(f"Gold Price in {selected_currency} ({selected_weight})")
plt.xlabel("Date")
plt.ylabel(f"Price ({selected_weight})")

# Add a gold coin marker at the last data point
last_date = filtered_df['date'].iloc[-1]
last_price = filtered_df[selected_currency].iloc[-1]
plt.scatter(last_date, last_price, color="#FFD700", marker="o", s=100, label="Last Data Point")

# Beautify the graph
plt.legend()
plt.grid(True)
plt.tight_layout()

# Display the graph
st.pyplot()

# Additional info
st.write("Note: Prices in the dataset are originally per ounce. Converted to grams if selected weight is per gram.")