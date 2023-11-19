from datetime import datetime
from api import db, Auditor, Paciente, Sinal, Gravidade, Classificacao


class AuditorCRUD:
    @staticmethod
    def type_of_sort(sort_by, direction):
        # direction = asc or desc
        match sort_by:
            case "ID":
                return (
                    Auditor.id_auditor.asc()
                    if direction == "asc"
                    else Auditor.id_auditor.desc()
                )
            case "NOME":
                return Auditor.nome.asc() if direction == "asc" else Auditor.nome.desc()

    @staticmethod
    def get_all_auditores(sort_by="ID", direction="asc"):
        auditores = Auditor.query.order_by(
            AuditorCRUD.type_of_sort(sort_by, direction)
        ).all()
        lista = []
        for auditor in auditores:
            lista.append(auditor.json())
        return lista

    @staticmethod
    def get_auditor_by_id(id):
        auditor = db.session.get(Auditor, id)
        if auditor:
            return auditor.json()
        return None

    @staticmethod
    def get_auditores_by_name(name, start_with=False, sort_by="ID", direction="asc"):
        if start_with:
            auditores = (
                # ILIKE = case insensitive
                Auditor.query.filter(Auditor.nome.ilike(f"{name}%"))
                .order_by(AuditorCRUD.type_of_sort(sort_by, direction))
                .all()
            )
        else:
            auditores = (
                Auditor.query.filter(Auditor.nome.ilike(f"%{name}%"))
                .order_by(AuditorCRUD.type_of_sort(sort_by, direction))
                .all()
            )
        lista = []
        for auditor in auditores:
            lista.append(auditor.json())
        return lista

    @staticmethod
    def create_auditor(nome, cpf, crm, coren, especialidade):
        auditor = Auditor(nome, cpf, crm, coren, especialidade)
        db.session.add(auditor)
        db.session.commit()
        return auditor.json()

    @staticmethod
    def update_auditor(id, nome, cpf, crm, coren, especialidade):
        auditor = db.session.get(Auditor, id)
        if auditor:
            auditor.nome = nome
            auditor.cpf = cpf
            auditor.crm = crm
            auditor.coren = coren
            auditor.especialidade = especialidade
            db.session.commit()
            return auditor.json()
        return None

    @staticmethod
    def delete_auditor(id):
        auditor = db.session.get(Auditor, id)
        if auditor:
            db.session.delete(auditor)
            db.session.commit()
            return auditor.json()
        return None


class PacienteCRUD:
    @staticmethod
    def type_of_sort(sort_by, direction):
        # direction = asc or desc
        match sort_by:
            case "ID":
                return (
                    Paciente.id_paciente.asc()
                    if direction == "asc"
                    else Paciente.id_paciente.desc()
                )
            case "NOME":
                return (
                    Paciente.nome.asc() if direction == "asc" else Paciente.nome.desc()
                )

    @staticmethod
    def get_all_pacientes(sort_by="ID", direction="asc"):
        pacientes = Paciente.query.order_by(
            PacienteCRUD.type_of_sort(sort_by, direction)
        ).all()
        lista = []
        for paciente in pacientes:
            lista.append(paciente.json())
        return lista

    @staticmethod
    def get_paciente_by_id(id):
        paciente = db.session.get(Paciente, id)
        if paciente:
            return paciente.json()
        return None

    @staticmethod
    def get_pacientes_by_name(name, start_with=False, sort_by="ID", direction="asc"):
        if start_with:
            pacientes = (
                # ILIKE = case insensitive
                Paciente.query.filter(Paciente.nome.ilike(f"{name}%"))
                .order_by(PacienteCRUD.type_of_sort(sort_by, direction))
                .all()
            )
        else:
            pacientes = (
                Paciente.query.filter(Paciente.nome.ilike(f"%{name}%"))
                .order_by(PacienteCRUD.type_of_sort(sort_by, direction))
                .all()
            )
        lista = []
        for paciente in pacientes:
            lista.append(paciente.json())
        return lista

    @staticmethod
    def create_paciente(
        nome, cpf, rg, data_hora_entrada, data_hora_saida, sexo, idade, altura, peso
    ):
        data_hora_entrada = datetime.strptime(data_hora_entrada, "%Y-%m-%d %H:%M:%S")
        data_hora_saida = (
            datetime.strptime(data_hora_saida, "%Y-%m-%d %H:%M:%S")
            if data_hora_saida
            else None
        )
        paciente = Paciente(
            nome, cpf, rg, data_hora_entrada, data_hora_saida, sexo, idade, altura, peso
        )
        db.session.add(paciente)
        db.session.commit()
        return paciente.json()

    @staticmethod
    def update_paciente(
        id, nome, cpf, rg, data_hora_entrada, data_hora_saida, sexo, idade, altura, peso
    ):
        paciente = db.session.get(Paciente, id)
        if paciente:
            paciente.nome = nome
            paciente.cpf = cpf
            paciente.rg = rg
            paciente.data_hora_entrada = data_hora_entrada
            paciente.data_hora_saida = data_hora_saida
            paciente.sexo = sexo
            paciente.idade = idade
            paciente.altura = altura
            paciente.peso = peso
            db.session.commit()
            return paciente.json()
        return None

    @staticmethod
    def delete_paciente(id):
        paciente = db.session.get(Paciente, id)
        if paciente:
            db.session.delete(paciente)
            db.session.commit()
            return paciente.json()
        return None


