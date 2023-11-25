"use client";
import Image from "next/image";
import Link from "next/link";
import { IoArrowForwardOutline } from "react-icons/io5";
import DoctorVector from "@/assets/img/Doctors-amico.svg";
import { useRecoilState } from "recoil";
import { loggedState } from "./recoilContextProvider";

export default function Home() {
  const [isLogged, setIsLogged] = useRecoilState(loggedState);
  return (
    <>
      <section className="bg-wite flex items-center justify-center min-h-[60vh] bg-background-50 ">
        <div className="grid max-w-screen-xl px-4 py-8 mx-auto gap-y-8 lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
          <div className="mr-auto order-2 lg:order-1 place-self-center lg:col-span-7">
            <h1 className="max-w-2xl mb-4 text-4xl font-bold font-heading leading-none md:text-5xl xl:text-6xl ">
              Priorizando Vidas com Eficiência
            </h1>
            <p className="max-w-2xl mb-6 font-light font-body text-text-600 lg:mb-8 md:text-lg lg:text-xl ">
              Descubra como o protocolo de Manchester e o nosso software agiliza
              a Triagem de pacientes para melhor atendimento.
            </p>
            {isLogged ? (
              <Link
                href="/software"
                className="inline-flex items-center justify-center px-5 py-3  mr-3 text-lg text-white  text-center  border font-bold bg-primary hover:bg-primary-600  rounded-lg  transition-all duration-300"
              >
                Software
                <IoArrowForwardOutline className="w-6 h-6 ml-2 -mr-1" />
              </Link>
            ) : (
              <>
                <Link
                  href="/cadastro"
                  className="inline-flex items-center text-lg justify-center px-5 py-3  mr-3  text-base text-white  text-center  border font-bold bg-primary hover:bg-primary-600  rounded-lg  transition-all duration-300"
                >
                  Cadastrar
                </Link>
                <Link
                  href="/login"
                  className="inline-flex items-center text-lg justify-center px-5 py-3 text-base text-center font-bold bg-secondary hover:bg-secondary-200 text-text rounded-lg  transition-all duration-300"
                >
                  Entrar
                  <IoArrowForwardOutline className="w-6 h-6 ml-2 -mr-1" />
                </Link>
              </>
            )}
          </div>
          <div className="order-1 lg:order-2 lg:mt-0 place-self-center lg:col-span-5 lg:flex">
            {/* <img
              src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/hero/phone-mockup.png"
              alt="mockup"
            /> */}
            <Image
              className="float"
              src={DoctorVector}
              alt="Vetor de doutores"
              width={500}
              height={500}
            />
          </div>
        </div>
      </section>
    </>
  );
}
