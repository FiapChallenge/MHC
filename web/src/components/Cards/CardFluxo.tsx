import { IoNuclear } from "react-icons/io5";

export default function CardFluxo({
  cor,
  sintomas,
  hidden = true,
}: {
  cor: { bg: string; shadow: string };
  sintomas: string[];
  hidden?: boolean;
}) {
  return (
    <li
      className={`${
        hidden ? "fadeOutDown" : "fadeInUp"
      } flex-col h-full justify-center items-center`}
    >
      <div className="md:h-full  justify-center">
        <div
          className={`rounded-xl h-full shadow-2xl ${cor.bg} ${cor.shadow} md:max-w-md`}
        >
          <ul className="text-white min-h-[14rem] flex flex-col h-full justify-center text-center text-xl">
            {sintomas.map((sintoma, index) =>
              index % 2 === 0 ? (
                <li
                  key={index}
                  className="bg-white flex justify-center items-center grow bg-opacity-0 p-2"
                >
                  {sintoma}
                </li>
              ) : (
                <li
                  key={index}
                  className="bg-white  flex justify-center items-center grow bg-opacity-10 p-2"
                >
                  {sintoma}
                </li>
              )
            )}
          </ul>
        </div>
      </div>
    </li>
  );
}
