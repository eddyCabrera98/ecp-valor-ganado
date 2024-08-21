from metricas import cpi, spi, cv, sv, csi, etc, eac

import streamlit as st
import pandas as pd

# Create an initial empty DataFrame
initial_data = {
    "Actividad": [""],
    "Earned Value (EV)": [0.0],
    "Planned Value (PV)": [0.0],
    "Actual Cost (AC)": [0.0],
    "Periodo": [0],
}

df = pd.DataFrame(initial_data)

# Display the table in Streamlit and allow users to edit it
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# # Dropdown to select a row to copy
# row_to_copy = st.selectbox("Select a row to copy:", edited_df.index, format_func=lambda x: f"Row {x + 1}")

# # Button to copy the selected row
# if st.button("Copy Selected Row"):
#     # Copy the selected row and append it to the DataFrame
#     row_copy = edited_df.iloc[row_to_copy].copy()
#     edited_df = pd.concat([edited_df, row_copy], ignore_index=True)
#     st.success(f"Row {row_to_copy + 1} copied successfully!")

#     # Display the updated DataFrame
#     st.write("Updated Table")
#     st.write(edited_df)

# else:
# Once the data is edited, you can display the DataFrame or use it further
# st.write("Edited Data:")
# st.write(edited_df)

# If you want to perform calculations based on the input data:
if st.button("Calculate Metrics"):
    # Perform calculations using the input data
    df = pd.DataFrame(columns=edited_df["Periodo"].unique(), index=["CV", "SV", "CPI", "SPI", "CSI/CR", "ETC", "EAC"])
    st.write("Calculated Metrics:")
    st.write(df)
