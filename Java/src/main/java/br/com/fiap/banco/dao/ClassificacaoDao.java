package br.com.fiap.banco.dao;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;

import br.com.fiap.banco.exception.IdNotFoundException;
import br.com.fiap.banco.model.Auditor;
import br.com.fiap.banco.model.Classificacao;
import br.com.fiap.banco.model.Gravidade;
import br.com.fiap.banco.model.Paciente;
import br.com.fiap.banco.model.Sinal;

import java.sql.PreparedStatement;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class ClassificacaoDao extends GenericDao<Classificacao> {

    public ClassificacaoDao(Connection conn) {
        super(conn);
    }

    @Override
    protected String getTableName() {
        return "CLASSIFICACAO";
    }

    @Override
    public void cadastrar(Classificacao classificacao) throws SQLException {
        String sql = "INSERT INTO " + getTableName() +
                " (data_hora_classificacao, gravidade_id_gravidade, sinal_id_sinal, paciente_id_paciente, auditor_id_auditor) "
                +
                "VALUES (?, ?, ?, ?, ?)";

        try (PreparedStatement stm = conn.prepareStatement(sql)) {
            stm.setDate(1, new java.sql.Date(classificacao.getDataHoraClassificacao().getTime()));
            stm.setInt(2, classificacao.getGravidade().getId());
            stm.setInt(3, classificacao.getSinal().getId());
            stm.setInt(4, classificacao.getPaciente().getId());
            stm.setInt(5, classificacao.getAuditor().getId());

            stm.executeUpdate();
        }
    }

    public Classificacao parse(ResultSet result) throws SQLException {
        int id = result.getInt("id_classificacao");
        Date dataHoraClassificacao = result.getDate("data_hora_classificacao");
        int idGravidade = result.getInt("gravidade_id_gravidade");
        int idSinal = result.getInt("sinal_id_sinal");
        int idPaciente = result.getInt("paciente_id_paciente");
        int idAuditor = result.getInt("auditor_id_auditor");

        GravidadeDao gravidadeDao = new GravidadeDao(conn);
        Gravidade gravidade = null;
        try {
            gravidade = gravidadeDao.pesquisar(idGravidade);
        } catch (IdNotFoundException e) {
            e.printStackTrace();
        }

        SinalDao sinalDao = new SinalDao(conn);
        Sinal sinal = null;
        try {
            sinal = sinalDao.pesquisar(idSinal);
        } catch (IdNotFoundException e) {
            e.printStackTrace();
        }

        PacienteDao pacienteDao = new PacienteDao(conn);
        Paciente paciente = null;
        try {
            paciente = pacienteDao.pesquisar(idPaciente);
        } catch (IdNotFoundException e) {
            e.printStackTrace();
        }

        AuditorDao auditorDao = new AuditorDao(conn);
        Auditor auditor = null;
        try {
            auditor = auditorDao.pesquisar(idAuditor);
        } catch (IdNotFoundException e) {
            e.printStackTrace();
        }

        Classificacao classificacao = new Classificacao(id, dataHoraClassificacao, gravidade, sinal, paciente, auditor);
        return classificacao;
    }

    @Override
    public void atualizar(Classificacao classificacao) throws SQLException {
        String sql = "UPDATE " + getTableName() +
                " SET data_hora_classificacao = ?, gravidade_id_gravidade = ?, sinal_id_sinal = ?, " +
                "paciente_id_paciente = ?, auditor_id_auditor = ? WHERE id_classificacao = ?";

        try (PreparedStatement stm = conn.prepareStatement(sql)) {
            stm.setDate(1, new java.sql.Date(classificacao.getDataHoraClassificacao().getTime()));
            stm.setInt(2, classificacao.getGravidade().getId());
            stm.setInt(3, classificacao.getSinal().getId());
            stm.setInt(4, classificacao.getPaciente().getId());
            stm.setInt(5, classificacao.getAuditor().getId());
            stm.setInt(6, classificacao.getId());

            int rowsUpdated = stm.executeUpdate();

            if (rowsUpdated == 0) {
                throw new SQLException("Classificacao not found for updating");
            }
        }
    }

    @Override
    public List<Classificacao> listar() throws SQLException {
        List<Classificacao> lista = new ArrayList<>();

        String sql = "SELECT * FROM " + getTableName();

        try (PreparedStatement stm = conn.prepareStatement(sql)) {
            try (ResultSet result = stm.executeQuery()) {
                while (result.next()) {
                    Classificacao classificacao = parse(result);
                    lista.add(classificacao);
                }
            }
        }

        return lista;
    }

    public List<Classificacao> pesquisarPorAuditor(int idAuditor) throws SQLException {
        List<Classificacao> lista = new ArrayList<>();

        String sql = "SELECT * FROM " + getTableName() + " WHERE auditor_id_auditor = ?";

        try (PreparedStatement stm = conn.prepareStatement(sql)) {
            stm.setInt(1, idAuditor);

            try (ResultSet result = stm.executeQuery()) {
                while (result.next()) {
                    Classificacao classificacao = parse(result);
                    lista.add(classificacao);
                }
            }
        }

        return lista;
    }

    public List<Classificacao> pesquisarPorPaciente(int idPaciente) throws SQLException {
        List<Classificacao> lista = new ArrayList<>();

        String sql = "SELECT * FROM " + getTableName() + " WHERE paciente_id_paciente = ?";

        try (PreparedStatement stm = conn.prepareStatement(sql)) {
            stm.setInt(1, idPaciente);

            try (ResultSet result = stm.executeQuery()) {
                while (result.next()) {
                    Classificacao classificacao = parse(result);
                    lista.add(classificacao);
                }
            }
        }

        return lista;
    }

    public List<Classificacao> pesquisarPorSinal(int idSinal) throws SQLException {
        List<Classificacao> lista = new ArrayList<>();

        String sql = "SELECT * FROM " + getTableName() + " WHERE sinal_id_sinal = ?";

        try (PreparedStatement stm = conn.prepareStatement(sql)) {
            stm.setInt(1, idSinal);

            try (ResultSet result = stm.executeQuery()) {
                while (result.next()) {
                    Classificacao classificacao = parse(result);
                    lista.add(classificacao);
                }
            }
        }

        return lista;
    }

    public List<Classificacao> pesquisarPorGravidade(int idGravidade) throws SQLException {
        List<Classificacao> lista = new ArrayList<>();

        String sql = "SELECT * FROM " + getTableName() + " WHERE gravidade_id_gravidade = ?";

        try (PreparedStatement stm = conn.prepareStatement(sql)) {
            stm.setInt(1, idGravidade);

            try (ResultSet result = stm.executeQuery()) {
                while (result.next()) {
                    Classificacao classificacao = parse(result);
                    lista.add(classificacao);
                }
            }
        }

        return lista;
    }

}
