import streamlit as st
import pandas as pd
import time
from schema import ContratoLayoutDDGS
from datetime import datetime

st.title("DDGS Comercial - ForeCast")


def carregar(file):
    df2 = pd.read_csv(file,delimiter=';')
    return df2.head(10)

st.subheader("Carregue aqui o seu arquivo")
file = st.file_uploader("Coloque aqui o seu arquivo",type='csv')

if file:
    try:
        with st.spinner('Aguarde...'):
            time.sleep(2)
            df2 = carregar(file)
        st.dataframe(df2)
    except Exception as err:
        st.write(f'Erro no upload: {err}')

if file:
    try:

        df3 = carregar(file)
        lista = []
        for  row in df3.iterrows():
            lista.append(row[1].tolist())
        
        st.write(lista)
    
    except Exception as err:
        st.write(f'Erro: {err}')

#######################################################################

def validar(csv):
    '''
    Validar CSV conforme o contrato de dados
    '''
    try:

        df = pd.read_csv(csv,delimiter=';')
        erros = []

        for idx, row in df.iterrows():

            try:

                ContratoLayoutDDGS(**row.to_dict())

            
            except Exception as error:
                erros.append(f'Erro na linha: {idx+2}: {error}')

        if erros:
            st.error(f'Erros encontrados no arquivo enviado:')
            for erro in erros:
                st.error(erro)

        else:
            st.success('Arquivo Validado com Sucesso!')
            return True
    
    except Exception as err:
        st.write(f'Erro ao ler o arquivo: {err}')

botao = st.button(label="Validar Arquivo")

if botao:
    validar(file)