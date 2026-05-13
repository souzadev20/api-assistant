# Objetivo: Função que solicita ao groq a temperatura atual de uma cidade, pelo nome da cidade
from dotenv import load_dotenv
import os
from groq import Groq
 # lê o .env automaticamente
load_dotenv()


def chat_whit_tools(mensagem):

    # Prompt para a grok utilizar a lista para identificar de que forma a mensagem deve ser respondida
    prompt = '''
        Você é um assistente útil que responde perguntas sobre três temas: temperatura/clima, matemática e calendário.

        Regras:
        - Se a mensagem mencionar uma cidade ou lugar → responda com a temperatura atual estimada e condição do clima desse lugar de acordo com dia, evite dizer que está fazendo sol ou chovendo.
        - Se envolver cálculo ou matemática → responda apenas com o resultado.
        - Se envolver datas ou calendário → responda de forma direta.
        - Se não for nenhum desses temas → responda apenas: "Sou um assistente treinado que responde apenas sobre os seguintes temas: Tempo/Clima, Matemática e Calendário"

        Seja direto. Não explique seu raciocínio. Responda apenas a informação solicitada.
'''

    client = Groq(api_key = os.environ.get('CHAVE_KEY'))   
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user", 
            "content": mensagem
        }
    ]
    )

    return response.choices[0].message.content










