package br.com.fiap.banco.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import br.com.fiap.banco.exception.IdNotFoundException;
import br.com.fiap.banco.model.Auditor;

public class AuditorDao extends GenericDao<Auditor> {

    public AuditorDao(Connection conn) {
        super(conn);
    }

    @Override
    protected String getTableName() {
        return "AUDITOR";
    }

    @Override
    public void cadastrar(Auditor auditor) throws SQLException {
        PreparedStatement stm = conn.prepareStatement(
                "INSERT INTO AUDITOR (id_auditor, nome, email, senha, cpf, crm, coren, especialidade) VALUES (AUDITOR_ID_SEQ.NEXTVAL, ?, ?, ?, ?, ?, ?, ?)");
        stm.setString(1, auditor.getNome());
        stm.setString(2, auditor.getEmail());
        stm.setString(3, auditor.getSenha());
        stm.setString(4, auditor.getCpf());
        stm.setString(5, auditor.getCrm());
        stm.setString(6, auditor.getCoren());
        stm.setString(7, auditor.getEspecialidade());

        stm.executeUpdate();
    }

    @Override
    protected Auditor parse(ResultSet result) throws SQLException {
        int id = result.getInt("id_auditor");
        String nome = result.getString("nome");
        String email = result.getString("email");
        String senha = result.getString("senha");
        String cpf = result.getString("cpf");
        String crm = result.getString("crm");
        String coren = result.getString("coren");
        String especialidade = result.getString("especialidade");

        Auditor auditor = new Auditor(id, nome, email, senha, cpf, crm, coren, especialidade);
        return auditor;
    }

    @Override
    public void atualizar(Auditor auditor) throws SQLException, IdNotFoundException {
        PreparedStatement stm = conn.prepareStatement(
                "UPDATE AUDITOR SET nome = ?, cpf = ?, crm = ?, coren = ?, especialidade = ? WHERE id_auditor = ?");
        stm.setString(1, auditor.getNome());
        stm.setString(2, auditor.getCpf());
        stm.setString(3, auditor.getCrm());
        stm.setString(4, auditor.getCoren());
        stm.setString(5, auditor.getEspecialidade());
        stm.setInt(6, auditor.getId());

        int linha = stm.executeUpdate();
        if (linha == 0)
            throw new IdNotFoundException("Auditor não encontrado para atualização");
    }

    public Auditor pesquisarPorEmail(String email) throws SQLException, ClassNotFoundException {
        PreparedStatement stm = conn.prepareStatement("SELECT * FROM AUDITOR WHERE email = ?");
        stm.setString(1, email);
        ResultSet result = stm.executeQuery();
        Auditor auditor = null;
        if (result.next()) {
            auditor = new AuditorDao(conn).parse(result);
        }
        conn.close();
        return auditor;
    }
}
