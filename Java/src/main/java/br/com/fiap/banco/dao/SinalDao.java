package br.com.fiap.banco.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import br.com.fiap.banco.exception.IdNotFoundException;
import br.com.fiap.banco.model.Sinal;

public class SinalDao extends GenericDao<Sinal> {

    public SinalDao(Connection conn) {
        super(conn);
    };

    @Override
    protected String getTableName() {
        return "SINAL";
    }

    @Override
    public void cadastrar(Sinal sinal) throws SQLException {
        PreparedStatement stm = conn.prepareStatement(
                "INSERT INTO SINAL (id_sinal, nome, descricao) VALUES (SINAL_ID_SEQ.NEXTVAL, ?, ?)");
        stm.setString(1, sinal.getNome());
        stm.setString(2, sinal.getDescricao());

        stm.executeUpdate();
    }

    @Override
    protected Sinal parse(ResultSet result) throws SQLException {
        int id = result.getInt("id_sinal");
        String nome = result.getString("nome");
        String descricao = result.getString("descricao");

        Sinal sinal = new Sinal(id, nome, descricao);
        return sinal;
    }

    @Override
    public void atualizar(Sinal sinal) throws SQLException, IdNotFoundException {
        PreparedStatement stm = conn.prepareStatement(
                "UPDATE SINAL SET nome = ?, descricao = ? WHERE id_sinal = ?");
        stm.setString(1, sinal.getNome());
        stm.setString(2, sinal.getDescricao());
        stm.setInt(3, sinal.getId());

        int linha = stm.executeUpdate();
        if (linha == 0)
            throw new IdNotFoundException("Sinal não encontrado para atualização");
    }
}
