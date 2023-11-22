"use client";
import { useEffect } from "react";

export default function page() {
  useEffect(() => {
    if (
      sessionStorage.getItem("token-user") != null &&
      sessionStorage.getItem("token-user") != undefined
    ) {
      // console.log("token-user: " + sessionStorage.getItem("token-user"));
    } else {
      window.location.href = "/login";
    }
  });

  return <div>Teste</div>;
}
