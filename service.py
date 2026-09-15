from dotenv import load_dotenv
import os
import json
from groq import Groq

load_dotenv()

# Nome do modelo oficial ativo atualmente na Groq
MODELO_ATUAL = "openai/gpt-oss-20b"

def obter_temperatura_atual(cidade):
    # Aqui continua sua lógica ou simulação de clima local
    return f"A temperatura atual em {cidade} é de 25°C com céu limpo."

def chat_with_tools(mensagem):
    try:
        chave_api = os.environ.get('CHAVE_KEY')
        if not chave_api:
            return "Erro: Chave API 'CHAVE_KEY' não configurada."
            
        client = Groq(api_key=chave_api)   
        
        # Histórico estruturado para manter o fluxo do Function Calling
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

        # 1. Primeira chamada: groq analisa o texto e decide se usa a função
        response = client.chat.completions.create(
            model=MODELO_ATUAL,  # <--- Usando o modelo ativo
            messages=mensagens_historico,
            tools=tools,
            tool_choice="auto"
        )
        
        resposta_mensagem = response.choices[0].message
        tool_calls = resposta_mensagem.tool_calls

        # Se o modelo identificou que precisa rodar a função de clima
        if tool_calls:
            mensagens_historico.append(resposta_mensagem)
            
            funcoes_disponiveis = {
                "obter_temperatura_atual": obter_temperatura_atual,
            }
            
            for tool_call in tool_calls:
                nome_funcao = tool_call.function.name
                argumentos_funcao = json.loads(tool_call.function.arguments)
                funcao_para_chamar = funcoes_disponiveis[nome_funcao]
                
                # Executa a função Python local
                resultado_da_ferramenta = funcao_para_chamar(cidade=argumentos_funcao.get("cidade"))
                
                # Adiciona o resultado no formato exigido pela API
                mensagens_historico.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": nome_funcao,
                    "content": resultado_da_ferramenta,
                })
            
            # 2. Segunda chamada: envia o resultado da função para o modelo gerar o texto final
            segunda_resposta = client.chat.completions.create(
                model=MODELO_ATUAL,  # <--- Usando o modelo ativo
                messages=mensagens_historico
            )
            return segunda_resposta.choices[0].message.content

        # Se não precisou usar ferramentas, devolve a resposta direta de texto
        return resposta_mensagem.content

    except Exception as e:
        print(f"ERRO BACK-END: {str(e)}")
        return f"Erro processando requisição: {str(e)}"
