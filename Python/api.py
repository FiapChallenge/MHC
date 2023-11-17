from datetime import datetime
from re import template
from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from cx_Oracle import makedsn
from sqlalchemy import inspect
from flasgger import Swagger, swag_from
from sqlalchemy.orm import validates

SELF_SIGN_CERT = False

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "API Classificação de Risco",
    "uiversion": 3,
    "specs_route": "/api/docs/",
    "description": "API para classificação de risco de pacientes",
}

template = {
    "swagger": "2.0",
    "info": {
        "title": "API Classificação de Risco",
        "description": "API para classificação de risco de pacientes",
        "contact": {
            "responsibleOrganization": "Manchester Healthcare",
            "responsibleDeveloper": "Augusto Barcelos Barros",
            "email": "augustobb@live.com",
        },
        "version": "0.0.1",
    },
    "schemes": ["http", "https"],
    "operationId": "getmyData",
    "definitions": {
        "Auditor": {
            "type": "object",
            "properties": {
                "id_auditor": {"type": "integer"},
                "nome": {"type": "string"},
                "cpf": {"type": "string"},
                "crm": {"type": "string"},
                "coren": {"type": "string"},
                "especialidade": {"type": "string"},
            },
        },
        "Classificacao": {
            "type": "object",
            "properties": {
                "id_classificacao": {"type": "integer"},
                "data_hora_classificacao": {"type": "string"},
                "gravidade_id_gravidade": {"type": "integer"},
                "sinal_id_sinal": {"type": "integer"},
                "paciente_id_paciente": {"type": "integer"},
                "auditor_id_auditor": {"type": "integer"},
            },
        },
        "Gravidade": {
            "type": "object",
            "properties": {
                "id_gravidade": {"type": "integer"},
                "nome_gravidade": {"type": "string"},
                "nome_cor": {"type": "string"},
                "hexadecimal_cor": {"type": "string"},
            },
        },
        "Paciente": {
            "type": "object",
            "properties": {
                "id_paciente": {"type": "integer"},
                "nome": {"type": "string"},
                "cpf": {"type": "string"},
                "rg": {"type": "string"},
                "data_hora_entrada": {"type": "string"},
                "data_hora_saida": {"type": "string"},
                "sexo": {"type": "string"},
                "idade": {"type": "integer"},
                "altura": {"type": "integer"},
                "peso": {"type": "integer"},
            },
        },
        "Sinal": {
            "type": "object",
            "properties": {
                "id_sinal": {"type": "integer"},
                "nome": {"type": "string"},
                "descricao": {"type": "string"},
            },
        },
    },
}

swagger = Swagger(app, template=template)

api = Api(app)

db_user = "rm98078"
db_pw = "261202"
db_host = "oracle.fiap.com.br"
db_service = "orcl"

oracle_connection_string = "oracle+cx_oracle://{username}:{password}@" + makedsn(
    "{hostname}", "{port}", service_name="{service_name}"
)