class SinalCRUD:
    @staticmethod
    def type_of_sort(sort_by, direction):
        # direction = asc or desc
        match sort_by:
            case "ID":
                return (
                    Sinal.id_sinal.asc()
                    if direction == "asc"
                    else Sinal.id_sinal.desc()
                )
            case "NOME":
                return Sinal.nome.asc() if direction == "asc" else Sinal.nome.desc()

    @staticmethod
    def get_all_sinais(sort_by="ID", direction="asc"):
        sinais = Sinal.query.order_by(SinalCRUD.type_of_sort(sort_by, direction)).all()
        lista = []
        for sinal in sinais:
            lista.append(sinal.json())
        return lista

    @staticmethod
    def get_sinal_by_id(id):
        sinal = db.session.get(Sinal, id)
        if sinal:
            return sinal.json()
        return None

    @staticmethod
    def get_sinais_by_name(name, start_with=False, sort_by="ID", direction="asc"):
        if start_with:
            sinais = (
                # ILIKE = case insensitive
                Sinal.query.filter(Sinal.nome.ilike(f"{name}%"))
                .order_by(SinalCRUD.type_of_sort(sort_by, direction))
                .all()
            )
        else:
            sinais = (
                Sinal.query.filter(Sinal.nome.ilike(f"%{name}%"))
                .order_by(SinalCRUD.type_of_sort(sort_by, direction))
                .all()
            )
        lista = []
        for sinal in sinais:
            lista.append(sinal.json())
        return lista

    @staticmethod
    def create_sinal(nome, descricao):
        sinal = Sinal(nome, descricao)
        db.session.add(sinal)
        db.session.commit()
        return sinal.json()

    @staticmethod
    def update_sinal(id, nome, descricao):
        sinal = db.session.get(Sinal, id)
        if sinal:
            sinal.nome = nome
            sinal.descricao = descricao
            db.session.commit()
            return sinal.json()
        return None

    @staticmethod
    def delete_sinal(id):
        sinal = db.session.get
        if sinal:
            db.session.delete(sinal)
            db.session.commit()
            return sinal.json()
        return None


class GravidadeCRUD:
    @staticmethod
    def type_of_sort(sort_by, direction):
        # direction = asc or desc
        match sort_by:
            case "ID":
                return (
                    Gravidade.id_gravidade.asc()
                    if direction == "asc"
                    else Gravidade.id_gravidade.desc()
                )
            case "NOME":
                return (
                    Gravidade.nome_gravidade.asc()
                    if direction == "asc"
                    else Gravidade.nome_gravidade.desc()
                )

    @staticmethod
    def get_all_gravidades(sort_by="ID", direction="asc"):
        gravidades = Gravidade.query.order_by(
            GravidadeCRUD.type_of_sort(sort_by, direction)
        ).all()
        lista = []
        for gravidade in gravidades:
            lista.append(gravidade.json())
        return lista

    @staticmethod
    def get_gravidade_by_id(id):
        gravidade = db.session.get(Gravidade, id)
        if gravidade:
            return gravidade.json()
        return None

    @staticmethod
    def get_gravidades_by_name(name, start_with=False, sort_by="ID", direction="asc"):
        if start_with:
            gravidades = (
                # ILIKE = case insensitive
                Gravidade.query.filter(Gravidade.nome_gravidade.ilike(f"{name}%"))
                .order_by(GravidadeCRUD.type_of_sort(sort_by, direction))
                .all()
            )
        else:
            gravidades = (
                Gravidade.query.filter(Gravidade.nome_gravidade.ilike(f"%{name}%"))
                .order_by(GravidadeCRUD.type_of_sort(sort_by, direction))
                .all()
            )
        lista = []
        for gravidade in gravidades:
            lista.append(gravidade.json())
        return lista

    @staticmethod
    def create_gravidade(nome_gravidade, nome_cor, hexadecimal_cor):
        gravidade = Gravidade(nome_gravidade, nome_cor, hexadecimal_cor)
        db.session.add(gravidade)
        db.session.commit()
        return gravidade.json()

    @staticmethod
    def update_gravidade(id, nome_gravidade, nome_cor, hexadecimal_cor):
        gravidade = db.session.get(Gravidade, id)
        if gravidade:
            gravidade.nome_gravidade = nome_gravidade
            gravidade.nome_cor = nome_cor
            gravidade.hexadecimal_cor = hexadecimal_cor
            db.session.commit()
            return gravidade.json()
        return None

    @staticmethod
    def delete_gravidade(id):
        gravidade = db.session.get(Gravidade, id)
        if gravidade:
            db.session.delete(gravidade)
            db.session.commit()
            return gravidade.json()
        return None


