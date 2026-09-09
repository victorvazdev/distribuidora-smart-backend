from flask_openapi3 import OpenAPI, Info
from flask import redirect
from flask_cors import CORS

from routes.product_routes import product_bp

info = Info(title='Distribuidora Smart - Backend', version='1.0.0')

app = OpenAPI(__name__, info=info)
CORS(app)

app.register_api(product_bp)


@app.get('/')
def home():
    '''Redireciona para a documentação interativa da API.
    
    Ao acessar a rota raiz da aplicação, o usuário é automaticamente 
    encaminhado para a interface gráfica do Swagger gerada pelo OpenAPI3.
    '''
    return redirect('/openapi/swagger')