app.config["SQLALCHEMY_DATABASE_URI"] = oracle_connection_string.format(
    username=db_user,
    password=db_pw,
    hostname=db_host.split(":")[0],
    port="1521",
    service_name=db_service,
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
if SELF_SIGN_CERT:
    talisman = Talisman(app, content_security_policy=None, force_https=True)


def verify_json_keys(json, model):
    inspector = inspect(model)
    if inspector:
        columns = [column.key for column in inspector.columns]
        print(columns)
        if not all(key in columns for key in json.keys()):
            return False
    return True


@app.route("/")
def home():
    return """<html>
    <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400&display=swap">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                margin-top: 20px;
            }
            p {
                font-size: 24px;
            }
            h1 {
                font-size: 34px;
            }
        </style>
    </head>
    <body>
        <h1>API Classificação de Risco</h1>
        <p>Documentação: <a href="/api/docs/">/api/docs/</a></h3>
        <p>Repositório: <a target="_blank" href="https://github.com/FiapChallenge/MHC">github.com/FiapChallenge/MHC</a></h3>
    </body>
    </html>
    """


class Auditor(db.Model):
    __tablename__ = "AUDITOR"
    id_auditor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    crm = db.Column(db.String(20))
    coren = db.Column(db.String(20))
    especialidade = db.Column(db.String(50))

    def __init__(self, id_auditor, nome, cpf, crm, coren, especialidade):
        self.id_auditor = id_auditor
        self.nome = nome
        self.cpf = cpf
        self.crm = crm
        self.coren = coren
        self.especialidade = especialidade

    def __repr__(self):
        return f"<Auditor {self.nome}>"

    @validates("cpf")
    def validate_cpf(self, key, cpf):
        if len(cpf) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        return cpf

    @validates("crm")
    def validate_crm(self, key, crm):
        if len(crm) > 20:
            raise ValueError("CRM deve ter no máximo 20 dígitos")
        return crm

    @validates("coren")
    def validate_coren(self, key, coren):
        if len(coren) > 20:
            raise ValueError("COREN deve ter no máximo 20 dígitos")
        return coren

    @validates("especialidade")
    def validate_especialidade(self, key, especialidade):
        if len(especialidade) > 50:
            raise ValueError("Especialidade deve ter no máximo 50 dígitos")
        return especialidade

    def json(self):
        return {
            "id_auditor": self.id_auditor,
            "nome": self.nome,
            "cpf": self.cpf,
            "crm": self.crm,
            "coren": self.coren,
            "especialidade": self.especialidade,
        }


class Classificacao(db.Model):
    __tablename__ = "CLASSIFICACAO"
    id_classificacao = db.Column(db.Integer, primary_key=True)
    data_hora_classificacao = db.Column(db.DateTime, nullable=False)
    gravidade_id_gravidade = db.Column(db.Integer, nullable=False)
    sinal_id_sinal = db.Column(db.Integer, nullable=False)
    paciente_id_paciente = db.Column(db.Integer, nullable=False)
    auditor_id_auditor = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        id_classificacao,
        data_hora_classificacao,
        gravidade_id_gravidade,
        sinal_id_sinal,
        paciente_id_paciente,
        auditor_id_auditor,
    ):
        self.id_classificacao = id_classificacao
        self.data_hora_classificacao = data_hora_classificacao
        self.gravidade_id_gravidade = gravidade_id_gravidade
        self.sinal_id_sinal = sinal_id_sinal
        self.paciente_id_paciente = paciente_id_paciente
        self.auditor_id_auditor = auditor_id_auditor

    def __repr__(self):
        return f"<Classificacao {self.id_classificacao}>"

    def json(self):
        return {
            "id_classificacao": self.id_classificacao,
            "data_hora_classificacao": self.data_hora_classificacao.isoformat().replace(
                "T", " "
            )
            if self.data_hora_classificacao
            else None,
            "gravidade_id_gravidade": self.gravidade_id_gravidade,
            "sinal_id_sinal": self.sinal_id_sinal,
            "paciente_id_paciente": self.paciente_id_paciente,
            "auditor_id_auditor": self.auditor_id_auditor,
        }


class Gravidade(db.Model):
    __tablename__ = "GRAVIDADE"
    id_gravidade = db.Column(db.Integer, primary_key=True)
    nome_gravidade = db.Column(db.String(20), nullable=False)
    nome_cor = db.Column(db.String(20), nullable=False)
    hexadecimal_cor = db.Column(db.String(6))

    def __init__(self, id_gravidade, nome_gravidade, nome_cor, hexadecimal_cor=None):
        self.id_gravidade = id_gravidade
        self.nome_gravidade = nome_gravidade
        self.nome_cor = nome_cor
        self.hexadecimal_cor = hexadecimal_cor

    def __repr__(self):
        return f"<Gravidade {self.nome_gravidade}>"

    def json(self):
        return {
            "id_gravidade": self.id_gravidade,
            "nome_gravidade": self.nome_gravidade,
            "nome_cor": self.nome_cor,
            "hexadecimal_cor": self.hexadecimal_cor,
        }


