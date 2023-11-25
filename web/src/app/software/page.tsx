"use client";
import { useEffect, useRef, useState } from "react";
import {
  IoAlertCircleOutline,
  IoInformationCircleOutline,
} from "react-icons/io5";
import { useRecoilState, useRecoilValue } from "recoil";
import { loggedState, selectedFluxoState } from "../recoilContextProvider";
import Notification from "@/components/Notification/Notification";
import CardFluxo from "@/components/Cards/CardFluxo";
import classNames from "classnames";

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
  const [selectedFluxo, setSelectedFluxo] = useRecoilState(selectedFluxoState);
  const [sinais, setSinais] = useState<Sinal[]>([]);
  const [sinal, setSinal] = useState<Sinal>({
    nome: "",
  });

  const [notificationFinal, setNotificationFinal] = useState<NotificationProps>(
    {
      nome: "",
      descricao: "",
      Icon: IoInformationCircleOutline,
      color: { bg: "", text: "" },
      hidden: true,
      size: "",
    }
  );
  const [notificationKey, SetNotificationKey] = useState(0);

  const [slide, setSlide] = useState(0);

  const [erroAPI, setErroAPI] = useState(false);

  useEffect(() => {
    if (
      sessionStorage.getItem("token-user") != null &&
      sessionStorage.getItem("token-user") != undefined
    ) {
      // console.log("token-user: " + sessionStorage.getItem("token-user"));
    } else {
      window.location.href = "/login";
    }

    const getSinais = async () => {
      try {
        const res = await fetch("http://localhost:3000/api/sinal", {
          cache: "no-store",
        });
        const data: Sinal[] = await res.json();
        setSinais(data);
      } catch (error) {
        console.log("teste");

        setErroAPI(true);
      }
    };
    getSinais();
    const getPacientes = async () => {
      try {
        const res = await fetch("http://localhost:3000/api/paciente", {
          cache: "no-store",
        });
        const data: Paciente[] = await res.json();
        setPacientes(data);
      } catch (error) {
        setErroAPI(true);
      }
    };
    getPacientes();
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

    if (paciente.cpf) {
      paciente.cpf = paciente.cpf.replace(/\D/g, "");
    }
    if (paciente.rg) {
      paciente.rg = paciente.rg.replace(/\D/g, "");
    }

    if (pacienteForm.current) {
      pacienteForm.current.classList.add("translate-x-[-150%]");
      classificacaoForm.current?.classList.add("-translate-x-[100%]");
      classificacaoForm.current?.classList.remove("translate-x-[100%]");
    }
    setSlide(1);
    // const section = document.getElementById("app-section");
    // if (section) {
    //   section.scrollIntoView({ behavior: "smooth",  });
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

  const getNameFluxo = (index: number) => {
    switch (index) {
      case 1:
        return "Emergência";
      case 2:
        return "Muito Urgente";
      case 3:
        return "Urgente";
      case 4:
        return "Pouco Urgente";
      default:
        return "Não Urgente";
    }
  };

  const getColorFluxo = (index: number) => {
    switch (index) {
      case 1:
        return "text-red-600";
      case 2:
        return "text-orange-600";
      case 3:
        return "text-amber-500";
      case 4:
        return "text-green-500";
      default:
        return "text-blue-500";
    }
  };

  const handleSalvar = async () => {
    // logica para cpf unico
    // const pacienteByCpf = pacientes.find(
    //   (pacienteDB) => pacienteDB.cpf === paciente.cpf
    // );
    // console.log(pacienteByCpf);
    // if (pacienteByCpf) {
    //   alert("CPF já cadastrado!");
    // } else {
    const dataFormatada = getDateNow();
    console.log(dataFormatada);

    paciente.data_hora_entrada = dataFormatada;
    window.scrollTo({ top: 0, behavior: "smooth" });
    try {
      fetch("http://localhost:3000/api/paciente", {
        method: "POST",
        body: JSON.stringify(paciente),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
          }
        })
        .catch((error) => {
          SetNotificationKey((prev) => prev + 1);
          setNotificationFinal({
            nome: "Erro",
            descricao: "Erro ao salvar dados!",
            Icon: IoAlertCircleOutline,
            color: { bg: "bg-red-100", text: "text-red-900" },
            hidden: false,
            size: "w-12 h-12",
          });
        });
    } catch (error) {
      console.log("Caught an error: ", error);
    }
    try {
      fetch("http://localhost:3000/api/classificacao", {
        method: "POST",
        body: JSON.stringify({
          data_hora_classificacao: getDateNow(),
          gravidade_id_gravidade: selectedFluxo,
          sinal_id_sinal: sinal.id_sinal,
          auditor_id_auditor: 1,
          paciente_id_paciente: 1,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
          }
          SetNotificationKey((prev) => prev + 1);
          setNotificationFinal({
            nome: "Sucesso",
            descricao: "Dados salvos com sucesso!",
            Icon: IoInformationCircleOutline,
            color: { bg: "bg-green-100", text: "text-green-900" },
            hidden: false,
            size: "w-12 h-12",
            timeout: 2000,
          });
          setPaciente({
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
          setSinal({
            nome: "",
          });

          setTimeout(() => {
            if (pacienteForm.current && slide === 1) {
              pacienteForm.current.classList.remove("translate-x-[-150%]");
              classificacaoForm.current?.classList.remove(
                "-translate-x-[100%]"
              );
              classificacaoForm.current?.classList.add("translate-x-[100%]");
            }
            setTimeout(() => {
              setSlide(0);
              setSelectedFluxo(0);
            }, 1000);
          }, 1000);
        })
        .catch((error) => {
          SetNotificationKey((prev) => prev + 1);
          setNotificationFinal({
            nome: "Erro",
            descricao: "Erro ao salvar dados!",
            Icon: IoAlertCircleOutline,
            color: { bg: "bg-red-100", text: "text-red-900" },
            hidden: false,
            size: "w-12 h-12",
          });
        });
    } catch (error) {
      console.error("Caught an error:", error);
    }
    // }
  };

  if (logged) {
    return (
      <>
        <section
          id="app-section"
          className="min-h-[60vh] flex px-4 justify-center bg-background-50"
        >
          <div className="overflow-x-clip h-full">
            <div className="bg-white relative duration-1000 transition-all shadow-md max-w-screen-lg my-20 mx-auto rounded-2xl px-8 pt-6 pb-8 flex flex-col">
              <div id="Title" className="flex flex-col justify-center gap-y-4">
                <Notification {...notificationFinal} key={notificationKey} />
                <div className="flex items-center gap-x-2">
                  <span className="border-l-4 rounded border-l-accent h-full"></span>
                  <h2 className="text-xl xs:text-2xl sm:text-3xl font-bold uppercase tracking-wider">
                    Classificação de Risco
                  </h2>
                </div>
                {erroAPI ? (
                  <div>
                    <Notification
                      nome="Erro"
                      descricao="Erro ao carregar dados!"
                      Icon={IoInformationCircleOutline}
                      color={{ bg: "bg-red-100", text: "text-red-900" }}
                      hidden={false}
                      size="w-8 h-8"
                    />
                  </div>
                ) : (
                  <></>
                )}
              </div>
              <hr className="my-5" />
              <div className="relative slides-list">
                <div
                  ref={pacienteForm}
                  className="visible transition-transform duration-[1.5s] ease-[cubic-bezier(0.68,-0.25,0.4,1.25);]"
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
                            setPaciente({
                              ...paciente,
                              rg: rgMask(e.target.value),
                            })
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
                            setPaciente({
                              ...paciente,
                              altura: +e.target.value,
                            })
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
                            onChange={(e) => {
                              let id: number | string | null =
                                e.target.options[
                                  e.target.selectedIndex
                                ].getAttribute("data-key");
                              if (id) {
                                const idInt = parseInt(id);
                                setSinal({
                                  ...sinal,
                                  nome: e.target.value,
                                  id_sinal: idInt,
                                });
                              } else {
                                setSinal({
                                  ...sinal,
                                  nome: e.target.value,
                                  id_sinal: null,
                                });
                              }
                            }}
                            required
                          >
                            <option value="" disabled>
                              Selecione
                            </option>
                            <option value="Dor">Dor</option>
                            {sinais.map((sinal) => (
                              <option
                                key={sinal.id_sinal}
                                value={sinal.nome}
                                data-key={sinal.id_sinal}
                              >
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
                            {sinal.nome === "Dor" ? (
                              <Notification
                                nome="Dor"
                                descricao="A dor pode ser classificada em aguda ou crônica. A dor aguda é aquela que surge de forma repentina e intensa, durando pouco tempo. Já a dor crônica é aquela que se prolonga por um período maior de tempo, podendo durar meses ou anos."
                                Icon={IoInformationCircleOutline}
                                hidden={false}
                              />
                            ) : (
                              ""
                            )}
                            {sinais.map((sinalDB) => (
                              <Notification
                                nome={sinalDB.nome}
                                key={sinalDB.nome}
                                descricao={
                                  sinalDB.descricao ? sinalDB.descricao : ""
                                }
                                Icon={IoInformationCircleOutline}
                                hidden={sinalDB.nome !== sinal.nome}
                              />
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="flex justify-end mt-8">
                      <button
                        type="submit"
                        className="bg-primary hover:bg-primary-600 text-xl transition-colors duration-300 text-white font-bold py-2 px-4 rounded-xl"
                      >
                        Continuar
                      </button>
                    </div>
                  </form>
                </div>
                {/* Fluxogramas */}
                <div
                  ref={classificacaoForm}
                  className=" h-full top-0 transition-transform w-full translate-x-[100%] duration-[1.5s] ease-[cubic-bezier(0.68,-0.25,0.4,1.25);]"
                >
                  <div className="h-full flex flex-col justify-between">
                    <div>
                      <h1 className="text-lg xs:text-xl sm:text-2xl font-bold uppercase font-heading mb-8">
                        {sinal.nome}
                      </h1>
                      <ol
                        className={classNames({
                          "grid grid-cols-1 md:grid-cols-2 justify-center items-center gap-x-16 gap-y-16":
                            true,
                          hidden: slide !== 1,
                        })}
                      >
                        <CardFluxo
                          cor={{
                            bg: "bg-red-600",
                            shadow: "shadow-red-500/50",
                          }}
                          sintomas={[
                            "Obstrução de vias aérea",
                            "Respiração inadequada",
                            "Hemorragia exanguinante",
                            "Choque",
                          ]}
                          hidden={slide !== 1}
                          index={1}
                        />
                        <CardFluxo
                          cor={{
                            bg: "bg-orange-600",
                            shadow: "shadow-orange-400/50",
                          }}
                          sintomas={[
                            "Mecanismo de trauma significativo",
                            "Dispneia aguda",
                            "Hemorragia maior incontrolável",
                            "Alteração súbita da consciência",
                            "Déficit neurológico agudo",
                            "Dor intensa",
                          ]}
                          hidden={slide !== 1}
                          index={2}
                        />
                        <CardFluxo
                          cor={{
                            bg: "bg-amber-500",
                            shadow: "shadow-yellow-500/50",
                          }}
                          // Hemorragia menor incontrolável
                          // Historia do inconsciência
                          // Déficit neurológico novo
                          // Distúrbio do coagulaçao
                          // História discordante
                          // Dor
                          sintomas={[
                            "Hemorragia menor incontrolável",
                            "História de inconsciência",
                            "Déficit neurológico novo",
                            "Distúrbio do coagulação",
                            "História discordante",
                            "Dor moderada",
                          ]}
                          hidden={slide !== 1}
                          index={3}
                        />
                        <CardFluxo
                          cor={{
                            bg: "bg-green-500",
                            shadow: "shadow-green-500/50",
                          }}
                          //                         Edema
                          // Deformidade
                          // Dor leve recente
                          // Evento reconto
                          sintomas={[
                            "Edema",
                            "Deformidade",
                            "Dor leve recente",
                            "Evento reconto",
                          ]}
                          hidden={slide !== 1}
                          index={4}
                        />
                      </ol>
                      <div className="flex flex-col lg:flex-row gap-y-8 justify-between items-center mt-12">
                        <h3 className="uppercase gap-x-2 font-heading flex flex-col md:flex-row text-center md:text-center text-xl xs:text-2xl sm:text-4xl md:text-3xl">
                          Classificação:
                          <span
                            className={`font-bold text-2xl xs:text-3xl sm:text-4xl md:text-3xl ${getColorFluxo(
                              selectedFluxo
                            )}`}
                          >
                            {getNameFluxo(selectedFluxo)}
                          </span>
                        </h3>
                        <div className="flex items-center gap-x-8">
                          <button
                            className="bg-secondary hover:bg-secondary-300 text-xl transition-colors duration-300 text-text font-bold py-2 px-4  rounded-xl"
                            onClick={() => {
                              // go to slide 3 if selectedFluxo is different of 0
                              if (pacienteForm.current) {
                                pacienteForm.current.classList.remove(
                                  "translate-x-[-150%]"
                                );
                                classificacaoForm.current?.classList.remove(
                                  "-translate-x-[100%]"
                                );
                                classificacaoForm.current?.classList.add(
                                  "translate-x-[100%]"
                                );
                              }
                              setTimeout(() => {
                                setSlide(0);
                              }, 1000);
                            }}
                          >
                            Voltar
                          </button>
                          <button
                            className="bg-primary hover:bg-primary-600 text-xl transition-colors duration-300 text-white font-bold py-2 px-4  rounded-xl"
                            onClick={() => {
                              handleSalvar();
                            }}
                          >
                            Salvar
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
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
