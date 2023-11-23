"use client";
import Image from "next/image";
import Logo from "@/assets/logo/LogoWithoutText.svg";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { loggedState } from "../recoilContextProvider";
import { useRecoilState } from "recoil";
import { IoEyeOffOutline, IoEyeOutline } from "react-icons/io5";

export default function Login() {
  const navigate = useRouter();
  const [auditores, setAuditores] = useState<Auditor[]>([]);

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");

  const [isLogged, setIsLogged] = useRecoilState(loggedState);

  useEffect(() => {
    const getAuditores = async () => {
      try {
        const res = await fetch("http://localhost:3000/api/auditor", {
          cache: "no-store",
        });
        const data: Auditor[] = await res.json();
        setAuditores(data);
      } catch (error) {
        console.log(error);
      }
    };
    getAuditores();
  }, []);

  const submitHandle = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (email === "admin@admin" && senha === "admin") {
      const token = JSON.stringify({ email: "admin", senha: "admin" });

      sessionStorage.setItem("token-user", token);

      process.env.NEXT_PUBLIC_TOKEN_USER = token;

      setIsLogged(true);

      navigate.push("/software");
      return;
    }
    const auditor = auditores.find((auditor) => auditor.email === email);
    if (auditor) {
      if (auditor.senha === senha) {
        const token = JSON.stringify(auditor);

        sessionStorage.setItem("token-user", token);

        process.env.NEXT_PUBLIC_TOKEN_USER = token;

        setIsLogged(true);

        navigate.push("/software");
      } else {
        alert("Senha incorreta!");
      }
    } else {
      alert("Email incorreto!");
    }
  };

  const [showPassword, setShowPassword] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="py-28 flex flex-col items-center justify-center bg-background-50 px-4">
      <div className="flex flex-col bg-white shadow-xl px-4 sm:px-6 md:px-8 lg:px-10 py-8 rounded-2xl w-full max-w-md">
        <div className="flex justify-center items-center pb-4">
          <Image
            src={Logo}
            alt="Logo Manchester HealthCare"
            width={64}
            height={64}
            className="animate-spin-slow pause hover:play"
          />
        </div>
        <div className="font-bold font-heading self-center text-xl sm:text-2xl uppercase text-text">
          Entrar no MHC
        </div>
        <div className="mt-6">
          <form onSubmit={submitHandle}>
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
                  required
                  className="text-sm sm:text-base placeholder-gray-500 pl-10 pr-4 rounded-lg border border-gray-400 w-full py-2 focus:outline-none focus:border-accent"
                  placeholder="Endereço de e-mail"
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
                  className="cursor-pointer inline-flex items-center justify-center absolute right-0 top-0 h-full w-10 text-gray-400"
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
                <span className="mr-2">LOGIN</span>
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
            href="/cadastro"
            target=""
            className="inline-flex gap-2 items-center text-md text-center group"
          >
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
                <path d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </span>
            <p className="group-hover:underline underline-offset-4">
              Não tem uma conta?
              <span className="text-accent group-hover:underline decoration-accent">
                {" "}
                Inscreva-se
              </span>
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
}
