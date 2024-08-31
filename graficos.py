import matplotlib.pyplot as plt

def plot_grafico_cpi_spi(df):
    #Genera un gráfico de CPI vs SPI
    fig, ax = plt.subplots()
    
    if 'CPI' in df.columns and 'SPI' in df.columns:
        ax.plot(df.index, df['CPI'], label='CPI', marker='o')
        ax.plot(df.index, df['SPI'], label='SPI', marker='o')
        ax.set_title('CPI vs SPI')
        ax.set_xlabel('Índice de Semana')
        ax.set_ylabel('Valor')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'Datos no disponibles', horizontalalignment='center', verticalalignment='center')
        ax.set_title('CPI vs SPI')
    
    plt.tight_layout()
    return fig

def plot_grafico_cv_sv(df):
    #Genera un gráfico de CV vs SV
    fig, ax = plt.subplots()
    
    if 'CV' in df.columns and 'SV' in df.columns:
        ax.plot(df.index, df['CV'], label='CV', marker='o')
        ax.plot(df.index, df['SV'], label='SV', marker='o')
        ax.set_title('CV vs SV')
        ax.set_xlabel('Índice de Semana')
        ax.set_ylabel('Valor')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'Datos no disponibles', horizontalalignment='center', verticalalignment='center')
        ax.set_title('CV vs SV')
    
    plt.tight_layout()
    return fig

def plot_grafico_eac_etc(df):
    #Genera un gráfico de EAC vs ETC
    fig, ax = plt.subplots()
    
    if 'EAC' in df.columns and 'ETC' in df.columns:
        ax.plot(df.index, df['EAC'], label='EAC', marker='o')
        ax.plot(df.index, df['ETC'], label='ETC', marker='o')
        ax.set_title('EAC vs ETC')
        ax.set_xlabel('Índice de Semana')
        ax.set_ylabel('Valor')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'Datos no disponibles', horizontalalignment='center', verticalalignment='center')
        ax.set_title('EAC vs ETC')
    
    plt.tight_layout()
    return fig
