"use client";
import classNames from "classnames";
import { usePathname } from "next/dist/client/components/navigation";
import Link from "next/link";

export default function NavLink(props: { href: string; name: string }) {
  const pathname = usePathname();

  return (
    <Link
      href={props.href}
      className={classNames("transition-colors hover:text-primary", {
        "text-primary": pathname === props.href,
      })}
    >
      {props.name}
    </Link>
  );
}
