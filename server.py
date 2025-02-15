from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne.asgi import GraphQL
from ariadne import QueryType, MutationType, make_executable_schema

from models import collection, serialize_user

# Define the schema
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

# Define GraphQL schema
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

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Add GraphQL route
app.add_route("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)