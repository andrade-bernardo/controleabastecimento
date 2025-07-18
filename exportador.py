import pandas as pd
from datetime import datetime
import os

def exportar_excel(base, dados):
    # Filtra apenas os dados da base atual
    filtrados = [d for d in dados if d["base"] == base]
    
    # Cria DataFrame
    df = pd.DataFrame(filtrados)

    # Garante que o diretório /tmp existe (Render só permite escrita nele)
    diretorio_tmp = "/tmp"
    if not os.path.exists(diretorio_tmp):
        os.makedirs(diretorio_tmp)

    # Cria o caminho completo do arquivo
    nome_arquivo = os.path.join(diretorio_tmp, f"export_{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")

    # Salva o arquivo Excel
    df.to_excel(nome_arquivo, index=False)

    # Retorna o caminho para o send_file
    return nome_arquivo

