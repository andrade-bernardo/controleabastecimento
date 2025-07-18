import pandas as pd
from datetime import datetime

def exportar_excel(base, dados):
    filtrados = [d for d in dados if d["base"] == base]
    df = pd.DataFrame(filtrados)
    nome_arquivo = f"export_{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(nome_arquivo, index=False)
    return nome_arquivo
