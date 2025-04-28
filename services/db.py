import json

# Caminho para o arquivo JSON
CLIENTS_FILE = "services/db.json"

# Carregar os clientes do arquivo JSON
def load_clients():
    try:
        with open(CLIENTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Salvar os clientes no arquivo JSON
def save_clients(clients):
    with open(CLIENTS_FILE, "w") as file:
        json.dump(clients, file, indent=4)

CLIENTS = load_clients()