import streamlit as st
import pandas as pd
from schema import ContratoLayoutDDGS
import time


# Definir o modo wide como padrão
st.set_page_config(
    layout="wide",
    page_title="DDGS - Validação",
    page_icon='📝')

st.title("DDGS Comercial - Validação de Arquivo")

def validar(csv):
    '''
    Validar CSV conforme o contrato de dados
    '''
    try:
        df = pd.read_csv(csv, delimiter=';')
        erros = []

        for idx, row in df.iterrows():
            try:
                # Convertendo as datas para o formato desejado
                row['Início Cadência'] = pd.to_datetime(row['Início Cadência'], format='%d/%m/%Y %H:%M')
                row['Data Pedido'] = pd.to_datetime(row['Data Pedido'], format='%d/%m/%Y %H:%M')
                row['Fim Cadência'] = pd.to_datetime(row['Fim Cadência'], format='%d/%m/%Y %H:%M')
                ContratoLayoutDDGS(**row.to_dict())
            except Exception as error:
                erros.append(f'Erro na linha: {idx+2}: {error}')

        if erros:
            st.error(f'Erros encontrados no arquivo enviado:')
            for erro in erros:
                st.error(erro)
        else:
            st.success('Arquivo Validado com Sucesso!')
            st.subheader("Pré-Visualização do arquivo: ")
            st.dataframe(df)

            # Reordenar e remover colunas conforme necessário
            df = df[['Status Pedido', 'Produto', 'Mercado', 'GEF', 'Nome Supervisor', 'Cód. Cliente',
                     'Nome', 'Data Pedido', 'Início Cadência', 'Fim Cadência', 'Pedido', 'Vol. Total Vendido', 'Vol. Total Carregado',
                     'Vol. Total Pendente', 'Forecast Total', 'Forecast jan/2024', 'Carregado jan/2024',
                     'Forecast fev/2024', 'Carregado fev/2024', 'Forecast mar/24', 'Carregado mar/2024', 'Forecast abr/24',
                     'Carregado abr/2024', 'Forecast mai/24', 'Carregado mai/2024', 'Forecast jun/24', 'Carregado jun/2024',
                     'Forecast jul/24', 'Carregado jul/2024', 'Forecast ago/24', 'Carregado ago/2024', 'Forecast set/2024',
                     'Carregado set/2024', 'Forecast out/2024', 'Carregado out/2024', 'Forecast nov/2024', 'Carregado nov/2024',
                     'Forecast dez/2024', 'Carregado dez/2024']]

            # Download do arquivo CSV
            csv_data = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="Baixar Arquivo", data=csv_data, file_name="arquivo_validado.csv", mime="text/csv")
            return True
    
    except Exception as Err:
        st.error(f'Erro na validação do arquivo! \n {Err}')

arquivo = st.file_uploader("Coloque aqui o seu arquivo para validar", type='csv')
botao = st.button(label="Validar Arquivo")

try:

    if botao:
        with st.spinner("Validando..."):
            time.sleep(2)
            validar(arquivo)
            st.write("---")
except Exception as err:
    st.error(f'Erro na tentativa de validação: {err}')
