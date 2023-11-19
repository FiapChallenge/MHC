""" 
Objetivos:
• A partir do modelo de banco de dados e tabelas implementadas na disciplina de Building Relational Database,
implementar um sistema de CRUD (Inserir, Excluir, Alterar, Consultar) integrado com o banco de dados Oracle.
Requisitos do Sistema:
• - Implementar um menu de opções com as principais funcionalidades oferecidas pelo sistema.
• - Realizar validações nas entradas de dados do usuário.
• - Aplicar adequadamente o tratamento de exceções.
• - Utilizar estruturas de decisão e repetição.
• - Utilizar funções com passagem de parâmetros e retorno.
• - Realizar pelo menos 3 consultas ao banco de dados e disponibilizar ao usuário a opção de exportar essas
consultas para um arquivo JSON.
"""


import os
import utils.comandosDB as comandosDB


def print_menu(tabelas):
    tabelas = "\n".join([f"{key} - {value}" for key, value in tabelas.items()])
    menu = f"""
--------------------------
      MENU - TABELAS
{tabelas}
    """

    print(menu)


if __name__ == "__main__":
    tabela_menu = {
        0: "Sair",
        1: "Auditor",
        2: "Paciente",
        3: "Sinal",
        4: "Gravidade",
        5: "Classificação",
    }
    while True:
        print_menu(tabela_menu)
        option_int = input("Digite a opção desejada: ")
        if option_int.isnumeric():
            option = int(option_int)
        else:
            print("Digite um número")
            continue
        option = int(option_int)
        if comandosDB.config["clear_output"]:
            os.system("cls" if os.name == "nt" else "clear")
        if option == 0:
            break
        elif option in tabela_menu:
            comandosDB.menu_crud(tabela_menu[option])
