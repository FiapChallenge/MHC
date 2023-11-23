import Image from "next/image";
import { IoLogoGithub, IoLogoLinkedin } from "react-icons/io5";

export default function Card({
  nome,
  descricao,
  funcao,
  imagem,
  redesSociais,
}: {
  nome: string;
  descricao: string;
  funcao: string;
  imagem: any;
  redesSociais: string[];
}) {
  return (
    <div className="max-w-md mx-auto my-10 bg-white rounded-2xl shadow-xl md:shadow-lg p-5 hover:shadow-2xl transition-all duration-500 ease-in-out">
      <Image
        className="rounded-full mx-auto w-48 h-48"
        src={imagem}
        alt="Profile picture"
      />
      <h2 className="text-center text-2xl font-bold font-heading mt-3">
        {nome}
      </h2>
      <p className="text-center text-gray-600 mt-1 underline underline-offset-4 decoration-accent">
        {funcao}
      </p>
      <div className="flex justify-center gap-x-8 mt-5">
        <a
          href={redesSociais[0]}
          className="text-primary transition-colors duration-300 hover:text-primary-600"
        >
          <IoLogoLinkedin className="w-8 h-8" />
        </a>
        <a
          href={redesSociais[1]}
          className="text-primary transition-colors duration-300 hover:text-primary-600"
        >
          <IoLogoGithub className="w-8 h-8" />
        </a>
      </div>

      <div className="mt-3">
        <div className="flex items-center gap-x-2">
          <span className="border-l-4 rounded border-l-accent h-7"></span>
          <h3 className="text-xl font-bold">Sobre</h3>
        </div>
        <p className="text-gray-600 mt-2">{descricao}</p>
      </div>
    </div>
  );
}
