import streamlit as st
import pandas as pd

from metricas import cpi, spi, cv, sv, csi, etc, eac, bac
from graficos import plot_grafico_cpi_spi, plot_grafico_cv_sv, plot_grafico_eac_etc
from export import exportar_excel

# Agregar el nombre del proyecto y el logo en el sidebar
st.sidebar.image('assets/logo.jpeg', use_column_width=True)  
st.sidebar.title('ECP Valor Ganado')
st.sidebar.subheader('Integrantes del Equipo')
st.sidebar.text('Inés Alarcón')
st.sidebar.text('Eddy Cabrera')
st.sidebar.text('Byron Mendez')
st.sidebar.text('Carlos Morales')

# Solicitar el nombre del proyecto
st.write("Ingrese el nombre de su proyecto:")
nombre_proyecto = st.text_input("", "")

pv_column = "Planned Value (PV)"
ev_column = "Earned Value (EV)"
ac_column = "Actual Cost (AC)"

# Crear un DataFrame inicial vacío
initial_data = {
    "Actividad": [""],
    pv_column: [0.0],
    ev_column: [0.0],
    ac_column: [0.0],
    "Semana": [0],
}

df_initial = pd.DataFrame(initial_data)

# Mostrar la tabla en Streamlit y permitir a los usuarios editarla
edited_df = st.data_editor(df_initial, num_rows="dynamic", use_container_width=True)

# Inicializar el estado de la sesión para resultados y figuras si no existen
if 'result_df' not in st.session_state:
    st.session_state.result_df = pd.DataFrame()
if 'figures' not in st.session_state:
    st.session_state.figures = {}

def datos_son_iniciales(df):
    # Comparar cada columna con sus valores iniciales
    for column in df.columns:
        if not (df[column] == df_initial[column][0]).all():
            return False
    return True

def calcular_metricas(edited_df):
    # Verificar si el DataFrame contiene solo los valores iniciales
    if datos_son_iniciales(edited_df):
        st.warning("Los datos no se han modificado. Por favor, ingrese datos significativos para calcular las métricas.")
        return None

    # Verificar si el DataFrame tiene datos válidos
    if not edited_df[[pv_column, ev_column, ac_column]].apply(pd.Series.notnull).any().any():
        st.warning("No se ha ingresado ninguna información válida. Por favor, ingrese datos para calcular las métricas.")
        return None

    edited_df[pv_column] = edited_df[pv_column].fillna(0)
    edited_df[ev_column] = edited_df[ev_column].fillna(0)
    edited_df[ac_column] = edited_df[ac_column].fillna(0)
    semanas = edited_df["Semana"].unique()
    accumulated = []

    for semana in semanas:
        filtered_df = edited_df[edited_df['Semana'] <= semana]
        accumulated.append(filtered_df[[pv_column, ev_column, ac_column]].sum())
    result_df = pd.DataFrame(accumulated, index=semanas)

    try:
        result_df["CV"] = round(cv(result_df[ac_column], result_df[ev_column]), 2)
        result_df["SV"] = round(sv(result_df[pv_column], result_df[ev_column]), 2)
        result_df["CPI"] = cpi(result_df[ac_column], result_df[ev_column])
        result_df["SPI"] = spi(result_df[ev_column], result_df[pv_column])
        result_df["CSI/CR"] = csi(result_df["CPI"], result_df["SPI"])
        result_bac = round(bac(edited_df[pv_column]), 2)
        result_df["EAC"] = round(eac(result_bac, result_df["CPI"]), 2)
        result_df["ETC"] = round(etc(result_df["EAC"], result_df[ac_column]), 2)

        # Guardar resultados en el estado de la sesión
        st.session_state.result_df = result_df

        return result_df

    except ZeroDivisionError as e:
        st.error(f"Error en el cálculo: {e}")
        return None
    except Exception as e:
        st.error(f"Se produjo un error inesperado: {e}")
        return None

# Calcular métricas si se presiona el botón
if st.button("Calcular métricas"):
    result_df = calcular_metricas(edited_df)
    
    if result_df is not None:
        st.write("Resultado")
        st.write(result_df.T)

        # Gráficos
        st.write("Gráficos de Desempeño del Proyecto")
        if 'figures' not in st.session_state or not st.session_state.figures:
            fig1 = plot_grafico_cpi_spi(result_df)
            fig2 = plot_grafico_cv_sv(result_df)
            fig3 = plot_grafico_eac_etc(result_df)

            # Guardar figuras en el estado de la sesión
            st.session_state.figures['fig1'] = fig1
            st.session_state.figures['fig2'] = fig2
            st.session_state.figures['fig3'] = fig3
        else:
            fig1 = st.session_state.figures['fig1']
            fig2 = st.session_state.figures['fig2']
            fig3 = st.session_state.figures['fig3']

        st.pyplot(fig1)
        st.pyplot(fig2)
        st.pyplot(fig3)

# Exportar
if st.button("Exportar Informe Excel"):
    if not nombre_proyecto:
        st.error("Por favor, ingrese un nombre para su proyecto antes de exportar.")
    else:
        result_df = st.session_state.get('result_df', None)
        
        if result_df is not None and not result_df.empty:
            excel_filename = exportar_excel(edited_df, result_df.T, [
                {'path': 'grafico_cpi_spi.png', 'title': 'Gráfico CPI vs SPI'},
                {'path': 'grafico_cv_sv.png', 'title': 'Gráfico CV vs SV'},
                {'path': 'grafico_eac_etc.png', 'title': 'Gráfico EAC vs ETC'}
            ], nombre_proyecto)
            st.success(f"Informe Excel generado exitosamente: {excel_filename}")

            # Descargar el archivo
            if excel_filename:
                with open(excel_filename, "rb") as file:
                    st.download_button(
                        label="Descargar Informe Excel",
                        data=file,
                        file_name=f"{nombre_proyecto}_informe_resultados.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        else:
            st.error("No se ha calculado ningún resultado. Por favor, calcule las métricas primero.")
