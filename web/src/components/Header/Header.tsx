"use client";
import Image from "next/image";
import Logo from "@/assets/logo/LogoWithoutText.svg";
import Link from "next/link";
import NavLink from "./NavLink";
import { usePathname, useRouter } from "next/navigation";
import { useRecoilState } from "recoil";
import { loggedState } from "@/app/recoilContextProvider";
import { IoPersonCircleOutline } from "react-icons/io5";
import { useEffect } from "react";

export default function Header() {
  const pathname = usePathname();
  const navigate = useRouter();
  const logout = () => {
    sessionStorage.removeItem("token-user");
    setIsLogged(false);
    if (pathname == "/software") {
      navigate.push("/");
    }
  };

  const [isLogged, setIsLogged] = useRecoilState(loggedState);

  useEffect(() => {
    if (
      sessionStorage.getItem("token-user") != null &&
      sessionStorage.getItem("token-user") != undefined
    ) {
      setIsLogged(true);
    } else {
      setIsLogged(false);
    }
  }, []);

  return (
    <header>
      <button
        type="button"
        className="text-md invisible !fixed bottom-5 right-5 z-50 rounded-full bg-primary p-4 font-medium uppercase leading-tight text-white opacity-0 shadow-lg transition-all duration-300 ease-in-out hover:bg-primary-600 hover:shadow-2xl focus:bg-azul-hover focus:shadow-lg focus:outline-none focus:ring-0 active:bg-azul-escuro active:shadow-2xl lg:bottom-10 lg:right-12"
        id="btn-back-to-top"
      >
        <svg
          aria-hidden="true"
          focusable="false"
          data-prefix="fas"
          className="w-4 h-4 lg:h-6 lg:w-6"
          role="img"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 448 512"
        >
          <path
            fill="currentColor"
            d="M34.9 289.5l-22.2-22.2c-9.4-9.4-9.4-24.6 0-33.9L207 39c9.4-9.4 24.6-9.4 33.9 0l194.3 194.3c9.4 9.4 9.4 24.6 0 33.9L413 289.4c-9.5 9.5-25 9.3-34.3-.4L264 168.6V456c0 13.3-10.7 24-24 24h-32c-13.3 0-24-10.7-24-24V168.6L69.2 289.1c-9.3 9.8-24.8 10-34.3.4z"
          ></path>
        </svg>
      </button>

      <nav
        id="navbar"
        className="fixed w-full duration-500 ease-in-out bg-background shadow-md z-50"
      >
        <div className="lg:px-16 xs:px-6 px-2 max-w-screen-xl justify-between flex flex-wrap items-center lg:py-0 py-2 mx-auto">
          <div className="flex flex-1 lg:flex-auto justify-between items-center py-2">
            <Link
              href="/"
              className="flex text-lg gap-2 justify-between items-center group"
            >
              <Image
                src={Logo}
                alt="Logo Manchester HealthCare"
                width={64}
                height={64}
                className="nav-link animate-spin pause group-hover:play"
                priority
              />
              <div>
                <p className="font-bold font-heading text-lg xs:text-xl">
                  MANCHESTER
                </p>
                <p className="font-heading text-base xs:text-lg tracking-widest">
                  HEALTHCARE
                </p>
              </div>
            </Link>
          </div>
          <label
            htmlFor="menu-toggle"
            className="cursor-pointer ml-2 order-3 lg:hidden block"
          >
            <svg
              className="fill-current text-gray-900"
              xmlns="http://www.w3.org/2000/svg"
              width={32}
              height={32}
              viewBox="0 0 20 20"
            >
              <title>menu</title>
              <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
            </svg>
          </label>
          <input className="hidden" type="checkbox" id="menu-toggle" />
          <div
            className="hidden lg:flex order-4 lg:items-center lg:w-auto w-full"
            id="menu"
          >
            <ul className="text-xl lg:absolute lg:top-1/2 lg:left-1/2 lg:transform lg:-translate-y-1/2 lg:-translate-x-1/2 text-center items-center gap-x-5 pt-4 md:gap-x-4 lg:text-lg lg:flex  lg:pt-0">
              <li className="py-2 lg:py-0 ">
                <NavLink href="/" name="Home" />
              </li>
              <li className="text-text-500 hidden lg:block">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  stroke="currentColor"
                  className="w-4 h-4 current-fill"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 5v0m0 7v0m0 7v0m0-13a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"
                  />
                </svg>
              </li>
              <li className="py-2 lg:py-0 ">
                <NavLink href="/contato" name="Contato" />
              </li>
              {isLogged && (
                <>
                  <li className="text-text-500 hidden lg:block">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      stroke="currentColor"
                      className="w-4 h-4 current-fill"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 5v0m0 7v0m0 7v0m0-13a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"
                      />
                    </svg>
                  </li>
                  <li className="py-2 lg:py-0 ">
                    <NavLink href="/software" name="Software" />
                  </li>
                </>
              )}
            </ul>
          </div>
          {!isLogged ? (
            <>
              <Link
                className="hidden lg:inline-block lg:ml-auto lg:mr-3 py-2 px-6 bg-secondary hover:bg-secondary-200 text-base text-gray-900 font-bold rounded-lg transition duration-200"
                href="/login"
              >
                Entrar
              </Link>
              <Link
                className="hidden lg:inline-block py-2 px-6 bg-primary hover:bg-primary-600 text-base text-white font-bold rounded-lg transition duration-200"
                href="/cadastro"
              >
                Cadastrar
              </Link>
              <Link
                href={"/login"}
                className="inline-flex lg:hidden order-1 items-center justify-center gap-x-1 lg:ml-auto lg:mr-3 py-2 px-4 lg:px-6 text-base text-gray-900 font-bold rounded-xl transition duration-200"
              >
                <IoPersonCircleOutline className="text-3xl" />
              </Link>
            </>
          ) : (
            // log out
            <>
              <button
                className="lg:inline-flex order-1 items-center justify-center gap-x-1 lg:ml-auto lg:mr-3 py-2 px-4 lg:px-6 bg-secondary hover:bg-secondary-200 text-base text-gray-900 font-bold rounded-lg transition duration-200"
                onClick={logout}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="ionicon w-6 h-6"
                  viewBox="0 0 512 512"
                >
                  <path
                    d="M304 336v40a40 40 0 01-40 40H104a40 40 0 01-40-40V136a40 40 0 0140-40h152c22.09 0 48 17.91 48 40v40M368 336l80-80-80-80M176 256h256"
                    fill="none"
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="32"
                  />
                </svg>
                <p className="hidden lg:block">Sair</p>
              </button>
            </>
          )}
        </div>
      </nav>
      <div className="h-20" />
    </header>
  );
}
