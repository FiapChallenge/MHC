import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  try {
    const {
      data_hora_classificacao,
      gravidade_id_gravidade,
      sinal_id_sinal,
      auditor_id_auditor,
      paciente_id_paciente,
    }: Classificacao = await request.json();
    const res = await fetch("http://127.0.0.1:8080/classificacao", {
      method: "POST",
      body: JSON.stringify({
        data_hora_classificacao,
        gravidade_id_gravidade,
        sinal_id_sinal,
        auditor_id_auditor,
        paciente_id_paciente,
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
