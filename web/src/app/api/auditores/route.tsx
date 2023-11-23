import { NextResponse } from "next/server";

export async function GET() {
  try {
    const res = await fetch("http://127.0.0.1:8080/auditor", {
      cache: "no-store",
    });
    const data: Auditor[] = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json([]);
  }
}

export async function POST(request: Request) {
  try {
    const { nome, email, senha } = await request.json();
    const res = await fetch("http://127.0.0.1:8080/auditor", {
      method: "POST",
      body: JSON.stringify({ nome, email, senha }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    const data: Auditor = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.error();
  }
}
