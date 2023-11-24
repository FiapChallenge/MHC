"use client";
import Image from "next/image";
import Logo from "@/assets/logo/LogoWithoutText.svg";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  IoAlertCircleOutline,
  IoCheckmarkCircleOutline,
  IoEyeOffOutline,
  IoEyeOutline,
} from "react-icons/io5";
import Notification from "@/components/Notification/Notification";

export default function Cadastro() {
  const router = useRouter();

  const [notification, setNotification] = useState<NotificationProps>({
    nome: "",
    descricao: "",
    size: "w-6 h-6",
    hidden: true,
  });

  const [auditores, setAuditores] = useState<Auditor[]>([]);
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");

  const [showPassword, setShowPassword] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  useEffect(() => {
    const getAuditores = async () => {
      try {
        const res = await fetch("http://localhost:3000/api/auditor", {
          cache: "no-store",
        });
        const data: Auditor[] = await res.json();
        setAuditores(data);
      } catch (error) {
        setNotification({
          Icon: IoAlertCircleOutline,
          nome: "Erro",
          descricao: "Erro ao carregar banco de dados!",
          size: "8",
          hidden: false,
          color: { bg: "bg-red-100", text: "text-red-900" },
        });
      }
    };
    getAuditores();
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const auditor = auditores.find((auditor) => auditor.email === email);
    if (auditor) {
      setNotification({
        Icon: IoAlertCircleOutline,
        nome: "Erro ao cadastrar",
        descricao: "E-mail já cadastrado",
        size: "6",
        hidden: false,
        color: { bg: "bg-red-100", text: "text-red-900" },
      });
    } else {
      try {
        const res = await fetch("http://localhost:3000/api/auditor", {
          method: "POST",
          body: JSON.stringify({ nome, email, senha }),
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        const data: Auditor = await res.json();
        setNotification({
          Icon: IoCheckmarkCircleOutline,
          nome: "Sucesso",
          descricao: "Cadastro realizado com sucesso!",
          size: "6",
          hidden: false,
          color: { bg: "bg-green-100", text: "text-green-900" },
        });
        setTimeout(() => {
          router.push("/login");
        }, 2000);
      } catch (error) {
        setNotification({
          Icon: IoAlertCircleOutline,
          nome: "Erro ao cadastrar",
          descricao: "Erro ao cadastrar",
          size: "6",
          hidden: false,
          color: { bg: "bg-red-100", text: "text-red-900" },
        });
      }
    }
  };

  return (
    <div className="py-28 flex flex-col items-center justify-center bg-background-50 px-4">
      <div className="flex flex-col bg-white shadow-xl px-4 sm:px-6 md:px-8 lg:px-10 py-8 rounded-2xl w-full max-w-md">
        <div className="mb-8">
          <Notification {...notification} />
        </div>
        <div className="flex justify-center items-center pb-4">
          <Image
            src={Logo}
            alt="Logo Manchester Healtcare"
            width={64}
            height={64}
            className="animate-spin-slow pause hover:play"
          />
        </div>
        <div className="font-bold font-heading self-center text-xl sm:text-2xl uppercase text-text">
          Cadastrar no MHC
        </div>
        <div className="mt-6">
          <form onSubmit={handleSubmit}>
            <div className="flex flex-col mb-6">
              <label
                htmlFor="nome"
                className="mb-1 text-xs sm:text-sm tracking-wide text-text"
              >
                Nome:
              </label>
              <div className="relative">
                <div className="inline-flex items-center justify-center absolute left-0 top-0 h-full w-10 text-gray-400">
                  <span>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="ionicon w-6 h-6"
                      viewBox="0 0 512 512"
                    >
                      <path
                        d="M344 144c-3.92 52.87-44 96-88 96s-84.15-43.12-88-96c-4-55 35-96 88-96s92 42 88 96z"
                        fill="none"
                        stroke="currentColor"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={32}
                      />
                      <path
                        d="M256 304c-87 0-175.3 48-191.64 138.6C62.39 453.52 68.57 464 80 464h352c11.44 0 17.62-10.48 15.65-21.4C431.3 352 343 304 256 304z"
                        fill="none"
                        stroke="currentColor"
                        strokeMiterlimit={10}
                        strokeWidth={32}
                      />
                    </svg>
                  </span>
                </div>
                <input
                  id="nome"
                  type="text"
                  name="nome"
                  className="text-sm sm:text-base placeholder-gray-500 pl-10 pr-4 rounded-lg border border-gray-400 w-full py-2 focus:outline-none focus:border-accent"
                  placeholder="Nome"
                  required
                  value={nome}
                  onChange={(e) => setNome(e.target.value)}
                />
              </div>
            </div>
            <div className="flex flex-col mb-6">
              <label
                htmlFor="email"
                className="mb-1 text-xs sm:text-sm tracking-wide text-text"
              >
                Endereço de e-mail:
              </label>
              <div className="relative">
                <div className="inline-flex items-center justify-center absolute left-0 top-0 h-full w-10 text-gray-400">
                  <svg
                    className="h-6 w-6"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </div>
                <input
                  id="email"
                  type="email"
                  name="email"
                  className="text-sm sm:text-base placeholder-gray-500 pl-10 pr-4 rounded-lg border border-gray-400 w-full py-2 focus:outline-none focus:border-accent"
                  placeholder="Endereço de e-mail"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>
            <div className="flex flex-col mb-6">
              <label
                htmlFor="senha"
                className="mb-1 text-xs sm:text-sm tracking-wide text-text"
              >
                Senha:
              </label>
              <div className="relative">
                <div
                  className="inline-flex items-center justify-center absolute right-0 top-0 h-full w-10 text-gray-400"
                  onClick={togglePasswordVisibility}
                >
                  {showPassword ? (
                    <IoEyeOutline className="text-gray-400 w-6 h-6" />
                  ) : (
                    <IoEyeOffOutline className="text-gray-400 w-6 h-6" />
                  )}
                </div>
                <div className="inline-flex items-center justify-center absolute left-0 top-0 h-full w-10 text-gray-400">
                  <span>
                    <svg
                      className="h-6 w-6"
                      fill="none"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </span>
                </div>
                <input
                  id="senha"
                  type={showPassword ? "text" : "password"}
                  name="senha"
                  className="text-sm sm:text-base placeholder-gray-500 pl-10 pr-4 rounded-lg border border-gray-400 w-full py-2 focus:outline-none focus:border-accent"
                  placeholder="Senha"
                  required
                  value={senha}
                  onChange={(e) => setSenha(e.target.value)}
                />
              </div>
            </div>
            <div className="flex w-full">
              <button
                type="submit"
                className="flex mt-2 items-center justify-center focus:outline-none text-white text-sm sm:text-base bg-primary hover:bg-primary-600 rounded py-2 w-full transition duration-150 ease-in"
              >
                <span className="mr-2">CADASTRAR</span>
                <span>
                  <svg
                    className="h-6 w-6"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </span>
              </button>
            </div>
          </form>
        </div>
        <div className="flex justify-center items-center mt-6">
          <Link
            href="/login"
            target=""
            className="inline-flex gap-2 items-center text-md text-center group"
          >
            <span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="w-7 h-7"
                viewBox="0 0 512 512"
              >
                <path
                  d="M192 176v-40a40 40 0 0140-40h160a40 40 0 0140 40v240a40 40 0 01-40 40H240c-22.09 0-48-17.91-48-40v-40"
                  fill="none"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="32"
                />
                <path
                  fill="none"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="32"
                  d="M288 336l80-80-80-80M80 256h272"
                />
              </svg>
            </span>
            <p className="group-hover:underline underline-offset-4">
              Tem uma conta?
              <span className="text-accent group-hover:underline decoration-accent">
                {" "}
                Entre
              </span>
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
}
