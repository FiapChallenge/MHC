import { useEffect, useRef, useState } from "react";
import { IoCloseOutline, IoInformationCircleOutline } from "react-icons/io5";

export default function Notification({
  nome,
  descricao,
  Icon = IoInformationCircleOutline,
  size = "w-16 h-16",
  hidden = false,
  color = { bg: "bg-secondary-100", text: "text-secondary-800" },
}: NotificationProps) {
  const [close, setClose] = useState(false);
  const noti = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (close) {
      if (noti.current) {
        noti.current?.classList.add("hidden");
      }
    }
  }, [close]);

  return (
    <div
      ref={noti}
      className={`${
        color.bg
      } flex flex-col relative md:flex-row items-center border max-w-[910px] border-gray-400 ${
        color.text
      } px-5 py-3 rounded relative ${hidden ? "hidden" : ""}`}
      role="alert"
    >
      <Icon className={`inline-block shrink-0 ${size} ${size} md:mr-4`} />
      <div>
        <p className="font-bold font-heading text-center md:text-left mb-1 md:mb-0 xs:text-lg uppercase tracking-wide">
          {nome}
        </p>
        <p className="block sm:inline">{descricao}</p>
      </div>
      {/* close button */}
      <button
        type="button"
        className="absolute right-0 top-0 mt-3 mr-3"
        onClick={() => setClose(true)}
      >
        <IoCloseOutline className="w-6 h-6" />
      </button>
    </div>
  );
}