class ClassificacaoCRUD:
    @staticmethod
    def type_of_sort(sort_by, direction):
        # direction = asc or desc
        match sort_by:
            case "ID":
                return (
                    Classificacao.id_classificacao.asc()
                    if direction == "asc"
                    else Classificacao.id_classificacao.desc()
                )
            case "DATA":
                return (
                    Classificacao.data_hora_classificacao.asc()
                    if direction == "asc"
                    else Classificacao.data_hora_classificacao.desc()
                )

    @staticmethod
    def get_all_classificacoes(sort_by="ID", direction="asc"):
        classificacoes = Classificacao.query.order_by(
            ClassificacaoCRUD.type_of_sort(sort_by, direction)
        ).all()
        lista = []
        for classificacao in classificacoes:
            lista.append(classificacao.json())
        return lista

    @staticmethod
    def get_classificacao_by_id(id):
        classificacao = db.session.get(Classificacao, id)
        if classificacao:
            return classificacao.json()
        return None

    @staticmethod
    def get_classificacoes_by_name(
        name, start_with=False, sort_by="ID", direction="asc"
    ):
        if start_with:
            classificacoes = (
                # ILIKE = case insensitive
                Classificacao.query.filter(
                    Classificacao.data_hora_classificacao.ilike(f"{name}%")
                )
                .order_by(ClassificacaoCRUD.type_of_sort(sort_by, direction))
                .all()
            )
        else:
            classificacoes = (
                Classificacao.query.filter(
                    Classificacao.data_hora_classificacao.ilike(f"%{name}%")
                )
                .order_by(ClassificacaoCRUD.type_of_sort(sort_by, direction))
                .all()
            )
        lista = []
        for classificacao in classificacoes:
            lista.append(classificacao.json())
        return lista

    @staticmethod
    def create_classificacao(
        data_hora_classificacao,
        gravidade_id_gravidade,
        sinal_id_sinal,
        paciente_id_paciente,
        auditor_id_auditor,
    ):
        data_hora_classificacao = datetime.strptime(
            data_hora_classificacao, "%Y-%m-%d %H:%M:%S"
        )
        classificacao = Classificacao(
            data_hora_classificacao,
            gravidade_id_gravidade,
            sinal_id_sinal,
            paciente_id_paciente,
            auditor_id_auditor,
        )

        db.session.add(classificacao)
        db.session.commit()

        return classificacao.json()

    @staticmethod
    def update_classificacao(
        id,
        data_hora_classificacao,
        gravidade_id_gravidade,
        sinal_id_sinal,
        paciente_id_paciente,
        auditor_id_auditor,
    ):
        classificacao = db.session.get(Classificacao, id)
        if classificacao:
            classificacao.data_hora_classificacao = data_hora_classificacao
            classificacao.gravidade_id_gravidade = gravidade_id_gravidade
            classificacao.sinal_id_sinal = sinal_id_sinal
            classificacao.paciente_id_paciente = paciente_id_paciente
            classificacao.auditor_id_auditor = auditor_id_auditor
            db.session.commit()
            return classificacao.json()
        return None

    @staticmethod
    def delete_classificacao(id):
        classificacao = db.session.get(Classificacao, id)
        if classificacao:
            db.session.delete(classificacao)
            db.session.commit()
            return classificacao.json()
        return None
