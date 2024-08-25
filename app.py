from metricas import cpi, spi, cv, sv, csi, etc, eac, bac

import streamlit as st
import pandas as pd

pv_column = "Planned Value (PV)"
ev_column = "Earned Value (EV)"
ac_column = "Actual Cost (AC)"


# Create an initial empty DataFrame
initial_data = {
    "Actividad": [""],
    pv_column: [0.0],
    ev_column: [0.0],
    ac_column: [0.0],
    "Semana": [0],
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

csv = edited_df.to_csv(index=False)

# # Create a download button
# st.download_button(
#     label="Download Data as CSV",
#     data=csv,
#     file_name='dataframe.csv',
#     mime='text/csv'
# )

# If you want to perform calculations based on the input data:
if st.button("Calcular metricas"):
    # Perform calculations using the input data
    edited_df[pv_column] = edited_df[pv_column].fillna(0)
    edited_df[ev_column ] = edited_df[ev_column].fillna(0)
    edited_df[ac_column] = edited_df[ac_column].fillna(0)
    semanas = edited_df["Semana"].unique()
    accumulated = []
    for semana in semanas:
        filtered_df = edited_df[edited_df['Semana'] <= semana]
        accumulated.append(filtered_df[[pv_column, ev_column, ac_column]].sum())
    result_df = pd.DataFrame(accumulated, index=semanas)
    result_df["CV"] = round(cv(result_df[ac_column], result_df[ev_column]), 2)
    result_df["SV"]= round(sv(result_df[pv_column], result_df[ev_column]), 2)
    result_df["CPI"] = cpi(result_df[ac_column], result_df[ev_column])
    result_df["SPI"] = spi(result_df[ev_column], result_df[pv_column])
    result_df["CSI/CR"] = csi(result_df["CPI"], result_df["SPI"])
    result_bac = round(bac(edited_df[pv_column]),2)
    result_df["EAC"] = round(eac(result_bac, result_df["CPI"]),2)
    result_df["ETC"] = round(etc(result_df["EAC"] , result_df[ac_column]),2)
    
    st.write("Resultado")
    st.write(result_df.T)

