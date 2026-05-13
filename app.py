from flask import Flask
from flask_cors import CORS # 1. Importe o CORS
from routes import router

app = Flask(__name__)
CORS(app) # 2. Isso libera o acesso para todas as origens (portas)

app.register_blueprint(router)

if __name__ == "__main__":
    app.run(port=5000, debug=True)