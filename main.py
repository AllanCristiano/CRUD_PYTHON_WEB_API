import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DB_NAME = "db.sqlite3"
DB_FILE = ROOT_DIR / DB_NAME
TABLE_NAME = "customers"

# Conexão com o banco de dados
connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

# Criação da tabela se não existir
cursor.execute("CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cpf INTEGER, data_nascimento DATE)".format(TABLE_NAME))
connection.commit()

# Fechar o cursor após a criação da tabela
cursor.close()

# Criar uma instância do aplicativo FastAPI
app = FastAPI()

# Modelo de dados para o corpo da solicitação de inserção de usuário
class UserIn(BaseModel):
    name: str
    cpf: int
    data_nascimento: str

# Rota inicial
@app.get("/")
async def read_root():
    return {"message": "API crud em banco de dados"}

# Rota para inserir um novo usuário no banco de dados
@app.post("/users/")
async def create_user(user_in: UserIn):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO {} (name, cpf, data_nascimento) VALUES (?, ?, ?)".format(TABLE_NAME), (user_in.name, user_in.cpf, user_in.data_nascimento))
    connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    return {"user_id": user_id, **user_in.dict(), "message": "User created successfully"}

# Rota para buscar um usuário pelo nome
@app.get("/users/{name}")
async def read_user(name: str):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM {} WHERE name = ?".format(TABLE_NAME), (name,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        user_dict = {"id": user[0], "name": user[1], "cpf": user[2], "data_nascimento": user[3]}
        return user_dict
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Rota para remover um usuário pelo nome
@app.delete("/users/{name}")
async def delete_user(name: str):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM {} WHERE name = ?".format(TABLE_NAME), (name,))
    connection.commit()
    cursor.close()
    return {"name": name, "message": "User deleted successfully"}