class Paciente(db.Model):
    __tablename__ = "PACIENTE"
    id_paciente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    cpf = db.Column(db.String(11))
    rg = db.Column(db.String(9))
    data_hora_entrada = db.Column(db.DateTime, nullable=False)
    data_hora_saida = db.Column(db.DateTime)
    sexo = db.Column(db.String(1))
    idade = db.Column(db.Integer)
    altura = db.Column(db.Integer)
    peso = db.Column(db.Integer)

    def __init__(
        self,
        id_paciente,
        nome,
        cpf,
        rg,
        data_hora_entrada,
        data_hora_saida,
        sexo,
        idade,
        altura,
        peso,
    ):
        self.id_paciente = id_paciente
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.data_hora_entrada = data_hora_entrada
        self.data_hora_saida = data_hora_saida
        self.sexo = sexo
        self.idade = idade
        self.altura = altura
        self.peso = peso

    def __repr__(self):
        return f"<Paciente {self.nome}>"

    def json(self):
        return {
            "id_paciente": self.id_paciente,
            "nome": self.nome,
            "cpf": self.cpf,
            "rg": self.rg,
            "data_hora_entrada": self.data_hora_entrada.isoformat().replace("T", " ")
            if self.data_hora_entrada
            else None,
            "data_hora_saida": self.data_hora_saida.isoformat().replace("T", " ")
            if self.data_hora_saida
            else None,
            "sexo": self.sexo,
            "idade": self.idade,
            "altura": self.altura,
            "peso": self.peso,
        }


class Sinal(db.Model):
    __tablename__ = "SINAL"
    id_sinal = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    descricao = db.Column(db.String(700))

    def __init__(self, id_sinal, nome, descricao=None):
        self.id_sinal = id_sinal
        self.nome = nome
        self.descricao = descricao

    def __repr__(self):
        return f"<Sinal {self.nome}>"

    def json(self):
        return {
            "id_sinal": self.id_sinal,
            "nome": self.nome,
            "descricao": self.descricao,
        }


class AuditorResource(Resource):
    @swag_from(
        {
            "tags": ["Auditor"],
            "description": "Get a list of all auditors.",
            "responses": {
                "200": {
                    "description": "A list of auditors.",
                    "schema": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Auditor"},
                    },
                    "examples": {
                        "application/json": [
                            {
                                "id_auditor": 1,
                                "nome": "John Doe",
                                "cpf": "12345678901",
                                "crm": "ABC123",
                                "coren": "XYZ456",
                                "especialidade": "Cardiology",
                            },
                            {
                                "id_auditor": 2,
                                "nome": "Jane Doe",
                                "cpf": "10987654321",
                                "crm": "DEF456",
                                "coren": "ZYX654",
                                "especialidade": "Pediatrics",
                            },
                        ]
                    },
                }
            },
        }
    )
    def get(self):
        auditores = Auditor.query.all()
        return [auditor.json() for auditor in auditores]

    @swag_from(
        {
            "tags": ["Auditor"],
            "description": "Create a new auditor.",
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {"$ref": "#/definitions/Auditor"},
                    "examples": {
                        "application/json": {
                            "id_auditor": 1,
                            "nome": "John Doe",
                            "cpf": "12345678901",
                            "crm": "ABC123",
                            "coren": "XYZ456",
                            "especialidade": "Cardiology",
                        }
                    },
                }
            ],
            "responses": {
                "201": {
                    "description": "Auditor created successfully.",
                    "schema": {"$ref": "#/definitions/Auditor"},
                    "examples": {
                        "application/json": {
                            "id_auditor": 1,
                            "nome": "John Doe",
                            "cpf": "12345678901",
                            "crm": "ABC123",
                            "coren": "XYZ456",
                            "especialidade": "Cardiology",
                        }
                    },
                },
                "400": {"description": "Invalid JSON keys."},
                "500": {"description": "Erro ao salvar auditor."},
            },
        }
    )
    def post(self):
        data = request.get_json()
        if not verify_json_keys(data, Auditor):
            return {"message": "Invalid JSON keys"}, 400
        auditor = Auditor(**data)
        try:
            db.session.add(auditor)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar auditor: {e}"}, 500
        return auditor.json(), 201


