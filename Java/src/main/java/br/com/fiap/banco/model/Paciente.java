package br.com.fiap.banco.model;

import java.util.Date;

import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import br.com.fiap.banco.serializer.CustomDateSerializer;

public class Paciente {

    private int id;
    private String nome;
    private String cpf;
    private String rg;
    @JsonSerialize(using = CustomDateSerializer.class)
    private Date dataHoraEntrada;
    @JsonSerialize(using = CustomDateSerializer.class)
    private Date dataHoraSaida;
    private String sexo;
    private Integer idade;
    private Integer altura;
    private Integer peso;

    public Paciente() {
    }

    public Paciente(String nome, String cpf, String rg, Date dataHoraEntrada,
            Date dataHoraSaida, String sexo, Integer idade, Integer altura, Integer peso) {
        this.nome = nome;
        this.cpf = cpf;
        this.rg = rg;
        this.dataHoraEntrada = dataHoraEntrada;
        this.dataHoraSaida = dataHoraSaida;
        this.sexo = sexo;
        this.idade = idade;
        this.altura = altura;
        this.peso = peso;
    }

    public Paciente(int idPaciente, String nome, String cpf, String rg, Date dataHoraEntrada,
            Date dataHoraSaida, String sexo, Integer idade, Integer altura, Integer peso) {
        this.id = idPaciente;
        this.nome = nome;
        this.cpf = cpf;
        this.rg = rg;
        this.dataHoraEntrada = dataHoraEntrada;
        this.dataHoraSaida = dataHoraSaida;
        this.sexo = sexo;
        this.idade = idade;
        this.altura = altura;
        this.peso = peso;
    }

    public int getId() {
        return id;
    }

    public void setId(int idPaciente) {
        this.id = idPaciente;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getCpf() {
        return cpf;
    }

    public void setCpf(String cpf) {
        this.cpf = cpf;
    }

    public String getRg() {
        return rg;
    }

    public void setRg(String rg) {
        this.rg = rg;
    }

    public Date getDataHoraEntrada() {
        return dataHoraEntrada;
    }

    public void setDataHoraEntrada(Date dataHoraEntrada) {
        this.dataHoraEntrada = dataHoraEntrada;
    }

    public Date getDataHoraSaida() {
        return dataHoraSaida;
    }

    public void setDataHoraSaida(Date dataHoraSaida) {
        this.dataHoraSaida = dataHoraSaida;
    }

    public String getSexo() {
        return sexo;
    }

    public void setSexo(String sexo) {
        this.sexo = sexo;
    }

    public Integer getIdade() {
        return idade;
    }

    public void setIdade(Integer idade) {
        this.idade = idade;
    }

    public Integer getAltura() {
        return altura;
    }

    public void setAltura(Integer altura) {
        this.altura = altura;
    }

    public Integer getPeso() {
        return peso;
    }

    public void setPeso(Integer peso) {
        this.peso = peso;
    }

    @Override
    public String toString() {
        return "Paciente{" +
                "idPaciente=" + id +
                ", nome='" + nome + '\'' +
                ", cpf='" + cpf + '\'' +
                ", rg='" + rg + '\'' +
                ", dataHoraEntrada=" + dataHoraEntrada +
                ", dataHoraSaida=" + dataHoraSaida +
                ", sexo='" + sexo + '\'' +
                ", idade=" + idade +
                ", altura=" + altura +
                ", peso=" + peso +
                '}';
    }
}
