import traceback
from flask import Blueprint, request, jsonify
from service import chat_with_tools

router = Blueprint('router', __name__)

@router.route("/assistant", methods=['POST'])
def minha_rota():
    try:
        body = request.get_json()
        if not body:
            return "Erro: Corpo da requisição vazio ou inválido", 400
            
        mensagem = body.get("mensagem")
        if not mensagem:
            return "Erro: Campo 'mensagem' não enviado", 400
            
        response = chat_with_tools(mensagem)
        return response, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
        # Se o Python quebrar por qualquer motivo (como chave inválida), 
        # ele vai capturar o erro real e mandar de volta para o JavaScript ver
        erro_detalhado = traceback.format_exc()
        print(erro_detalhado) # Aparecerá nos logs do Render
        return f"Erro interno no Flask:\n{erro_detalhado}", 500, {'Content-Type': 'text/plain; charset=utf-8'}
