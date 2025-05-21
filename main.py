from fastapi import FastAPI
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from database import init_db
from resolvers import resolvers

app = FastAPI(title="Star Wars GraphQL API")

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, resolvers)
graphql_app = GraphQL(schema, debug=True)

app.mount("/graphql", graphql_app)

@app.on_event("startup")
async def startup_event():
    init_db()
    print("API siap! Akses GraphiQL di http://localhost:8000/graphql")

@app.get("/")
async def root():
    return {"message": "Selamat datang di Star Wars GraphQL API! Buka /graphql untuk mulai."}