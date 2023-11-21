from api import db, Auditor, Paciente, Sinal, Gravidade, Classificacao


class AuditorCRUD:
    @staticmethod
    def type_of_sort(sort_by, direction):
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
    def get_all(sort_by="ID", direction="asc"):
        auditores = Auditor.query.order_by(
            AuditorCRUD.type_of_sort(sort_by, direction)
        ).all()
        lista = []
        for auditor in auditores:
            lista.append(auditor.json())
        return lista

    @staticmethod
    def get_by_id(id):
        auditor = db.session.get(Auditor, id)
        if auditor:
            return auditor.json()
        return None

    @staticmethod
    def get_by_name(name, start_with=False, sort_by="ID", direction="asc"):
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
    def get_by_field(field, value, start_with=False, sort_by="ID", direction="asc"):
        # Assuming the field is a valid attribute of the Auditor model
        filter_condition = (
            getattr(Auditor, field).ilike(f"{value}%")
            if start_with
            else getattr(Auditor, field).ilike(f"%{value}%")
        )

        auditores = (
            Auditor.query.filter(filter_condition)
            .order_by(AuditorCRUD.type_of_sort(sort_by, direction))
            .all()
        )

        lista = [auditor.json() for auditor in auditores]
        return lista

    @staticmethod
    def create(auditor):
        db.session.add(auditor)
        db.session.commit()
        return auditor.json()

    @staticmethod
    def update(id, auditor_novo):
        auditor = db.session.get(Auditor, id)
        if auditor:
            auditor.nome = auditor_novo.nome
            auditor.cpf = auditor_novo.cpf
            auditor.crm = auditor_novo.crm
            auditor.coren = auditor_novo.coren
            auditor.especialidade = auditor_novo.especialidade
            db.session.commit()
            return auditor.json()
        return None

    @staticmethod
    def delete(id):
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
    def get_all(sort_by="ID", direction="asc"):
        pacientes = Paciente.query.order_by(
            PacienteCRUD.type_of_sort(sort_by, direction)
        ).all()
        lista = []
        for paciente in pacientes:
            lista.append(paciente.json())
        return lista

    @staticmethod
    def get_by_id(id):
        paciente = db.session.get(Paciente, id)
        if paciente:
            return paciente.json()
        return None

    @staticmethod
    def get_by_name(name, start_with=False, sort_by="ID", direction="asc"):
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
    def get_by_field(field, value, start_with=False, sort_by="ID", direction="asc"):
        filter_condition = (
            getattr(Paciente, field).ilike(f"{value}%")
            if start_with
            else getattr(Paciente, field).ilike(f"%{value}%")
        )

        pacientes = (
            Paciente.query.filter(filter_condition)
            .order_by(PacienteCRUD.type_of_sort(sort_by, direction))
            .all()
        )

        lista = [paciente.json() for paciente in pacientes]
        return lista

    @staticmethod
    def create(
        paciente,
    ):
        db.session.add(paciente)
        db.session.commit()
        return paciente.json()

    @staticmethod
    def update(
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
    def delete(id):
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
    def get_all(sort_by="ID", direction="asc"):
        sinais = Sinal.query.order_by(SinalCRUD.type_of_sort(sort_by, direction)).all()
        lista = []
        for sinal in sinais:
            lista.append(sinal.json())
        return lista

    @staticmethod
    def get_by_id(id):
        sinal = db.session.get(Sinal, id)
        if sinal:
            return sinal.json()
        return None

    @staticmethod
    def get_by_name(name, start_with=False, sort_by="ID", direction="asc"):
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
    def get_by_field(field, value, start_with=False, sort_by="ID", direction="asc"):
        # Assuming the field is a valid attribute of the Sinal model
        filter_condition = (
            getattr(Sinal, field).ilike(f"{value}%")
            if start_with
            else getattr(Sinal, field).ilike(f"%{value}%")
        )

        sinais = (
            Sinal.query.filter(filter_condition)
            .order_by(SinalCRUD.type_of_sort(sort_by, direction))
            .all()
        )

        lista = [sinal.json() for sinal in sinais]
        return lista

    @staticmethod
    def create(sinal):
        db.session.add(sinal)
        db.session.commit()
        return sinal.json()

    @staticmethod
    def update(id, nome, descricao):
        sinal = db.session.get(Sinal, id)
        if sinal:
            sinal.nome = nome
            sinal.descricao = descricao
            db.session.commit()
            return sinal.json()
        return None

    @staticmethod
    def delete(id):
        sinal = db.session.get(Sinal, id)
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
    def get_all(sort_by="ID", direction="asc"):
        gravidades = Gravidade.query.order_by(
            GravidadeCRUD.type_of_sort(sort_by, direction)
        ).all()
        lista = []
        for gravidade in gravidades:
            lista.append(gravidade.json())
        return lista

    @staticmethod
    def get_by_id(id):
        gravidade = db.session.get(Gravidade, id)
        if gravidade:
            return gravidade.json()
        return None

    @staticmethod
    def get_by_name(name, start_with=False, sort_by="ID", direction="asc"):
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
    def get_by_field(field, value, start_with=False, sort_by="ID", direction="asc"):
        # Assuming the field is a valid attribute of the Gravidade model
        filter_condition = (
            getattr(Gravidade, field).ilike(f"{value}%")
            if start_with
            else getattr(Gravidade, field).ilike(f"%{value}%")
        )

        gravidades = (
            Gravidade.query.filter(filter_condition)
            .order_by(GravidadeCRUD.type_of_sort(sort_by, direction))
            .all()
        )

        lista = [gravidade.json() for gravidade in gravidades]
        return lista

    @staticmethod
    def create(gravidade):
        db.session.add(gravidade)
        db.session.commit()
        return gravidade.json()

    @staticmethod
    def update(id, gravidade_novo):
        gravidade = db.session.get(Gravidade, id)
        if gravidade:
            gravidade.nome_gravidade = gravidade_novo.nome_gravidade
            gravidade.nome_cor = gravidade_novo.nome_cor
            gravidade.hexadecimal_cor = gravidade_novo.hexadecimal_cor
            db.session.commit()
            return gravidade.json()
        return None

    @staticmethod
    def delete(id):
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

    @staticmethod
    def get_all(sort_by="ID", direction="asc"):
        classificacoes = Classificacao.query.order_by(
            ClassificacaoCRUD.type_of_sort(sort_by, direction)
        ).all()
        lista = []
        for classificacao in classificacoes:
            lista.append(classificacao.json())
        return lista

    @staticmethod
    def get_by_id(id):
        classificacao = db.session.get(Classificacao, id)
        if classificacao:
            return classificacao.json()
        return None

    @staticmethod
    def get_by_field(field, value, start_with=False, sort_by="ID", direction="asc"):
        # Assuming the field is a valid attribute of the Classificacao model
        filter_condition = (
            getattr(Classificacao, field).ilike(f"{value}%")
            if start_with
            else getattr(Classificacao, field).ilike(f"%{value}%")
        )

        classificacoes = (
            Classificacao.query.filter(filter_condition)
            .order_by(ClassificacaoCRUD.type_of_sort(sort_by, direction))
            .all()
        )

        lista = [classificacao.json() for classificacao in classificacoes]
        return lista

    @staticmethod
    def create(
        classificacao,
    ):
        db.session.add(classificacao)
        db.session.commit()

        return classificacao.json()

    @staticmethod
    def update(
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
    def delete(id):
        classificacao = db.session.get(Classificacao, id)
        if classificacao:
            db.session.delete(classificacao)
            db.session.commit()
            return classificacao.json()
        return None