class AuditorIdResource(Resource):
    @swag_from(
        {
            "tags": ["Auditor"],
            "description": "Get a single auditor by ID.",
            "parameters": [
                {
                    "name": "id_modelo",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                    "description": "The ID of the auditor to retrieve.",
                }
            ],
            "responses": {
                "200": {
                    "description": "Auditor found.",
                    "schema": {"$ref": "#/definitions/Auditor"},
                    "examples": {
                        "application/json": {
                            "id_auditor": 1,
                            "nome": "John Doe",
                            "cpf": "12345678901",
                            "crm": "ABC123",
                            "coren": "XYZ456",
                            "especialidade": "Cardiology",
                        }
                    },
                },
                "404": {"description": "Auditor not found."},
            },
        }
    )
    def get(self, id_modelo):
        if not id_modelo.isdigit():
            return {"message": "Invalid ID"}, 400

        auditor = db.session.get(Auditor, id_modelo)
        if auditor:
            return auditor.json()
        return {"message": "Auditor não encontrado."}, 404

    @swag_from(
        {
            "tags": ["Auditor"],
            "description": "Update a single auditor by ID.",
            "parameters": [
                {
                    "name": "id_modelo",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                    "description": "The ID of the auditor to update.",
                },
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {"$ref": "#/definitions/Auditor"},
                    "examples": {
                        "application/json": {
                            "id_auditor": 1,
                            "nome": "John Doe",
                            "cpf": "12345678901",
                            "crm": "ABC123",
                            "coren": "XYZ456",
                            "especialidade": "Cardiology",
                        }
                    },
                },
            ],
            "responses": {
                "200": {
                    "description": "Auditor updated successfully.",
                    "schema": {"$ref": "#/definitions/Auditor"},
                    "examples": {
                        "application/json": {
                            "id_auditor": 1,
                            "nome": "John Doe",
                            "cpf": "12345678901",
                            "crm": "ABC123",
                            "coren": "XYZ456",
                            "especialidade": "Cardiology",
                        }
                    },
                },
                "400": {"description": "Invalid JSON keys."},
                "404": {"description": "Auditor not found."},
                "500": {"description": "Erro ao salvar auditor."},
            },
        }
    )
    def put(self, id_modelo):
        data = request.get_json()
        auditor = db.session.get(Auditor, id_modelo)
        if not auditor:
            return {"message": "Auditor não encontrado."}, 404
        auditor.nome = data["nome"]
        auditor.cpf = data["cpf"]
        auditor.crm = data["crm"]
        auditor.coren = data["coren"]
        auditor.especialidade = data["especialidade"]
        try:
            db.session.add(auditor)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar auditor: {e}"}, 500
        return auditor.json(), 200

    @swag_from(
        {
            "tags": ["Auditor"],
            "description": "Delete a single auditor by ID.",
            "parameters": [
                {
                    "name": "id_modelo",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                    "description": "The ID of the auditor to delete.",
                }
            ],
            "responses": {
                "200": {"description": "Auditor deleted successfully."},
                "404": {"description": "Auditor not found."},
                "500": {"description": "Erro ao deletar auditor."},
            },
        }
    )
    def delete(self, id_modelo):
        auditor = db.session.get(Auditor, id_modelo)
        if not auditor:
            return {"message": "Auditor não encontrado."}, 404
        try:
            db.session.delete(auditor)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao deletar auditor: {e}"}, 500
        return {"message": "Auditor deletado com sucesso."}, 200


