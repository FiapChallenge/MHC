import { NextResponse } from "next/server";

export async function GET() {
  try {
    const res = await fetch("http://127.0.0.1:8080/sinal", {
      cache: "no-store",
    });
    const data: Sinal[] = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json([]);
  }
}
