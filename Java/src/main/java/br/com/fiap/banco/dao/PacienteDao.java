package br.com.fiap.banco.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import br.com.fiap.banco.exception.IdNotFoundException;
import br.com.fiap.banco.model.Paciente;

public class PacienteDao extends GenericDao<Paciente> {

    public PacienteDao(Connection conn) {
        super(conn);
    }

    @Override
    protected String getTableName() {
        return "PACIENTE";
    }

    @Override
    public void cadastrar(Paciente paciente) throws SQLException {
        PreparedStatement stm = conn.prepareStatement(
                "INSERT INTO PACIENTE (id_paciente, nome, cpf, rg, data_hora_entrada, data_hora_saida, sexo, idade, altura, peso) VALUES (PACIENTE_ID_SEQ.NEXTVAL, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
        stm.setString(1, paciente.getNome());
        stm.setString(2, paciente.getCpf());
        stm.setString(3, paciente.getRg());
        stm.setDate(4, new java.sql.Date(paciente.getDataHoraEntrada().getTime()));
        stm.setDate(5, new java.sql.Date(paciente.getDataHoraSaida().getTime()));
        stm.setString(6, paciente.getSexo());
        stm.setInt(7, paciente.getIdade());
        stm.setInt(8, paciente.getAltura());
        stm.setInt(9, paciente.getPeso());

        stm.executeUpdate();
    }

    @Override
    protected Paciente parse(ResultSet result) throws SQLException {
        int id = result.getInt("id_paciente");
        String nome = result.getString("nome");
        String cpf = result.getString("cpf");
        String rg = result.getString("rg");
        java.util.Date dataHoraEntrada = result.getDate("data_hora_entrada");
        java.util.Date dataHoraSaida = result.getDate("data_hora_saida");
        String sexo = result.getString("sexo");
        int idade = result.getInt("idade");
        int altura = result.getInt("altura");
        int peso = result.getInt("peso");

        Paciente paciente = new Paciente(id, nome, cpf, rg, dataHoraEntrada, dataHoraSaida, sexo, idade, altura, peso);
        return paciente;
    }

    @Override
    public void atualizar(Paciente paciente) throws SQLException, IdNotFoundException {
        PreparedStatement stm = conn.prepareStatement(
                "UPDATE PACIENTE SET nome = ?, cpf = ?, rg = ?, data_hora_entrada = ?, data_hora_saida = ?, sexo = ?, idade = ?, altura = ?, peso = ? WHERE id_paciente = ?");
        stm.setString(1, paciente.getNome());
        stm.setString(2, paciente.getCpf());
        stm.setString(3, paciente.getRg());
        stm.setDate(4, new java.sql.Date(paciente.getDataHoraEntrada().getTime()));
        stm.setDate(5, new java.sql.Date(paciente.getDataHoraSaida().getTime()));
        stm.setString(6, paciente.getSexo());
        stm.setInt(7, paciente.getIdade());
        stm.setInt(8, paciente.getAltura());
        stm.setInt(9, paciente.getPeso());
        stm.setInt(10, paciente.getId());

        int linha = stm.executeUpdate();
        if (linha == 0)
            throw new IdNotFoundException("Paciente não encontrado para atualização");
    }

}