class ClassificacaoResource(Resource):
    def get(self):
        classificacoes = Classificacao.query.all()
        return [classificacao.json() for classificacao in classificacoes]

    def post(self):
        data = request.get_json()
        if not verify_json_keys(data, Classificacao):
            return {"message": "Invalid JSON keys"}, 400
        classificacao = Classificacao(**data)
        try:
            db.session.add(classificacao)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar classificacao: {e}"}, 500
        return classificacao.json(), 201


class ClassificacaoIdResource(Resource):
    def get(self, id_modelo):
        if not id_modelo.isdigit():
            return {"message": "Invalid ID"}, 400

        classificacao = db.session.get(Classificacao, id_modelo)
        if classificacao:
            return classificacao.json()
        return {"message": "Classificacao não encontrada."}, 404

    def put(self, id_modelo):
        data = request.get_json()
        classificacao = db.session.get(Classificacao, id_modelo)
        if not classificacao:
            return {"message": "Classificacao não encontrada."}, 404
        classificacao.data_hora_classificacao = data["data_hora_classificacao"]
        classificacao.gravidade_id_gravidade = data["gravidade_id_gravidade"]
        classificacao.sinal_id_sinal = data["sinal_id_sinal"]
        classificacao.paciente_id_paciente = data["paciente_id_paciente"]
        classificacao.auditor_id_auditor = data["auditor_id_auditor"]
        try:
            db.session.add(classificacao)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar classificacao: {e}"}, 500
        return classificacao.json(), 200

    def delete(self, id_modelo):
        classificacao = db.session.get(Classificacao, id_modelo)
        if not classificacao:
            return {"message": "Classificacao não encontrada."}, 404
        try:
            db.session.delete(classificacao)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao deletar classificacao: {e}"}, 500
        return {"message": "Classificacao deletada com sucesso."}, 200


class GravidadeResource(Resource):
    def get(self):
        gravidades = Gravidade.query.all()
        return [gravidade.json() for gravidade in gravidades]

    def post(self):
        data = request.get_json()
        if not verify_json_keys(data, Gravidade):
            return {"message": "Invalid JSON keys"}, 400
        gravidade = Gravidade(**data)
        try:
            db.session.add(gravidade)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar gravidade: {e}"}, 500
        return gravidade.json(), 201


class GravidadeIdResource(Resource):
    def get(self, id_modelo):
        if not id_modelo.isdigit():
            return {"message": "Invalid ID"}, 400

        gravidade = db.session.get(Gravidade, id_modelo)
        if gravidade:
            return gravidade.json()
        return {"message": "Gravidade não encontrada."}, 404

    def put(self, id_modelo):
        data = request.get_json()
        gravidade = db.session.get(Gravidade, id_modelo)
        if not gravidade:
            return {"message": "Gravidade não encontrada."}, 404
        gravidade.nome_gravidade = data["nome_gravidade"]
        gravidade.nome_cor = data["nome_cor"]
        gravidade.hexadecimal_cor = data["hexadecimal_cor"]
        try:
            db.session.add(gravidade)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar gravidade: {e}"}, 500
        return gravidade.json(), 200

    def delete(self, id_modelo):
        gravidade = db.session.get(Gravidade, id_modelo)
        if not gravidade:
            return {"message": "Gravidade não encontrada."}, 404
        try:
            db.session.delete(gravidade)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao deletar gravidade: {e}"}, 500
        return {"message": "Gravidade deletada com sucesso."}, 200


class PacienteResource(Resource):
    def get(self):
        pacientes = Paciente.query.all()
        return [paciente.json() for paciente in pacientes]

    def post(self):
        data = request.get_json()
        if not verify_json_keys(data, Paciente):
            return {"message": "Invalid JSON keys"}, 400
        data["data_hora_entrada"] = datetime.strptime(
            data["data_hora_entrada"], "%Y-%m-%d %H:%M:%S"
        )
        data["data_hora_saida"] = (
            datetime.strptime(data["data_hora_saida"], "%Y-%m-%d %H:%M:%S")
            if data.get("data_hora_saida")
            else None
        )
        paciente = Paciente(**data)
        try:
            db.session.add(paciente)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar paciente: {e}"}, 500
        return paciente.json(), 201


