package br.com.fiap.banco.model;

import java.util.Objects;

public class Sinal {

    private int id;
    private String nome;
    private String descricao;

    public Sinal() {
    }

    public Sinal(String nome, String descricao) {
        this.nome = nome;
        this.descricao = descricao;
    }

    public Sinal(int idSinal, String nome, String descricao) {
        this.id = idSinal;
        this.nome = nome;
        this.descricao = descricao;
    }

    public int getId() {
        return id;
    }

    public void setId(int idSinal) {
        this.id = idSinal;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getDescricao() {
        return descricao;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;
        Sinal sinal = (Sinal) o;
        return id == sinal.id &&
                Objects.equals(nome, sinal.nome) &&
                Objects.equals(descricao, sinal.descricao);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, nome, descricao);
    }

    @Override
    public String toString() {
        return "Sinal{" +
                "idSinal=" + id +
                ", nome='" + nome + '\'' +
                ", descricao='" + descricao + '\'' +
                '}';
    }
}
