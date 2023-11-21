package br.com.fiap.banco.model;

public class Auditor {

    private int id;
    private String nome;
    private String cpf;
    private String crm;
    private String coren;
    private String especialidade;

    public Auditor() {
    }

    public Auditor(String nome, String cpf, String crm, String coren, String especialidade) {
        this.nome = nome;
        this.cpf = cpf;
        this.crm = crm;
        this.coren = coren;
        this.especialidade = especialidade;
    }

    public Auditor(int idAuditor, String nome, String cpf, String crm, String coren, String especialidade) {
        this.id = idAuditor;
        this.nome = nome;
        this.cpf = cpf;
        this.crm = crm;
        this.coren = coren;
        this.especialidade = especialidade;
    }

    public int getId() {
        return id;
    }

    public void setId(int idAuditor) {
        this.id = idAuditor;
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

    public String getCrm() {
        return crm;
    }

    public void setCrm(String crm) {
        this.crm = crm;
    }

    public String getCoren() {
        return coren;
    }

    public void setCoren(String coren) {
        this.coren = coren;
    }

    public String getEspecialidade() {
        return especialidade;
    }

    public void setEspecialidade(String especialidade) {
        this.especialidade = especialidade;
    }

    @Override
    public String toString() {
        return "Auditor{" +
                "idAuditor=" + id +
                ", nome='" + nome + '\'' +
                ", cpf='" + cpf + '\'' +
                ", crm='" + crm + '\'' +
                ", coren='" + coren + '\'' +
                ", especialidade='" + especialidade + '\'' +
                '}';
    }
}