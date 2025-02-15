# ✨ Guia Completo: Site com GraphQL + MongoDB + Python (Ariadne)

## ✨ Estrutura do Projeto
1. **Backend (Python)**
   - API GraphQL usando **Ariadne**
   - Conexão com **MongoDB** através de **Motor** (async) ou **PyMongo** (sync)
   - Definição do esquema GraphQL e resolvers

2. **Base de Dados (MongoDB)**
   - Instalar e configurar MongoDB
   - Criar uma coleção e inserir dados

3. **Frontend**
   - Pode ser **React, Vue, Angular ou HTML+JS puro**
   - Fazer chamadas à API GraphQL

---

## ✅ 1. Configuração do Backend (Python + FastAPI + GraphQL)

### 📌 Passo 1: Criar e ativar um ambiente virtual
```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

### 📌 Passo 2: Instalar dependências
```sh
pip install fastapi ariadne motor uvicorn
```
- `fastapi` → Framework web para a API  
- `ariadne` → Biblioteca GraphQL para Python  
- `motor` → Driver assíncrono para MongoDB  
- `uvicorn` → Servidor ASGI para rodar a API  

---

### 📌 Passo 3: Criar o Modelo MongoDB
Cria um ficheiro **`models.py`**:

```python
import motor.motor_asyncio
from bson import ObjectId

# Conectar ao MongoDB
MONGO_URI = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["mydatabase"]
collection = db["users"]

def serialize_user(user):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }
```

---

### 📌 Passo 4: Criar a API GraphQL
Cria um ficheiro **`server.py`**:

```python
from fastapi import FastAPI
from ariadne.asgi import GraphQL
from ariadne import QueryType, MutationType, make_executable_schema


from models import collection, serialize_user

# Definir o esquema
query = QueryType()
mutation = MutationType()

@query.field("getUsers")
async def resolve_get_users(_, info):
    users = await collection.find().to_list(100)
    return [serialize_user(user) for user in users]

@mutation.field("createUser")
async def resolve_create_user(_, info, name: str, email: str):
    user = {"name": name, "email": email}
    result = await collection.insert_one(user)
    user["id"] = str(result.inserted_id)
    return user

# Criar esquema GraphQL
schema_str = """
type User {
  id: ID!
  name: String!
  email: String!
}

type Query {
  getUsers: [User]!
}

type Mutation {
  createUser(name: String!, email: String!): User
}
"""
schema = make_executable_schema(schema_str, query, mutation)

# Criar a API FastAPI
app = FastAPI()
app.add_route("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

### 📌 Passo 5: Rodar o Servidor
```sh
python server.py
```
Agora, a API GraphQL está disponível em `http://localhost:8000/graphql`.

---

## ✅ 2. Configuração da Base de Dados MongoDB

### 📌 Passo 1: Instalar MongoDB
- **Linux**:
  ```sh
  sudo apt update
  sudo apt install -y mongodb
  ```
- **Windows**:
  - Baixar e instalar [MongoDB Community Server](https://www.mongodb.com/try/download/community)

### 📌 Passo 2: Rodar o MongoDB
```sh
mongod --dbpath ./data/db
```

### 📌 Passo 3: Inserir Dados de Teste
```sh
mongosh  # Abrir o shell do MongoDB
use mydatabase
db.users.insertMany([
    { name: "Alice", email: "alice@example.com" },
    { name: "Bob", email: "bob@example.com" }
])
```

---

## ✅ 3. Criar o Frontend
Exemplo usando **React**:

### 📌 Passo 1: Criar um projeto React
```sh
npx create-react-app frontend
cd frontend
npm install graphql-request
```

### 📌 Passo 2: Criar um Componente para Buscar Dados
Edita **`src/App.js`**:

```jsx
import { useEffect, useState } from "react";
import { request } from "graphql-request";

const API_URL = "http://localhost:8000/graphql";

const GET_USERS = `
  query {
    getUsers {
      id
      name
      email
    }
  }
`;

function App() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    request(API_URL, GET_USERS)
      .then((data) => setUsers(data.getUsers))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div>
      <h1>Lista de Usuários</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name} - {user.email}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```

### 📌 Passo 3: Rodar o Frontend
```sh
npm start
```
Agora podes aceder ao frontend em `http://localhost:3000`.

---

## 🔍 4. Testando a API com GraphQL Playground
No `http://localhost:8000/graphql`, podes testar:

```graphql
query {
  getUsers {
    id
    name
    email
  }
}
```

Para criar um usuário:
```graphql
mutation {
  createUser(name: "Carlos", email: "carlos@example.com") {
    id
    name
    email
  }
}
```

---

## 🔗 Conclusão
Agora tens um site funcional onde:
✅ O **backend** está em **Python + FastAPI + Ariadne**  
✅ A **base de dados** é **MongoDB**  
✅ O **frontend** pode ser **React, Vue, Angular ou HTML+JS**  

Se precisares de mais alguma coisa, avisa! 🚀

