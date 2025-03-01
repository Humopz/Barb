from fastapi import FastAPI, Body, APIRouter, HTTPException,Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from controllers.controller import Controller
from models.model import *
from database.connection import *
from database.database import *
from datetime import datetime, timezone
from urllib.parse import unquote
from controllers.tokens import Token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict

db_handle = DBConnectionHandler()
db_handle.connect_to_db()
db_connection = db_handle.get_db_connection()
controller = Controller(db_connection)

security = HTTPBearer()
app = FastAPI()
jwt_token = Token()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/cadastrar/")
async def add_item(cliente: Cliente):
    cliente.client_id = controller.qtd_ids_cliente()
    return controller.inserir_cliente(cliente)

@app.post("/cadastrar_funcionario")
async def add_func(funcionario: Funcionario = Body(...)):
    funcionario.funcionario_id = controller.qtd_ids_funcionario()
    return controller.inserir_funcionario(funcionario)

@app.post("/logar/")
async def add_item(cliente: ClienteLogin):
    return controller.check_Login(cliente)

@app.post('/marcarcorte')
async def addCorteNoBanco(corte: dict = Body(...)):
    await adicionar_corte(corte)
    return "CORTE MARCARDO E ENVIADO AO BANCO"

@app.get('/pegarcortes')
async def pegarCortes():
    dados = await pegar_cortes() 
    return dados

@app.delete('/deletarcorte/{id}')
async def deletecorte(id):
    await deletar_cortes(id)
    return "CORTE DELETADO"

@app.put('/atualizarcortes/{id}')
async def atualizarCortes(id , dados: dict = Body(...)):
    await atualizar_cortes(id, dados)
    return "CORTE ATUALIZADO"

@app.get("/verificar-token/")
def verificar_token(token: str):
    try:
        payload = jwt_token.verificar_token(token) 
        exp = payload.get('exp')
        if exp:
            exp_date = datetime.fromtimestamp(exp)
            if exp_date > datetime.now():
                print(exp_date)
                print(datetime.now())
                return {"status": "Token válido"}
            else:
                raise HTTPException(status_code=401, detail="Token expirado")
        else:
            raise HTTPException(status_code=401, detail="Token inválido")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao verificar token")
    
@app.post("/login/")
def login(email: str, senha: str, request: Request):
    email_decoded = unquote(email)
    resultado = controller.login(email_decoded, senha, request)
    if resultado:
        tipousuario = controller.tipoUsuario(email)
        print(resultado)
        return {"status": "Login bem-sucedido","token" : resultado, "tipo_usuario": tipousuario}
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

@app.get('/usuario')
async def get_usuario(id: int):
    return controller.listar_usuario_por_id(id)

@app.get('/listar_funcionarios/')
async def get_funcionarios():
    return controller.listar_funcionarios()

@app.delete('/deletar_funcionario/{funcid}')
async def delete_funcionarios(funcid: int):
    return controller.excluir_funcionario(funcid)

@app.post('/editar_cliente/')
async def editar_cliente(id: int, name: str , email: str, phone: str ):
    return controller.editar_cliente(id,name,email ,phone)
    
    