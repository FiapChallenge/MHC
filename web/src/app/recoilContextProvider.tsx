"use client";
import { RecoilRoot, atom } from "recoil";

export const loggedState = atom({
  key: "Logged",
  default: false,
});

export default function RecoilContextProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return <RecoilRoot>{children}</RecoilRoot>;
}
