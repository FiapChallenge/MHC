package br.com.fiap.banco.service;

import java.sql.SQLException;
import java.util.List;

import br.com.fiap.banco.dao.GenericDao;
import br.com.fiap.banco.exception.BadInfoException;
import br.com.fiap.banco.exception.HasChildException;
import br.com.fiap.banco.exception.IdNotFoundException;

public abstract class GenericService<T> {

    protected GenericDao<T> genericDao;

    public GenericService(GenericDao<T> genericDao) {
        this.genericDao = genericDao;
    }

    public void cadastrar(T entity) throws ClassNotFoundException, SQLException, BadInfoException {
        validar(entity);
        genericDao.cadastrar(entity);
    }

    protected abstract void validar(T entity) throws BadInfoException, SQLException;

    public void atualizar(T entity)
            throws ClassNotFoundException, SQLException, IdNotFoundException, BadInfoException {
        validar(entity);
        genericDao.atualizar(entity);
    }

    public void remover(int id)
            throws ClassNotFoundException, SQLException, IdNotFoundException, HasChildException {
        genericDao.remover(id);
    }

    public List<T> listar() throws ClassNotFoundException, SQLException {
        return genericDao.listar();
    }

    public T pesquisar(int codigo) throws ClassNotFoundException, SQLException, IdNotFoundException {
        return genericDao.pesquisar(codigo);
    }

    public List<T> pesquisarPorNome(String nome) throws SQLException {
        return genericDao.pesquisarPorNome(nome);
    }
}
