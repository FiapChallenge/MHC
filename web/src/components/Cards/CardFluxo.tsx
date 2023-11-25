import { selectedFluxoState } from "@/app/recoilContextProvider";
import classNames from "classnames";
import { IoInformationCircleOutline } from "react-icons/io5";
import { useRecoilState } from "recoil";

export default function CardFluxo({
  cor,
  sintomas,
  hidden = true,
  index: indexFluxo,
}: {
  cor: { bg: string; shadow: string };
  sintomas: string[];
  hidden?: boolean;
  index: number;
}) {
  const [selectedFluxo, setSelectedFluxo] = useRecoilState(selectedFluxoState);

  return (
    <li
      // className={`${
      // hidden ? "fadeOutDown" : "fadeInUp"
      // } flex-col h-full justify-center items-center`}
      className={classNames(
        `cursor-pointer flex-col justify-center items-center rounded-2xl overflow-hidden shadow-2xl ${cor.shadow}`,
        {
          fadeOutDown: hidden,
          fadeInUp: !hidden,
          "outline outline-4": selectedFluxo === indexFluxo,
        }
      )}
      onClick={() => {
        if (selectedFluxo === indexFluxo) {
          setSelectedFluxo(5);
          return;
        }
        setSelectedFluxo(indexFluxo);
      }}
    >
      <div className="md:h-full group rounded-2xl justify-center">
        <div className={`h-full ${cor.bg} md:max-w-md`}>
          <ul className="text-white min-h-[16rem] flex flex-col h-full justify-center text-center text-xl">
            {sintomas.map((sintoma, index) =>
              index % 2 === 0 ? (
                <li
                  key={index}
                  className="bg-white relative flex h-full justify-center items-center grow bg-opacity-0 "
                >
                  <span className="grow p-2">{sintoma}</span>
                  <div
                    className={`bg-black absolute right-0 transition-all duration-500 translate-x-full group-hover:translate-x-0 bg-opacity-40 px-2 h-full flex justify-center items-center`}
                  >
                    <IoInformationCircleOutline className={`w-6 h-6`} />
                  </div>
                </li>
              ) : (
                <li
                  key={index}
                  className="bg-white relative flex h-full justify-center items-center grow bg-opacity-20"
                >
                  <span className="grow p-2">{sintoma}</span>
                  <div
                    className={`bg-black absolute right-0 transition-all duration-500 translate-x-full group-hover:translate-x-0 bg-opacity-60 px-2 h-full flex justify-center items-center`}
                  >
                    <IoInformationCircleOutline className={`w-6 h-6`} />
                  </div>
                </li>
              )
            )}
          </ul>
        </div>
      </div>
    </li>
  );
}
