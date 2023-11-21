package br.com.fiap.banco.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import br.com.fiap.banco.exception.IdNotFoundException;

public abstract class GenericDao<T> {

    protected Connection conn;

    public GenericDao(Connection conn) {
        this.conn = conn;
    }

    protected abstract String getTableName();

    public abstract void cadastrar(T entity) throws SQLException;

    protected abstract T parse(ResultSet result) throws SQLException;

    public abstract void atualizar(T entity) throws SQLException, IdNotFoundException;

    public void remover(int id) throws SQLException, IdNotFoundException {
        PreparedStatement stm = conn
                .prepareStatement(
                        "DELETE FROM " + getTableName() + " WHERE id_" + getTableName().toLowerCase() + " = ?");
        stm.setInt(1, id);
        stm.executeUpdate();
        if (stm.getUpdateCount() == 0) {
            throw new IdNotFoundException(getTableName() + " com id " + id + " não encontrado");
        }
    }

    public List<T> listar() throws SQLException {
        PreparedStatement stm = conn.prepareStatement("SELECT * FROM " + getTableName());
        return executeQuery(stm);
    }

    public T pesquisar(int id) throws SQLException, IdNotFoundException {
        PreparedStatement stm = conn
                .prepareStatement("SELECT * FROM " + getTableName() + " WHERE id_" + getTableName() + " = ?");
        stm.setInt(1, id);
        ResultSet result = stm.executeQuery();
        if (result.next()) {
            return parse(result);
        }
        throw new IdNotFoundException(getTableName() + " com id " + id + " não encontrado");
    }

    public List<T> pesquisarPorNome(String nome) throws SQLException {
        PreparedStatement stm = conn
                .prepareStatement("SELECT * FROM " + getTableName() + " WHERE LOWER(nome) LIKE LOWER(?)");
        stm.setString(1, "%" + nome + "%");
        return executeQuery(stm);
    }

    protected List<T> executeQuery(PreparedStatement stm) throws SQLException {
        ResultSet result = stm.executeQuery();
        List<T> lista = new ArrayList<>();
        while (result.next()) {
            T entity = parse(result);
            lista.add(entity);
        }
        return lista;
    }
}
