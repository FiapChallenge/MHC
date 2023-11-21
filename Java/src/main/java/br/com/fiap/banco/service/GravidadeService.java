package br.com.fiap.banco.service;

import java.sql.SQLException;

import br.com.fiap.banco.dao.ClassificacaoDao;
import br.com.fiap.banco.dao.GravidadeDao;
import br.com.fiap.banco.exception.BadInfoException;
import br.com.fiap.banco.model.Gravidade;
import br.com.fiap.banco.exception.HasChildException;
import br.com.fiap.banco.exception.IdNotFoundException;
import br.com.fiap.banco.factory.ConnectionFactory;

public class GravidadeService extends GenericService<Gravidade> {

    private ClassificacaoDao classificacaoDao;;

    public GravidadeService() throws ClassNotFoundException, SQLException {
        super(new GravidadeDao(ConnectionFactory.getConnection()));
        this.classificacaoDao = new ClassificacaoDao(ConnectionFactory.getConnection());
    }

    @Override
    public void remover(int id) throws ClassNotFoundException, SQLException, HasChildException, IdNotFoundException {
        if (classificacaoDao.pesquisarPorGravidade(id).size() > 0) {
            throw new HasChildException("Gravidade não pode ser removida pois possui classificações");
        }
        super.remover(id);
    }

    @Override
    protected void validar(Gravidade gravidade) throws BadInfoException, SQLException {
        if (gravidade.getNomeGravidade() == null) {
            throw new BadInfoException("Nome da gravidade não pode ser vazio");
        }
        if (gravidade.getNomeGravidade().length() > 20) {
            throw new BadInfoException("Nome da gravidade não pode ter mais de 20 caracteres");
        }
        if (gravidade.getNomeCor() == null) {
            throw new BadInfoException("Nome da cor não pode ser vazio");
        }
        if (gravidade.getNomeCor().length() > 20) {
            throw new BadInfoException("Nome da cor não pode ter mais de 20 caracteres");
        }
        if (gravidade.getHexadecimalCor() != null && gravidade.getHexadecimalCor().length() > 6) {
            throw new BadInfoException("Hexadecimal da cor não pode ter mais de 6 caracteres");
        }
    }

}
