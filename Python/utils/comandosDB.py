import inspect
import json
import os
import textwrap
import csv
from api import Auditor
from tabulate import tabulate
from classes_crud import (
    Auditor,
    AuditorCRUD,
    Paciente,
    PacienteCRUD,
    Sinal,
    SinalCRUD,
    Gravidade,
    GravidadeCRUD,
    Classificacao,
    ClassificacaoCRUD,
)

try:
    with open("settings.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {"clear_output": False, "sort_by": "ID", "export": {format: "json"}}


def wrap_text(sentence, width=40):
    wrapped_text = textwrap.fill(sentence, width)
    return wrapped_text


def menu_crud(nome):
    if config["clear_output"]:
        os.system("cls" if os.name == "nt" else "clear")
    match nome:
        case "Auditor":
            classe = Auditor
            crud = AuditorCRUD()
        case "Paciente":
            classe = Paciente
            crud = PacienteCRUD()
        case "Sinal":
            classe = Sinal
            crud = SinalCRUD()
        case "Gravidade":
            classe = Gravidade
            crud = GravidadeCRUD()
        case "Classificação":
            classe = Classificacao
            crud = ClassificacaoCRUD()
        case _:
            print("Tabela não encontrada")
            return
    while True:
        menu = f"""
--------------------------
      {nome.upper()}
0 - Voltar
1 - Consultar
2 - Inserir
3 - Excluir
4 - Alterar
"""
        print(menu)
        option = input("Digite a opção desejada: ")
        if option.isnumeric():
            option = int(option)
        else:
            print("Digite um número")
            continue
        if config["clear_output"]:
            os.system("cls" if os.name == "nt" else "clear")
        match option:
            case 0:
                return
            case 1:
                select_menu(classe, crud)
            case 2:
                insert(classe, crud)
            case 3:
                delete(crud)
            case 4:
                update(classe, crud)


def create_instance(classe):
    args = inspect.getfullargspec(classe.__init__).args[1:]
    user_inputs = {}
    for arg in args:
        value = input(f"Digite o valor para {arg}: ")

        validation_method = f"validate_{arg}"
        if hasattr(classe, validation_method):
            while True:
                try:
                    value = getattr(classe, validation_method)(value)
                    break
                except ValueError as e:
                    print(f"Valor inválido: {e}")
                    value = input(f"Digite o valor para {arg}: ")

        if value == "":
            value = None
        user_inputs[arg] = value

    class_instance = classe(**user_inputs)
    return class_instance


def update_instance(classe, objeto):
    args = inspect.getfullargspec(classe.__init__).args[1:]
    user_inputs = {}
    for arg in args:
        value = input(f"Digite o novo valor para {arg} (valor atual: {objeto[arg]}): ")

        validation_method = f"validate_{arg}"
        if hasattr(classe, validation_method):
            while True:
                try:
                    value = getattr(classe, validation_method)(value)
                    break
                except ValueError as e:
                    print(f"Valor inválido: {e}")
                    value = input(
                        f"Digite o novo valor para {arg} (valor atual: {objeto[arg]}): "
                    )

        user_inputs[arg] = value

    class_instance = classe(**user_inputs)
    return class_instance


def insert(classe, classeCrud):
    print(
        f"""
--------------------------
    INSERIR EM {classe.__name__.upper()}
"""
    )
    class_instance = create_instance(classe)
    objeto = classeCrud.create(class_instance)
    key = [key for key in objeto if key.startswith("id_")][0]
    id = objeto[key]
    print(f"Objeto criado com sucesso com id: {id}")


def delete(classeCrud):
    print(
        f"""
--------------------------
    EXCLUIR DE {classeCrud.__class__.__name__.upper().replace("CRUD", "")}
"""
    )
    id = input("Digite o ID: ")
    removido = classeCrud.delete(id)
    if removido:
        print(removido)
        print("Removido com sucesso")
    else:
        print("ID não encontrado")


def update(classe, classeCrud):
    print(
        f"""
--------------------------
    ATUALIZAR EM {classe.__name__.upper()}
"""
    )
    id = input("Digite o ID do registro a ser atualizado: ")

    objeto = classeCrud.get_by_id(id)
    if objeto:
        class_instance = update_instance(classe, objeto)
        objeto = classeCrud.update(id, class_instance)
        print("Atualizado com sucesso")
    else:
        print("ID não encontrado")


def select_menu(classe, classeCrud):
    menu = f"""
--------------------------
    CONSULTAR {classe.__name__.upper()}
0 - Voltar
1 - Todos
2 - Por ID
3 - Por campo
"""
    print(menu)
    option = input("Digite a opção desejada: ")
    if option.isnumeric():
        option = int(option)
    else:
        print("Digite um número")
        return
    if config["clear_output"]:
        os.system("cls" if os.name == "nt" else "clear")
    match option:
        case 0:
            return
        case 1:
            select_all(classeCrud)
        case 2:
            select_by_id(classeCrud)
        case 3:
            select_by_field_menu(classe, classeCrud)


def select_all(classeCrud):
    objetos = classeCrud.get_all(sort_by=config["sort_by"])
    if objetos:
        for row in objetos:
            for key, value in row.items():
                if len(str(value)) > 40:
                    row[key] = wrap_text(str(value))
        print(tabulate(objetos, headers="keys", tablefmt="fancy_grid"))
        answer = input(f"Deseja exportar para {config['export']['format']}? (S/N): ")
        if answer.lower() == "s":
            match config["export"]["format"]:
                case "csv":
                    export_csv(objetos)
                case "json":
                    export_json(objetos)
    else:
        print("Nenhum registro encontrado")


def select_by_id(classeCrud):
    id = input("Digite o ID: ")
    if not id.isnumeric():
        print("Digite um número")
        select_by_id(classeCrud)
    objeto = classeCrud.get_by_id(id)
    if objeto:
        print(tabulate([objeto], headers="keys", tablefmt="fancy_grid"))
    else:
        print("ID não encontrado")


def select_by_field_menu(classe, classeCrud):
    campos = inspect.getfullargspec(classe.__init__).args[1:]
    campos = [campo for campo in campos if not campo.startswith("id_")]
    campos_txt = "\n".join([f"{i} - {campo}" for i, campo in enumerate(campos, 1)])
    menu = f"""
--------------------------
    CONSULTAR POR CAMPO
0 - Voltar
{campos_txt}
"""
    print(menu)
    option = input("Digite a opção desejada: ")
    if option.isnumeric():
        option = int(option)
    else:
        print("Digite um número")
        return
    if config["clear_output"]:
        os.system("cls" if os.name == "nt" else "clear")
    match option:
        case 0:
            return
        case _:
            select_by_field(classeCrud, campos[option - 1])


def select_by_field(classeCrud, campo):
    valor = input(f"Digite o valor para {campo}: ")
    objetos = classeCrud.get_by_field(campo, valor, sort_by=config["sort_by"])
    if objetos:
        for row in objetos:
            for key, value in row.items():
                if len(str(value)) > 40:
                    row[key] = wrap_text(str(value))
        print(tabulate(objetos, headers="keys", tablefmt="fancy_grid"))
        answer = input(f"Deseja exportar para {config['export']['format']}? (S/N): ")
        if answer.lower() == "s":
            match config["export"]["format"]:
                case "csv":
                    export_csv(objetos)
                case "json":
                    export_json(objetos)
    else:
        print("Nenhum registro encontrado")


def export_csv(obj):
    for row in obj:
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.replace("\n", " ")
    with open("export.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=obj[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(obj)


def export_json(obj):
    for row in obj:
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.replace("\n", " ")
    with open("export.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)
