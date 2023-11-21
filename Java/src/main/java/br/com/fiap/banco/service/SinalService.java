package br.com.fiap.banco.service;

import java.sql.SQLException;

import br.com.fiap.banco.dao.ClassificacaoDao;
import br.com.fiap.banco.dao.SinalDao;
import br.com.fiap.banco.exception.BadInfoException;
import br.com.fiap.banco.model.Sinal;
import br.com.fiap.banco.exception.HasChildException;
import br.com.fiap.banco.exception.IdNotFoundException;
import br.com.fiap.banco.factory.ConnectionFactory;

public class SinalService extends GenericService<Sinal> {

    private ClassificacaoDao classificacaoDao;;
    public SinalService() throws ClassNotFoundException, SQLException {
        super(new SinalDao(ConnectionFactory.getConnection()));
        this.classificacaoDao = new ClassificacaoDao(ConnectionFactory.getConnection());
    }

    @Override
    public void remover(int id) throws ClassNotFoundException, SQLException, HasChildException, IdNotFoundException {
        if (classificacaoDao.pesquisarPorSinal(id).size() > 0) {
            throw new HasChildException("Sinal não pode ser removido pois possui classificações");
        }
        super.remover(id);
    }


    @Override
    protected void validar(Sinal sinal) throws BadInfoException, SQLException {
        if (sinal.getNome() == null) {
            throw new BadInfoException("Nome do sinal não pode ser vazio");
        }
        if (sinal.getNome().length() > 60) {
            throw new BadInfoException("Nome do sinal não pode ter mais de 60 caracteres");
        }
        if (sinal.getDescricao() == null) {
            throw new BadInfoException("Descrição do sinal não pode ser vazio");
        }
        if (sinal.getDescricao().length() > 700) {
            throw new BadInfoException("Descrição do sinal não pode ter mais de 700 caracteres");
        }
    }

}
