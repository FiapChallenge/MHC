package br.com.fiap.banco.service;

import java.sql.SQLException;

import br.com.fiap.banco.dao.ClassificacaoDao;
import br.com.fiap.banco.exception.BadInfoException;
import br.com.fiap.banco.model.Classificacao;
import br.com.fiap.banco.factory.ConnectionFactory;

public class ClassificacaoService extends GenericService<Classificacao> {

    // private ClassificacaoDao classificacaoDao;

    public ClassificacaoService() throws ClassNotFoundException, SQLException {
        super(new ClassificacaoDao(ConnectionFactory.getConnection()));
        // this.classificacaoDao = (ClassificacaoDao) genericDao;
    }

    @Override
    protected void validar(Classificacao classificacao) throws BadInfoException, SQLException {
        if (classificacao.getDataHoraClassificacao() == null) {
            throw new BadInfoException("Data e hora da classificação não pode ser vazio");
        }
        if (classificacao.getGravidade() == null) {
            throw new BadInfoException("ID da gravidade não pode ser vazio");
        }
        if (classificacao.getPaciente() == null) {
            throw new BadInfoException("ID do paciente não pode ser vazio");
        }
        if (classificacao.getAuditor() == null) {
            throw new BadInfoException("ID do auditor não pode ser vazio");
        }
        if (classificacao.getSinal() == null) {
            throw new BadInfoException("ID do sinal não pode ser vazio");
        }
    }

}
