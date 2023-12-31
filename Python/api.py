from datetime import datetime
from re import template
from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from cx_Oracle import makedsn, init_oracle_client
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Sequence, inspect
from flasgger import Swagger
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


# Cant use this decorator because changes the signature of the function and i need the original signature to use in the main.py
# def validate_attributes(func):
#     def wrapper(self, *args, **kwargs):
#         for attr_name, value in kwargs.items():
#             validator_method = getattr(self.__class__, f"validate_{attr_name}", None)
#             if validator_method:
#                 kwargs[attr_name] = validator_method(value)
#         return func(self, *args, **kwargs)
#     return wrapper


def validate_attributes(self, **kwargs):
    for attr_name, value in kwargs.items():
        validator_method = getattr(self, f"validate_{attr_name}", None)
        if validator_method:
            setattr(self, attr_name, validator_method(value))


class Auditor(db.Model):
    __tablename__ = "AUDITOR"
    id_auditor = db.Column(db.Integer, Sequence("AUDITOR_ID_SEQ"), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11))
    crm = db.Column(db.String(20))
    coren = db.Column(db.String(20))
    especialidade = db.Column(db.String(50))

    def __init__(
        self, nome, email, senha, cpf=None, crm=None, coren=None, especialidade=None
    ):
        validate_attributes(
            self,
            nome=nome,
            email=email,
            senha=senha,
            cpf=cpf,
            crm=crm,
            coren=coren,
            especialidade=especialidade,
        )
        self.nome = nome
        self.email = email
        self.senha = senha
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

    @classmethod
    def validate_nome(cls, nome):
        if not nome:
            raise ValueError("Nome não pode ser vazio")
        if len(nome) > 50:
            raise ValueError("Nome deve ter no máximo 50 dígitos")
        return nome

    @classmethod
    def validate_email(cls, email):
        if not email:
            raise ValueError("Email não pode ser vazio")
        if len(email) > 50:
            raise ValueError("Email deve ter no máximo 50 dígitos")
        if db.session.query(Auditor).filter_by(email=email).first():
            raise ValueError("Email já cadastrado")
        return email

    @classmethod
    def validate_senha(cls, senha):
        if not senha:
            raise ValueError("Senha não pode ser vazio")
        if len(senha) > 50:
            raise ValueError("Senha deve ter no máximo 50 dígitos")
        return senha

    def update(self, Auditor):
        self.nome = Auditor.nome
        self.email = Auditor.email
        self.senha = Auditor.senha
        self.cpf = Auditor.cpf
        self.crm = Auditor.crm
        self.coren = Auditor.coren
        self.especialidade = Auditor.especialidade

    def json(self):
        return {
            "id_auditor": self.id_auditor,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
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
        validate_attributes(
            self,
            data_hora_classificacao=data_hora_classificacao,
            gravidade_id_gravidade=gravidade_id_gravidade,
            sinal_id_sinal=sinal_id_sinal,
            paciente_id_paciente=paciente_id_paciente,
            auditor_id_auditor=auditor_id_auditor,
        )
        data_hora_classificacao = datetime.strptime(
            data_hora_classificacao, "%Y-%m-%d %H:%M:%S"
        )
        self.data_hora_classificacao = data_hora_classificacao
        self.gravidade_id_gravidade = gravidade_id_gravidade
        self.sinal_id_sinal = sinal_id_sinal
        self.paciente_id_paciente = paciente_id_paciente
        self.auditor_id_auditor = auditor_id_auditor

    @classmethod
    def validate_data_hora_classificacao(cls, data_hora_classificacao):
        if not data_hora_classificacao:
            raise ValueError("Data e hora da classificação não pode ser vazio")
        try:
            datetime.strptime(data_hora_classificacao, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(
                "Data e hora da classificação deve estar no formato YYYY-MM-DD HH:MM:SS (ex: 2021-01-01 00:00:00)"
            )

        return data_hora_classificacao

    @classmethod
    def validate_gravidade_id_gravidade(cls, gravidade_id_gravidade):
        if not gravidade_id_gravidade:
            raise ValueError("Gravidade não pode ser vazio")
        return gravidade_id_gravidade

    @classmethod
    def validate_sinal_id_sinal(cls, sinal_id_sinal):
        if not sinal_id_sinal:
            raise ValueError("Sinal não pode ser vazio")
        return sinal_id_sinal

    @classmethod
    def validate_paciente_id_paciente(cls, paciente_id_paciente):
        if not paciente_id_paciente:
            raise ValueError("Paciente não pode ser vazio")
        return paciente_id_paciente

    @classmethod
    def validate_auditor_id_auditor(cls, auditor_id_auditor):
        if not auditor_id_auditor:
            raise ValueError("Auditor não pode ser vazio")
        return auditor_id_auditor

    def __repr__(self):
        return f"<Classificacao {self.id_classificacao}>"

    def update(self, Classificacao):
        self.data_hora_classificacao = Classificacao.data_hora_classificacao
        self.gravidade_id_gravidade = Classificacao.gravidade_id_gravidade
        self.sinal_id_sinal = Classificacao.sinal_id_sinal
        self.paciente_id_paciente = Classificacao.paciente_id_paciente
        self.auditor_id_auditor = Classificacao.auditor_id_auditor

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
        validate_attributes(
            self,
            nome_gravidade=nome_gravidade,
            nome_cor=nome_cor,
            hexadecimal_cor=hexadecimal_cor,
        )
        self.nome_gravidade = nome_gravidade
        self.nome_cor = nome_cor
        self.hexadecimal_cor = hexadecimal_cor

    @classmethod
    def validate_nome_gravidade(cls, nome_gravidade):
        if not nome_gravidade:
            raise ValueError("Nome da gravidade não pode ser vazio")
        if len(nome_gravidade) > 20:
            raise ValueError("Nome da gravidade deve ter no máximo 20 dígitos")
        return nome_gravidade

    @classmethod
    def validate_nome_cor(cls, nome_cor):
        if not nome_cor:
            raise ValueError("Nome da cor não pode ser vazio")
        if len(nome_cor) > 20:
            raise ValueError("Nome da cor deve ter no máximo 20 dígitos")
        return nome_cor

    @classmethod
    def validate_hexadecimal_cor(cls, hexadecimal_cor):
        if not hexadecimal_cor:
            return hexadecimal_cor
        if len(hexadecimal_cor) > 6:
            raise ValueError("Hexadecimal da cor deve ter no máximo 6 dígitos")
        return hexadecimal_cor

    def __repr__(self):
        return f"<Gravidade {self.nome_gravidade}>"

    def update(self, Gravidade):
        self.nome_gravidade = Gravidade.nome_gravidade
        self.nome_cor = Gravidade.nome_cor
        self.hexadecimal_cor = Gravidade.hexadecimal_cor

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
        validate_attributes(
            self,
            nome=nome,
            cpf=cpf,
            rg=rg,
            data_hora_entrada=data_hora_entrada,
            data_hora_saida=data_hora_saida,
            sexo=sexo,
            idade=idade,
            altura=altura,
            peso=peso,
        )
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        data_hora_entrada = datetime.strptime(data_hora_entrada, "%Y-%m-%d %H:%M:%S")
        data_hora_saida = (
            datetime.strptime(data_hora_saida, "%Y-%m-%d %H:%M:%S")
            if data_hora_saida
            else None
        )
        self.data_hora_entrada = data_hora_entrada
        self.data_hora_saida = data_hora_saida
        self.sexo = sexo
        self.idade = idade
        self.altura = altura
        self.peso = peso

    @classmethod
    def validate_nome(cls, nome):
        if not nome:
            raise ValueError("Nome não pode ser vazio")
        if len(nome) > 50:
            raise ValueError("Nome deve ter no máximo 50 dígitos")
        return nome

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
    def validate_rg(cls, rg):
        if not rg:
            return rg
        if not rg.isdigit():
            raise ValueError("RG deve conter apenas números")
        if len(rg) != 9:
            raise ValueError("RG deve ter 9 dígitos")
        return rg

    @classmethod
    def validate_data_hora_entrada(cls, data_hora_entrada):
        if not data_hora_entrada:
            raise ValueError("Data e hora de entrada não pode ser vazio")
        try:
            datetime.strptime(data_hora_entrada, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(
                "Data e hora de entrada deve estar no formato YYYY-MM-DD HH:MM:SS (ex: 2021-01-01 00:00:00)"
            )
        return data_hora_entrada

    @classmethod
    def validate_data_hora_saida(cls, data_hora_saida):
        if not data_hora_saida:
            return data_hora_saida
        try:
            datetime.strptime(data_hora_saida, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(
                "Data e hora de saída deve estar no formato YYYY-MM-DD HH:MM:SS (ex: 2021-01-01 00:00:00)"
            )
        return data_hora_saida

    @classmethod
    def validate_sexo(cls, sexo):
        if not sexo:
            return sexo
        if len(sexo) > 1:
            raise ValueError("Sexo deve ter no máximo 1 dígito")
        return sexo

    @classmethod
    def validate_idade(cls, idade):
        if not idade:
            return idade
        if not str(idade).isdigit():
            raise ValueError("Idade deve conter apenas números")
        if int(idade) > 150:
            raise ValueError("Idade deve ser menor que 150 anos")
        return idade

    @classmethod
    def validate_altura(cls, altura):
        if not altura:
            return altura
        if not str(altura).isdigit():
            raise ValueError("Altura deve conter apenas números")

        if int(altura) > 300:
            raise ValueError("Altura deve ser menor que 300 cm")
        return altura

    @classmethod
    def validate_peso(cls, peso):
        if not peso:
            return peso
        if not str(peso).isdigit():
            raise ValueError("Peso deve conter apenas números")
        if int(peso) > 500:
            raise ValueError("Peso deve ser menor que 500 kg")
        return peso

    def __repr__(self):
        return f"<Paciente {self.nome}>"

    def update(self, Paciente):
        self.nome = Paciente.nome
        self.cpf = Paciente.cpf
        self.rg = Paciente.rg
        self.data_hora_entrada = Paciente.data_hora_entrada
        self.data_hora_saida = Paciente.data_hora_saida
        self.sexo = Paciente.sexo
        self.idade = Paciente.idade
        self.altura = Paciente.altura
        self.peso = Paciente.peso

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

    def __init__(self, nome, descricao=None):
        validate_attributes(self, nome=nome, descricao=descricao)
        self.nome = nome
        self.descricao = descricao

    @classmethod
    def validate_nome(cls, nome):
        if not nome:
            raise ValueError("Nome não pode ser vazio")
        if len(nome) > 60:
            raise ValueError("Nome deve ter no máximo 60 dígitos")
        return nome

    @classmethod
    def validate_descricao(cls, descricao):
        if not descricao:
            return descricao
        if len(descricao) > 700:
            raise ValueError("Descrição deve ter no máximo 700 dígitos")
        return descricao

    def __repr__(self):
        return f"<Sinal {self.nome}>"

    def update(self, Sinal):
        self.nome = Sinal.nome
        self.descricao = Sinal.descricao

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
        if not str(id_modelo).isdigit():
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
        except IntegrityError as e:
            return {
                "message": f"Erro ao deletar auditor pois existem classificações relacionadas: {e}"
            }, 400
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
        if not str(id_modelo).isdigit():
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
        if not str(id_modelo).isdigit():
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
        except IntegrityError as e:
            return {
                "message": f"Erro ao deletar gravidade pois existem classificações relacionadas: {e}"
            }, 400
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
        if not str(id_modelo).isdigit():
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
        except IntegrityError as e:
            return {
                "message": f"Erro ao deletar paciente pois existem classificações relacionadas: {e}"
            }, 400

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
        if not str(id_modelo).isdigit():
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
        except IntegrityError as e:
            return {
                "message": f"Erro ao deletar sinal pois existem classificações relacionadas: {e}"
            }, 400

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
