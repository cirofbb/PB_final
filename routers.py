from fastapi import APIRouter, HTTPException
from models import ChatModel, ChatResponseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv('.env')

router = APIRouter()

@router.post("/chat/", response_model=ChatResponseModel)
async def chat(body: ChatModel) -> ChatResponseModel:
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Verificação do corpo da requisição
        if not body.messages or not isinstance(body.messages, list):
            raise HTTPException(status_code=422, detail="O campo 'messages' é obrigatório e deve ser uma lista.")
        
        # Construindo o prompt com o histórico
        persona = """Você é um assistente amigável especialista em questões de reciclagem e tratamento de resíduos. 
        Mantenha consistência com suas respostas anteriores e forneça informações precisas sobre reciclagem."""
        
        # Construindo o prompt com todo o contexto
        conversation = "\n".join([f"{msg.role}: {msg.content}" for msg in body.messages])
        final_prompt = f"{persona}\n\nConversa anterior:\n{conversation}\nAssistant:"
        
        # Configurando os parâmetros de geração
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        response = model.generate_content(
            final_prompt,
            generation_config=generation_config
        )

        if not response or not response.text:
            raise HTTPException(
                status_code=500, 
                detail="Erro ao gerar a resposta. O modelo retornou uma resposta vazia."
            )
            
        return ChatResponseModel(response=response.text)

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro inesperado ao processar a solicitação: {str(e)}"
        )