import Image from "next/image";
import { IoLogoGithub, IoLogoLinkedin, IoLogoTwitter } from "react-icons/io5";
import AsteriuzProfile from "@/assets/cards/asteriuz.webp";
import GriblProfile from "@/assets/cards/gribl.jpg";
import SouzaProfile from "@/assets/cards/souza.jpg";
import GabsProfile from "@/assets/cards/gabs.jpg";
import CardProfile from "@/components/Cards/CardProfile";

export default function Contato() {
  return (
    <section className="flex justify-center items-center flex-col bg-background-50 px-4 pb-10">
      <h1 className="font-bold font-heading text-4xl uppercase tracking-wider mb-2 mt-12 text-center">
        Conheça a <span className="fancy">Equipe</span>
      </h1>
      <div className="min-h-[60vh] flex justify-center">
        <div className="grid lg:grid-cols-2 gap-x-24 lg:gap-y-8">
          <CardProfile
            nome="Augusto Barcelos Barros"
            descricao="Bom dia! Eu sou Augusto Barcelos Barros e sou apaixonado por tecnologia desde a infância.
Meu principal hobby é desenvolver programas que me auxiliem em atividades cotidianas e diminuam o tempo para realizar tarefas repetitivas"
            imagem={AsteriuzProfile}
            redesSociais={[
              "https://www.linkedin.com/in/asteriuz/",
              "https://github.com/Asteriuz",
            ]}
            funcao="Diretor de Tecnologia"
          />
          {/* Gabriel Gribl de Carvalho (Diretor de Projetos e Inovação)  */}
          <CardProfile
            nome="Gabriel Gribl de Carvalho"
            descricao="Comunicativo, sociável, produtivo e organizado. Aprendendo cada dia mais sobre programação, inteligência artificial, inovação e tecnologias. Sempre aberto para novas experiências e desafios"
            imagem={GriblProfile}
            redesSociais={[
              "https://www.linkedin.com/in/gabriel-gribl-302799243/",
              "https://github.com/gribl88",
            ]}
            funcao="Diretor de Projetos e Inovação"
          />
          <CardProfile
            nome="Gabriel Souza"
            descricao="Olá! Meu nome é Gabriel Souza de Queiroz e sou um jovem profissional em desenvolvimento na área de tecnologia. Atualmente, trabalho como jovem aprendiz em Assuntos Regulatórios na Sanofi Medley"
            imagem={SouzaProfile}
            redesSociais={[
              "https://www.linkedin.com/in/gabriel-souza-039a05202/",
              "https://github.com/GabrielSouzaQ",
            ]}
            funcao="Diretor Adm. Financeiro"
          />
          <CardProfile
            nome="Gabriela Zanotto Alves "
            descricao="Sou uma pessoa que ama aprender, atualmente estou cursando análise e desenvolvimento de sistemas na FIAP, aprendo rápido e gosto de trabalhar no ramo"
            imagem={GabsProfile}
            redesSociais={[
              "https://www.linkedin.com/in/gabriela-zanotto-385a61211/",
              "https://github.com/GabsBecca",
            ]}
            funcao="Diretora de Marketing"
          />
        </div>
      </div>
    </section>
  );
}
