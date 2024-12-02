from fastapi import FastAPI
from routers import router as chat_router

app = FastAPI()

app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "Bem vindo a aplicação Streamlit sobre reciclagem"}