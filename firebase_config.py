import firebase_admin
from firebase_admin import credentials, firestore
import os

# ESTE É O NOME EXATO DO ARQUIVO .JSON QUE VOCÊ BAIXOU!
# Certifique-se de que este arquivo (.json) está na MESMA PASTA
# que o seu 'firebase_config.py' e 'app.py'.
SERVICE_ACCOUNT_FILE_NAME = 'abastecimento-onibus-firebase-adminsdk-fbsvc-6766186fb8.json'

# =========================================================================
# O CÓDIGO ABAIXO IRÁ FAZER A INICIALIZAÇÃO DO FIREBASE ADMIN SDK
# =========================================================================

# Construímos o caminho completo para o arquivo de credenciais.
# os.path.dirname(__file__) pega o diretório atual do firebase_config.py
# os.path.join() junta o diretório com o nome do arquivo .json
path_to_service_account = os.path.join(os.path.dirname(__file__), SERVICE_ACCOUNT_FILE_NAME)

# Variável para armazenar as credenciais, iniciamos como None
cred = None

# 1. Tenta carregar as credenciais de uma VARIÁVEL DE AMBIENTE primeiro (Melhor para PRODUÇÃO como o Render)
# Esta parte é mais para o futuro, quando você for para o Render.
# Se você tiver uma variável de ambiente 'FIREBASE_SERVICE_ACCOUNT_JSON' com o conteúdo do seu .json
# no Render, esta parte será usada.
if os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON"):
    try:
        import json # Importamos json apenas se precisarmos dele aqui
        # Carrega o conteúdo JSON da variável de ambiente
        cred_dict = json.loads(os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON"))
        cred = credentials.Certificate(cred_dict)
        print("Firebase Admin SDK: Credenciais carregadas de variável de ambiente (FIREBASE_SERVICE_ACCOUNT_JSON).")
    except Exception as e:
        print(f"ATENÇÃO: Erro ao carregar credenciais da variável de ambiente. Tentando arquivo local. Detalhes: {e}")
        # Se falhou na variável de ambiente, vamos tentar o arquivo local.

# 2. Se as credenciais não foram carregadas da variável de ambiente, tenta do ARQUIVO LOCAL
if cred is None: # Só tenta o arquivo local se 'cred' ainda não foi definido
    if os.path.exists(path_to_service_account):
        try:
            cred = credentials.Certificate(path_to_service_account)
            print(f"Firebase Admin SDK: Credenciais carregadas do arquivo local: {SERVICE_ACCOUNT_FILE_NAME}.")
        except Exception as e:
            print(f"ERRO CRÍTICO: Problema ao carregar o arquivo de credenciais local '{SERVICE_ACCOUNT_FILE_NAME}'. Detalhes: {e}")
            print("Verifique se o arquivo .json não está corrompido.")
            # Levanta a exceção para que o app não continue se as credenciais estiverem ruins
            raise
    else:
        # Se o arquivo .json não foi encontrado e a variável de ambiente não funcionou
        print(f"ERRO CRÍTICO: Arquivo de chave de serviço '{SERVICE_ACCOUNT_FILE_NAME}' NÃO FOI ENCONTRADO.")
        print("E a variável de ambiente 'FIREBASE_SERVICE_ACCOUNT_JSON' também não está configurada ou é inválida.")
        print("Por favor, certifique-se de que o arquivo .json está na mesma pasta que 'firebase_config.py', OU configure a variável de ambiente corretamente.")
        # O aplicativo não pode continuar sem as credenciais
        raise FileNotFoundError(f"Credenciais Firebase não encontradas: {SERVICE_ACCOUNT_FILE_NAME}")

# 3. Inicializa o app Firebase Admin SDK com as credenciais obtidas
try:
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK inicializado com sucesso!")
except Exception as e:
    # Este erro ocorre se a inicialização do Firebase falhar mesmo com credenciais válidas
    print(f"ERRO CRÍTICO: Não foi possível inicializar o Firebase Admin SDK. Detalhes: {e}")
    # Levanta a exceção para garantir que o app não prossiga sem o Firebase funcionando
    raise

# =========================================================================
# FIM DA INICIALIZAÇÃO DO FIREBASE ADMIN SDK
# =========================================================================

# Esta é a sua instância do cliente Firestore.
# Seu 'app.py' importará 'db' para interagir com o Firestore.
db = firestore.client()

