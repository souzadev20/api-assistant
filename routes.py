from flask import Blueprint, request, jsonify
from service import chat_whit_tools

router = Blueprint('router', __name__)

@router.route("/assistant", methods = ['POST'])
def minha_rota():
    body = request.get_json()
    mensagem = body.get("mensagem")
    response = chat_whit_tools(mensagem)
    return jsonify(response), 200


