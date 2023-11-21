package br.com.fiap.banco.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import br.com.fiap.banco.exception.IdNotFoundException;
import br.com.fiap.banco.model.Gravidade;

public class GravidadeDao extends GenericDao<Gravidade> {

    public GravidadeDao(Connection conn) {
        super(conn);
    }

    @Override
    protected String getTableName() {
        return "GRAVIDADE";
    }

    @Override
    public void cadastrar(Gravidade gravidade) throws SQLException {
        PreparedStatement stm = conn.prepareStatement(
                "INSERT INTO GRAVIDADE (id_gravidade, nome_gravidade, nome_cor, hexadecimal_cor) VALUES (GRAVIDADE_ID_SEQ.NEXTVAL, ?, ?, ?)");
        stm.setString(1, gravidade.getNomeGravidade());
        stm.setString(2, gravidade.getNomeCor());
        stm.setString(3, gravidade.getHexadecimalCor());

        stm.executeUpdate();
    }

    @Override
    protected Gravidade parse(ResultSet result) throws SQLException {
        int id = result.getInt("id_gravidade");
        String nomeGravidade = result.getString("nome_gravidade");
        String nomeCor = result.getString("nome_cor");
        String hexadecimalCor = result.getString("hexadecimal_cor");

        Gravidade gravidade = new Gravidade(id, nomeGravidade, nomeCor, hexadecimalCor);
        return gravidade;
    }

    @Override
    public void atualizar(Gravidade gravidade) throws SQLException, IdNotFoundException {
        PreparedStatement stm = conn.prepareStatement(
                "UPDATE GRAVIDADE SET nome_gravidade = ?, nome_cor = ?, hexadecimal_cor = ? WHERE id_gravidade = ?");
        stm.setString(1, gravidade.getNomeGravidade());
        stm.setString(2, gravidade.getNomeCor());
        stm.setString(3, gravidade.getHexadecimalCor());
        stm.setInt(4, gravidade.getId());

        int linha = stm.executeUpdate();
        if (linha == 0)
            throw new IdNotFoundException("Gravidade não encontrada para atualização");
    }

}
