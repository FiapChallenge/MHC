import Link from "next/link";
import Logo from "@/assets/logo/LogoWithoutText.svg";
import Image from "next/image";

export default function NotFound() {
  return (
    <div className="mb-4 min-h-[60vh] bg-background-50 flex items-center justify-center font-heading">
      <div className="flex items-center justify-center flex-col gap-y-2">
        <h1 className="text-6xl font-bold text-center flex gap-1 group">
          4
          <Image
            src={Logo}
            alt="Logo Manchester HealthCare"
            width={64}
            height={64}
            className="animate-spin-slow grayscale group-hover:grayscale-0 transition-all duration-500"
          />
          4
        </h1>
        <h2 className="text-3xl font-bold text-center">
          Oops! Página não encontrada
        </h2>
        <Link
          className="mt-8 p-4 rounded-2xl bg-azul-claro text-primary text-2xl"
          href="/"
        >
          Voltar para a página inicial
        </Link>
      </div>
    </div>
  );
}
