"use client";
import { useEffect, useRef, useState } from "react";
import { IoInformationCircleOutline } from "react-icons/io5";
import { useRecoilValue } from "recoil";
import { loggedState } from "../recoilContextProvider";

export default function Software(this: any) {
  const pacienteForm = useRef<HTMLDivElement>(null);
  const classificacaoForm = useRef<HTMLDivElement>(null);
  const [pacientes, setPacientes] = useState<Paciente[]>([]);
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
  const logged = useRecoilValue(loggedState);
  const [sinais, setSinais] = useState<Sinal[]>([]);
  const [sinal, setSinal] = useState<Sinal>({
    nome: "",
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

    try {
      fetch("http://localhost:3000/api/sinais", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
          }
          return res.json();
        })
        .then((data) => {
          setSinais(data);
        });
    } catch (error) {
      alert("Erro ao buscar sinais!");
    }

    try {
      fetch("http://localhost:3000/api/paciente", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
          }
          return res.json();
        })
        .then((data) => {
          setPacientes(data);
        });
    } catch (error) {
      alert("Erro ao buscar pacientes!");
    }
  }, []);

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
    console.log(dataFormatada);

    paciente.data_hora_entrada = dataFormatada;

    console.log(paciente);

    if (paciente.cpf) {
      paciente.cpf = paciente.cpf.replace(/\D/g, "");
    }
    if (paciente.rg) {
      paciente.rg = paciente.rg.replace(/\D/g, "");
    }

    // const pacienteByCpf = pacientes.find(
    //   (pacienteDB) => pacienteDB.cpf === paciente.cpf
    // );
    // console.log(pacienteByCpf);
    // if (pacienteByCpf) {
    //   alert("CPF já cadastrado!");
    // } else {
    // try {
    //   fetch("http://localhost:3000/api/paciente", {
    //     method: "POST",
    //     body: JSON.stringify(paciente),
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //   })
    //     .then((res) => {
    //       if (!res.ok) {
    //         throw new Error(`HTTP error! Status: ${res.status}`);
    //       }
    //       return res.json();
    //     })
    //     .then((data) => {
    // alert("Paciente salvo com sucesso!");
    // add class translate-y-[-150%] to pacienteForm
    if (pacienteForm.current) {
      pacienteForm.current.classList.add("translate-x-[-150%]");
      classificacaoForm.current?.classList.remove("translate-x-[150%]");
    }
    // });
    // } catch (error) {
    //   alert("Erro ao salvar!");
    // }
    // }
  };

  const cpfMask = (value: any) => {
    return value
      .replace(/\D/g, "")
      .replace(/(\d{3})(\d)/, "$1.$2")
      .replace(/(\d{3})(\d)/, "$1.$2")
      .replace(/(\d{3})(\d{1,2})/, "$1-$2")
      .replace(/(-\d{2})\d+?$/, "$1");
  };

  const rgMask = (value: any) => {
    return value
      .replace(/\D/g, "")
      .replace(/(\d{2})(\d)/, "$1.$2")
      .replace(/(\d{3})(\d)/, "$1.$2")
      .replace(/(\d{3})(\d{1,2})/, "$1-$2")
      .replace(/(-\d{1})\d+?$/, "$1");
  };
  if (logged) {
    return (
      <>
        <section className="min-h-[60vh] flex px-4 bg-background-50">
          <div className="bg-white relative overflow-x-hidden shadow-md max-w-screen-2xl my-20 mx-auto rounded-2xl px-8 pt-6 pb-8 flex flex-col">
            <div className="flex items-center gap-x-2">
              <span className="border-l-4 rounded border-l-accent h-full"></span>
              <h2 className="text-xl xs:text-2xl font-bold uppercase tracking-wider">
                Classficação de Risco
              </h2>
            </div>
            <hr className="my-5" />
            <div
              ref={pacienteForm}
              className="transition-transform duration-[1.5s] ease-[cubic-bezier(0.68,-0.55,0.27,1.55);]"
            >
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
                      maxLength={14}
                      onChange={(e) =>
                        setPaciente({
                          ...paciente,
                          cpf: cpfMask(e.target.value),
                        })
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
                        setPaciente({ ...paciente, rg: rgMask(e.target.value) })
                      }
                    />
                  </div>
                </div>
                <div className="-mx-3 md:flex mb-6">
                  <div className="md:w-1/4 px-3 mb-6 md:mb-0">
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
                  <div className="md:w-1/4 px-3 mb-6 md:mb-0">
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
                <hr className="h-[2px] mx-auto my-8 bg-accent border-0 rounded " />
                <div className="-mx-3 md:flex mb-6">
                  <div className="md:w-full px-3 mb-6 md:mb-0">
                    <label
                      className="block uppercase tracking-wide text-md font-bold mb-2"
                      htmlFor="grid-queixa"
                    >
                      Queixa / Sintomas *
                    </label>
                    {/* select sinais */}
                    <div className="relative">
                      <select
                        className="block appearance-none w-full border py-3 px-4 pr-8 rounded focus:outline-primary"
                        id="grid-queixa"
                        value={sinal.nome}
                        onChange={(e) =>
                          setSinal({ ...sinal, nome: e.target.value })
                        }
                        required
                      >
                        <option value="" disabled>
                          Selecione
                        </option>
                        <option value="Dor">Dor</option>
                        {sinais.map((sinal) => (
                          <option key={sinal.id_sinal} value={sinal.nome}>
                            {sinal.nome}
                          </option>
                        ))}
                      </select>
                      <div className="pointer-events-none absolute flex items-center px-2 right-0 top-0 h-12">
                        <svg
                          className="h-4 w-4"
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 20 20"
                        >
                          <path
                            fill="#000"
                            fillRule="evenodd"
                            d="M10.707 12.95l.707.707L17.071 8l-1.414-1.414L11.414 10.828 7.172 6.586 5.758 8z"
                            clipRule="evenodd"
                          />
                        </svg>
                      </div>
                      <div className="mt-2">
                        {sinais.map((sinalDB) => (
                          <div
                            key={sinalDB.id_sinal}
                            className={`${
                              sinalDB.nome === sinal.nome ? "block" : "hidden"
                            } bg-secondary-100 flex flex-col md:flex-row items-center border max-w-[910px] border-gray-400 text-secondary-800 px-5 py-3 rounded relative`}
                            role="alert"
                          >
                            <IoInformationCircleOutline className="inline-block shrink-0 w-16 h-16 md:mr-4" />
                            <div>
                              <p className="font-bold font-heading text-center md:text-left mb-1 md:mb-0 xs:text-lg uppercase tracking-wide">
                                {sinalDB.nome}
                              </p>
                              <p className="block sm:inline">
                                {sinalDB.descricao}
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex justify-end mt-8">
                  <button
                    type="submit"
                    className="bg-primary hover:bg-accent-hover text-xl text-white font-bold py-2 px-4 rounded-xl"
                  >
                    Continuar
                  </button>
                </div>
              </form>
            </div>
            <div
              ref={classificacaoForm}
              className="absolute left-8 w-full pr-16 top-28 transition-transform translate-x-[150%] duration-[1.5s] ease-[cubic-bezier(0.68,-0.55,0.27,1.55);]"
            >
              <div className="h-full flex flex-col justify-between">
                <h1 className="text-xl font-bold uppercase font-heading">
                  {sinal.nome}
                </h1>
                <div className="flex justify-end mt-8">
                  <button
                    type="submit"
                    className="bg-primary hover:bg-accent-hover text-xl text-white font-bold py-2 px-4 rounded-xl"
                    onClick={() => {
                      if (pacienteForm.current) {
                        pacienteForm.current.classList.remove(
                          "translate-x-[-150%]"
                        );
                        classificacaoForm.current?.classList.add(
                          "translate-x-[150%]"
                        );
                      }
                    }}
                  >
                    Voltar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </>
    );
  } else {
    return <></>;
  }
}
