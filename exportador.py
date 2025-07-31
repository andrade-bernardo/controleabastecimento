import pandas as pd
from datetime import datetime
import os

def exportar_excel(base, dados):
    # Filtra apenas os dados da base atual
    filtrados = [d for d in dados if d.get("base") == base]

    # Garante que o diretório /tmp existe (Render só permite escrita nele)
    diretorio_tmp = "/tmp"
    if not os.path.exists(diretorio_tmp):
        os.makedirs(diretorio_tmp)

    # Evita erro com DataFrame vazio
    if not filtrados:
        df = pd.DataFrame(columns=["data", "hora", "onibus", "litros", "responsavel", "base"])
    else:
        df = pd.DataFrame(filtrados)
        # Ordena colunas, se existirem
        colunas = ["data", "hora", "onibus", "litros", "responsavel", "base"]
        df = df[[c for c in colunas if c in df.columns]]

    # Cria nome do arquivo
    nome_arquivo = os.path.join(
        diretorio_tmp, f"export_{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    # Salva o Excel
    df.to_excel(nome_arquivo, index=False)

    return nome_arquivo
