import { NextResponse } from "next/server";

export async function GET() {
  try {
    const res = await fetch("http://127.0.0.1:8080/paciente", {
      cache: "no-store",
    });
    const data: Paciente[] = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.error();
  }
}

export async function POST(request: Request) {
  try {
    const {
      nome,
      cpf,
      rg,
      data_hora_entrada,
      data_hora_saida,
      sexo,
      idade,
      altura,
      peso,
    } = await request.json();
    const res = await fetch("http://127.0.0.1:8080/paciente", {
      method: "POST",
      body: JSON.stringify({
        nome,
        cpf,
        rg,
        data_hora_entrada,
        data_hora_saida,
        sexo,
        idade,
        altura,
        peso,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    const data: Paciente = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.error();
  }
}
