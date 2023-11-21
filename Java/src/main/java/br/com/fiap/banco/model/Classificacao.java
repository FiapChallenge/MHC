package br.com.fiap.banco.model;

import java.util.Date;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import br.com.fiap.banco.serializer.CustomDateSerializer;

public class Classificacao {
    private int id;
    @JsonSerialize(using = CustomDateSerializer.class)
    private Date dataHoraClassificacao;
    private Gravidade gravidade;
    private Sinal sinal;
    private Paciente paciente;
    private Auditor auditor;

    public Classificacao() {
    }

    public Classificacao(Date dataHoraClassificacao, Gravidade gravidade, Sinal sinal, Paciente paciente,
            Auditor auditor) {
        this.dataHoraClassificacao = dataHoraClassificacao;
        this.gravidade = gravidade;
        this.sinal = sinal;
        this.paciente = paciente;
        this.auditor = auditor;
    }

    public Classificacao(int id, Date dataHoraClassificacao, Gravidade gravidade, Sinal sinal, Paciente paciente,
            Auditor auditor) {
        this.id = id;
        this.dataHoraClassificacao = dataHoraClassificacao;
        this.gravidade = gravidade;
        this.sinal = sinal;
        this.paciente = paciente;
        this.auditor = auditor;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public Date getDataHoraClassificacao() {
        return dataHoraClassificacao;
    }

    public void setDataHoraClassificacao(Date dataHoraClassificacao) {
        this.dataHoraClassificacao = dataHoraClassificacao;
    }

    public Gravidade getGravidade() {
        return gravidade;
    }

    public void setGravidade(Gravidade gravidade) {
        this.gravidade = gravidade;
    }

    public Sinal getSinal() {
        return sinal;
    }

    public void setSinal(Sinal sinal) {
        this.sinal = sinal;
    }

    public Paciente getPaciente() {
        return paciente;
    }

    public void setPaciente(Paciente paciente) {
        this.paciente = paciente;
    }

    public Auditor getAuditor() {
        return auditor;
    }

    public void setAuditor(Auditor auditor) {
        this.auditor = auditor;
    }

    @Override
    public String toString() {
        return "Classificacao{" +
                "dataHoraClassificacao=" + dataHoraClassificacao +
                ", gravidade=" + gravidade +
                ", sinal=" + sinal +
                ", paciente=" + paciente +
                ", auditor=" + auditor +
                '}';
    }
}
