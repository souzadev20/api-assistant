import traceback
from flask import Blueprint, request, jsonify
from service import chat_with_tools

router = Blueprint('router', __name__)

@router.route("/assistant", methods=['POST'])
def minha_rota():
    try:
        body = request.get_json()
        if not body:
            # Retorna um JSON de erro com status 400
            return jsonify({"erro": "Corpo da requisição vazio ou inválido"}), 400
            
        mensagem = body.get("mensagem")
        if not mensagem:
            # Retorna um JSON de erro com status 400
            return jsonify({"erro": "Campo 'mensagem' não enviado"}), 400
            
        response = chat_with_tools(mensagem)
        
        # CORREÇÃO AQUI: Devolve um JSON estruturado em vez de text/plain
        return jsonify({"resposta": response}), 200
        
    except Exception as e:
        erro_detalhado = traceback.format_exc()
        print(erro_detalhado) # Aparecerá nos logs do Render
        
        # Retorna o erro interno estruturado em JSON com status 500
        return jsonify({
            "erro": "Erro interno no Flask",
            "detalhes": erro_detalhado
        }), 500
