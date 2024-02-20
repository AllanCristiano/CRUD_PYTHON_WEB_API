import requests

BASE_URL = "http://localhost:8000"  # URL base da sua API

# Dados de exemplo para inserção de usuário
user_data = {
    "name": "John Doe",
    "cpf": 12345678900,
    "data_nascimento": "1990-01-01"
}

name_to_search = "John Doe"

# Inserir um novo usuário
def add_usuario():    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print("Inserção de usuário:")
    print(response.json())

# Buscar um usuário pelo nome
def search_usuario():    
    response = requests.get(f"{BASE_URL}/users/{name_to_search}")
    print("\nBusca de usuário pelo nome:")
    print(response.json())

# Remover um usuário pelo nome
def remove_usuario():
    response = requests.delete(f"{BASE_URL}/users/{name_to_search}")
    print("\nRemoção de usuário pelo nome:")
    print(response.json())
    

# add_usuario()
# search_usuario()
remove_usuario()

