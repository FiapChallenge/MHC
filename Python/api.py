from datetime import datetime
from re import template
from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from cx_Oracle import makedsn, init_oracle_client
from sqlalchemy import Sequence, inspect
from flasgger import Swagger
from sqlalchemy.orm import validates
import pathlib
import yaml

SELF_SIGN_CERT = False


INSTANTCLIENTDIR = rf"{pathlib.Path().resolve()}\instantclient"
init_oracle_client(lib_dir=INSTANTCLIENTDIR)

app = Flask(__name__)
app.config["SWAGGER"] = {
    "specs_route": "/api/docs/",
}

# template external yaml file to json
with open("docs/swagger.yaml", "r", encoding="utf-8") as f:
    template = yaml.safe_load(f)
    if SELF_SIGN_CERT:
        template["schemes"] = ["https"]
    else:
        template["schemes"] = ["http"]

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
        columns = [
            column.key
            for column in inspector.columns
            if not column.key.startswith("id_")
        ]
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
    id_auditor = db.Column(db.Integer, Sequence("AUDITOR_ID_SEQ"), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    crm = db.Column(db.String(20))
    coren = db.Column(db.String(20))
    especialidade = db.Column(db.String(50))

    def __init__(self, nome, cpf, crm, coren, especialidade):
        self.validate_cpf(cpf)
        self.validate_crm(crm)
        self.validate_coren(coren)
        self.validate_especialidade(especialidade)

        self.nome = nome
        self.cpf = cpf
        self.crm = crm
        self.coren = coren
        self.especialidade = especialidade

    def __repr__(self):
        return f"<Auditor {self.nome}>"

    @classmethod
    def validate_cpf(cls, cpf):
        if not cpf:
            return cpf
        if not cpf.isdigit():
            raise ValueError("CPF deve conter apenas números")
        if len(cpf) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        return cpf

    @classmethod
    def validate_crm(cls, crm):
        if not crm:
            return crm
        if len(crm) > 20:
            raise ValueError("CRM deve ter no máximo 20 dígitos")
        return crm

    @classmethod
    def validate_coren(cls, coren):
        if not coren:
            return coren
        if len(coren) > 20:
            raise ValueError("COREN deve ter no máximo 20 dígitos")
        return coren

    @classmethod
    def validate_especialidade(cls, especialidade):
        if not especialidade:
            return especialidade
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
    id_classificacao = db.Column(
        db.Integer, Sequence("CLASSIFICACAO_ID_SEQ"), primary_key=True
    )
    data_hora_classificacao = db.Column(db.DateTime, nullable=False)
    gravidade_id_gravidade = db.Column(db.Integer, nullable=False)
    sinal_id_sinal = db.Column(db.Integer, nullable=False)
    paciente_id_paciente = db.Column(db.Integer, nullable=False)
    auditor_id_auditor = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        data_hora_classificacao,
        gravidade_id_gravidade,
        sinal_id_sinal,
        paciente_id_paciente,
        auditor_id_auditor,
    ):
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
    id_gravidade = db.Column(db.Integer, Sequence("GRAVIDADE_ID_SEQ"), primary_key=True)
    nome_gravidade = db.Column(db.String(20), nullable=False)
    nome_cor = db.Column(db.String(20), nullable=False)
    hexadecimal_cor = db.Column(db.String(6))

    def __init__(self, nome_gravidade, nome_cor, hexadecimal_cor=None):
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
    id_paciente = db.Column(db.Integer, Sequence("PACIENTE_ID_SEQ"), primary_key=True)
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
    id_sinal = db.Column(db.Integer, Sequence("SINAL_ID_SEQ"), primary_key=True)
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


app.app_context().push()
db.create_all()


class AuditorResource(Resource):
    def get(self):
        auditores = Auditor.query.all()
        return [auditor.json() for auditor in auditores]

    def post(self):
        data = request.get_json()
        if not verify_json_keys(data, Auditor):
            return {"message": "Invalid JSON keys"}, 400
        try:
            auditor = Auditor(**data)
        except ValueError as e:
            return {"message": f"Erro ao salvar auditor: {e}"}, 400
        try:
            db.session.add(auditor)
            db.session.commit()
        except Exception as e:
            return {"message": f"Erro ao salvar auditor: {e}"}, 500
        return auditor.json(), 201


class AuditorIdResource(Resource):
    def get(self, id_modelo):
        if not id_modelo.isdigit():
            return {"message": "Invalid ID"}, 400

        auditor = db.session.get(Auditor, id_modelo)
        if auditor:
            return auditor.json()
        return {"message": "Auditor não encontrado."}, 404

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
        data["data_hora_classificacao"] = datetime.strptime(
            data["data_hora_classificacao"], "%Y-%m-%d %H:%M:%S"
        )
        if not verify_json_keys(data, Classificacao):
            return {"message": "Invalid JSON keys"}, 400

        try:
            classificacao = Classificacao(**data)
        except ValueError as e:
            return {"message": f"Erro ao salvar classificacao: {e}"}, 400
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
        classificacao.data_hora_classificacao = datetime.strptime(
            data["data_hora_classificacao"], "%Y-%m-%d %H:%M:%S"
        )
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
        try:
            gravidade = Gravidade(**data)
        except ValueError as e:
            return {"message": f"Erro ao salvar gravidade: {e}"}, 400
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
        try:
            paciente = Paciente(**data)
        except ValueError as e:
            return {"message": f"Erro ao salvar paciente: {e}"}, 400
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
        try:
            sinal = Sinal(**data)
        except ValueError as e:
            return {"message": f"Erro ao salvar sinal: {e}"}, 400
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
