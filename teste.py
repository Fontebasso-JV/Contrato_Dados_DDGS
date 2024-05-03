import pandas as pd
from schema import ContratoLayoutDDGS


file = r'C:\Users\joaoa\OneDrive\Documentos\INPASA\data\data.csv'

def validar(csv):
    '''
    Validar CSV conforme o contrato de dados
    '''
    try:

        df_raw = pd.read_csv(csv,delimiter=';')
        df = df_raw.head(1)
        erros = []

        for idx, row in df.iterrows():

            try:

                ContratoLayoutDDGS(**row.to_dict())

            
            except Exception as error:
                erros.append(f'Erro na linha: {idx+2}: {error}')

        if erros:
            print(f'Erros encontrados no arquivo enviado:')
            for erro in erros:
                print(erro)

        else:
            print('Arquivo Validado com Sucesso!')
            return True
    
    except Exception as err:
        print(f'Erro ao ler o arquivo: {err}')

validar(file)
    