class PacienteIdResource(Resource):
    def get(self, id_modelo):
        if not id_modelo.isdigit():
            return {"message": "Invalid ID"}, 400

        paciente = db.session.get(Paciente, id_modelo)
        if paciente:
            return paciente.json()
        return {"message": "Paciente não encontrado."}, 404

    def put(self, id_modelo):
        data = request.get_json()
        paciente = db.session.get(Paciente, id_modelo)
        if not paciente:
            return {"message": "Paciente não encontrado."}, 404
        paciente.nome = data["nome"]
        paciente.cpf = data["cpf"]
        paciente.rg = data["rg"]
        paciente.data_hora_entrada = datetime.strptime(
            data["data_hora_entrada"], "%Y-%m-%d %H:%M:%S"
        )
        paciente.data_hora_saida = (
            datetime.strptime(data["data_hora_saida"], "%Y-%m-%d %H:%M:%S")
            if data.get("data_hora_saida")
            else None
        )
        paciente.sexo = data["sexo"]
        paciente.idade = data["idade"]
        paciente.altura = data["altura"]
        paciente.peso = data["peso"]
        try:
            db.session.add(paciente)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar paciente: {e}"}, 500
        return paciente.json(), 200

    def delete(self, id_modelo):
        paciente = db.session.get(Paciente, id_modelo)
        if not paciente:
            return {"message": "Paciente não encontrado."}, 404
        try:
            db.session.delete(paciente)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao deletar paciente: {e}"}, 500
        return {"message": "Paciente deletado com sucesso."}, 200


class SinalResource(Resource):
    def get(self):
        sinais = Sinal.query.all()
        return [sinal.json() for sinal in sinais]

    def post(self):
        data = request.get_json()
        if not verify_json_keys(data, Sinal):
            return {"message": "Invalid JSON keys"}, 400
        sinal = Sinal(**data)
        try:
            db.session.add(sinal)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar sinal: {e}"}, 500
        return sinal.json(), 201


class SinalIdResource(Resource):
    def get(self, id_modelo):
        if not id_modelo.isdigit():
            return {"message": "Invalid ID"}, 400

        sinal = db.session.get(Sinal, id_modelo)
        if sinal:
            return sinal.json()
        return {"message": "Sinal não encontrado."}, 404

    def put(self, id_modelo):
        data = request.get_json()
        sinal = db.session.get(Sinal, id_modelo)
        if not sinal:
            return {"message": "Sinal não encontrado."}, 404
        sinal.nome = data["nome"]
        sinal.descricao = data["descricao"]
        try:
            db.session.add(sinal)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar sinal: {e}"}, 500
        return sinal.json(), 200

    def delete(self, id_modelo):
        sinal = db.session.get(Sinal, id_modelo)
        if not sinal:
            return {"message": "Sinal não encontrado."}, 404
        try:
            db.session.delete(sinal)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao deletar sinal: {e}"}, 500
        return {"message": "Sinal deletado com sucesso."}, 200


api.add_resource(AuditorResource, "/auditor")
api.add_resource(AuditorIdResource, "/auditor/<string:id_modelo>")
api.add_resource(ClassificacaoResource, "/classificacao")
api.add_resource(ClassificacaoIdResource, "/classificacao/<string:id_modelo>")
api.add_resource(GravidadeResource, "/gravidade")
api.add_resource(GravidadeIdResource, "/gravidade/<string:id_modelo>")
api.add_resource(PacienteResource, "/paciente")
api.add_resource(PacienteIdResource, "/paciente/<string:id_modelo>")
api.add_resource(SinalResource, "/sinal")
api.add_resource(SinalIdResource, "/sinal/<string:id_modelo>")


if __name__ == "__main__":
    if SELF_SIGN_CERT:
        app.run(port=8080, debug=True, ssl_context=("cert.pem", "key.pem"))
    else:
        app.run(port=8080, debug=True)
