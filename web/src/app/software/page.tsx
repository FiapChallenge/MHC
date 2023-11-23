"use client";
import { useEffect, useState } from "react";

export default function Software() {
  const [paciente, setPaciente] = useState<Paciente>({
    nome: "",
    cpf: "",
    rg: "",
    data_hora_entrada: "",
    data_hora_saida: "",
    sexo: "",
    idade: 0,
    altura: 0,
    peso: 0,
  });

  useEffect(() => {
    if (
      sessionStorage.getItem("token-user") != null &&
      sessionStorage.getItem("token-user") != undefined
    ) {
      // console.log("token-user: " + sessionStorage.getItem("token-user"));
    } else {
      window.location.href = "/login";
    }
  });

  const getDateNow = () => {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const dataFormatada = getDateNow();
    setPaciente({ ...paciente, data_hora_entrada: dataFormatada });
    alert(JSON.stringify(paciente, null, 4));
  };

  return (
    <>
      <section className="min-h-[60vh] flex px-4 bg-background-50">
        <div className="bg-white shadow-md max-w-screen-2xl my-20 mx-auto rounded-2xl px-8 pt-6 pb-8 flex flex-col">
          <div className="flex items-center gap-x-2">
            <span className="border-l-4 rounded border-l-accent h-full"></span>
            <h2 className="text-2xl font-bold">Cadastro Paciente</h2>
          </div>
          <hr className="my-5" />
          <form onSubmit={handleSubmit}>
            <div className="-mx-3 md:flex mb-6">
              <div className="md:w-full px-3 mb-6 md:mb-0">
                <label
                  className="block uppercase tracking-wide text-md font-bold mb-2"
                  htmlFor="grid-first-name"
                >
                  Nome Completo *
                </label>
                <input
                  className="appearance-none block w-full border rounded py-3 px-4 focus:outline-primary"
                  id="grid-first-name"
                  type="text"
                  placeholder="Nome completo"
                  required
                  value={paciente.nome}
                  onChange={(e) =>
                    setPaciente({ ...paciente, nome: e.target.value })
                  }
                />
              </div>
            </div>
            <div className="-mx-3 md:flex mb-6">
              <div className="md:w-1/2 px-3 mb-6 md:mb-0">
                <label
                  className="block uppercase tracking-wide text-md font-bold mb-2"
                  htmlFor="grid-cpf"
                >
                  CPF
                </label>
                <input
                  className="appearance-none block w-full border rounded py-3 px-4 focus:outline-primary"
                  id="grid-cpf"
                  type="text"
                  placeholder="CPF"
                  value={paciente.cpf}
                  onChange={(e) =>
                    setPaciente({ ...paciente, cpf: e.target.value })
                  }
                />
              </div>
              <div className="md:w-1/2 px-3">
                <label
                  className="block uppercase tracking-wide text-md font-bold mb-2"
                  htmlFor="grid-rg"
                >
                  RG
                </label>
                <input
                  className="appearance-none block w-full border rounded py-3 px-4 focus:outline-primary"
                  id="grid-rg"
                  type="text"
                  placeholder="RG"
                  value={paciente.rg}
                  onChange={(e) =>
                    setPaciente({ ...paciente, rg: e.target.value })
                  }
                />
              </div>
            </div>
            <div className="-mx-3 md:flex mb-6">
              <div className="md:w-1/4 px-3">
                <label
                  className="block uppercase tracking-wide text-md font-bold mb-2 "
                  htmlFor="grid-sexo"
                >
                  Sexo
                </label>
                <div className="relative">
                  <select
                    className="block appearance-none w-full border py-3 px-4 pr-8 rounded focus:outline-primary"
                    id="grid-sexo"
                    value={paciente.sexo}
                    onChange={(e) =>
                      setPaciente({ ...paciente, sexo: e.target.value })
                    }
                  >
                    <option value="">Sexo</option>
                    <option value="M">Masculino</option>
                    <option value="F">Feminino</option>
                  </select>
                  <div className="pointer-events-none absolute flex items-center px-2 right-0 top-0 h-full">
                    <svg
                      className="h-4 w-4"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                    >
                      <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                    </svg>
                  </div>
                </div>
              </div>
              <div className="md:w-1/4 px-3">
                <label
                  className="block uppercase tracking-wide text-md font-bold mb-2"
                  htmlFor="grid-idade"
                >
                  Idade
                </label>
                <input
                  className="appearance-none block w-full border rounded py-3 px-4 focus:outline-primary"
                  id="grid-idade"
                  type="number"
                  placeholder="Idade"
                  value={paciente.idade}
                  onChange={(e) =>
                    setPaciente({ ...paciente, idade: +e.target.value })
                  }
                />
              </div>
              <div className="md:w-1/4 px-3 mb-6 md:mb-0">
                <label
                  className="block uppercase tracking-wide text-md font-bold mb-2"
                  htmlFor="grid-altura"
                >
                  Altura (CM)
                </label>
                <input
                  className="appearance-none block w-full border rounded py-3 px-4 focus:outline-primary"
                  id="grid-altura"
                  type="number"
                  placeholder="Altura"
                  value={paciente.altura}
                  onChange={(e) =>
                    setPaciente({ ...paciente, altura: +e.target.value })
                  }
                />
              </div>
              <div className="md:w-1/4 px-3">
                <label
                  className="block uppercase tracking-wide text-md font-bold mb-2"
                  htmlFor="grid-peso"
                >
                  Peso (KG)
                </label>
                <input
                  className="appearance-none block w-full border rounded py-3 px-4 focus:outline-primary"
                  id="grid-peso"
                  type="number"
                  placeholder="Peso"
                  value={paciente.peso}
                  onChange={(e) =>
                    setPaciente({ ...paciente, peso: +e.target.value })
                  }
                />
              </div>
            </div>
            <hr className="my-3" />
            <div className="flex justify-end">
              <button
                type="submit"
                className="bg-accent hover:bg-accent-hover text-white font-bold py-2 px-4 rounded-xl"
              >
                Cadastrar
              </button>
            </div>
          </form>
        </div>
      </section>
    </>
  );
}
