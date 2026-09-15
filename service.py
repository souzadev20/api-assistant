from dotenv import load_dotenv
import os
import json
from groq import Groq

load_dotenv()

def obter_temperatura_atual(cidade):
    # Simulação de retorno da API de clima
    return f"A temperatura atual em {cidade} é de 25°C com céu limpo."

def chat_with_tools(mensagem):
    try:
        # Garanta que a chave API está sendo lida corretamente
        chave_api = os.environ.get('CHAVE_KEY')
        if not chave_api:
            return {"erro": "Chave API 'CHAVE_KEY' não encontrada no ambiente."}, 500
            
        client = Groq(api_key=chave_api)   
        
        # Histórico de mensagens
        mensagens_historico = [{"role": "user", "content": mensagem}]
        
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "obter_temperatura_atual",
                    "description": "Busca a temperatura atual de uma cidade pelo nome.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "cidade": {"type": "string", "description": "Nome da cidade"}
                        },
                        "required": ["cidade"],
                    },
                },
            }
        ]

        # Primeira chamada ao Groq
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=mensagens_historico,
            tools=tools,
            tool_choice="auto"
        )
        
        # CORREÇÃO AQUI: Adicionado o índice [0] que faltava
        resposta_mensagem = response.choices[0].message
        tool_calls = resposta_mensagem.tool_calls

        # Se o modelo quis chamar a ferramenta (function calling)
        if tool_calls:
            # 1. Adiciona a resposta de intenção do modelo ao histórico
            mensagens_historico.append(resposta_mensagem)
            
            funcoes_disponiveis = {
                "obter_temperatura_atual": obter_temperatura_atual,
            }
            
            for tool_call in tool_calls:
                nome_funcao = tool_call.function.name
                argumentos_funcao = json.loads(tool_call.function.arguments)
                funcao_para_chamar = funcoes_disponiveis[nome_funcao]
                
                # Executa a função local
                resultado_da_ferramenta = funcao_para_chamar(cidade=argumentos_funcao.get("cidade"))
                
                # 2. Adiciona o resultado da função no histórico para o Groq ler
                mensagens_historico.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": nome_funcao,
                    "content": resultado_da_ferramenta,
                })
            
            # Segunda chamada ao Groq, agora com o resultado da temperatura
            segunda_resposta = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=mensagens_historico
            )
            return segunda_resposta.choices[0].message.content

        # Se não precisou de ferramenta, retorna o texto direto
        return resposta_mensagem.content

    except Exception as e:
        # Exibe o erro real no terminal do Python para você conseguir rastrear
        print(f"ERRO NO SERVIDOR: {str(e)}")
        raise e 
