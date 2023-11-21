package br.com.fiap.banco.model;

public class Gravidade {

    private int id;
    private String nomeGravidade;
    private String nomeCor;
    private String hexadecimalCor;

    public Gravidade() {
    }

    public Gravidade(String nomeGravidade, String nomeCor, String hexadecimalCor) {
        this.nomeGravidade = nomeGravidade;
        this.nomeCor = nomeCor;
        this.hexadecimalCor = hexadecimalCor;
    }

    public Gravidade(int idGravidade, String nomeGravidade, String nomeCor, String hexadecimalCor) {
        this.id = idGravidade;
        this.nomeGravidade = nomeGravidade;
        this.nomeCor = nomeCor;
        this.hexadecimalCor = hexadecimalCor;
    }

    public int getId() {
        return id;
    }

    public void setId(int idGravidade) {
        this.id = idGravidade;
    }

    public String getNomeGravidade() {
        return nomeGravidade;
    }

    public void setNomeGravidade(String nomeGravidade) {
        this.nomeGravidade = nomeGravidade;
    }

    public String getNomeCor() {
        return nomeCor;
    }

    public void setNomeCor(String nomeCor) {
        this.nomeCor = nomeCor;
    }

    public String getHexadecimalCor() {
        return hexadecimalCor;
    }

    public void setHexadecimalCor(String hexadecimalCor) {
        this.hexadecimalCor = hexadecimalCor;
    }

    @Override
    public String toString() {
        return "Gravidade{" +
                "idGravidade=" + id +
                ", nomeGravidade='" + nomeGravidade + '\'' +
                ", nomeCor='" + nomeCor + '\'' +
                ", hexadecimalCor='" + hexadecimalCor + '\'' +
                '}';
    }
}
