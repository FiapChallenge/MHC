package br.com.fiap.banco.service;

import java.sql.SQLException;

import br.com.fiap.banco.dao.AuditorDao;
import br.com.fiap.banco.dao.ClassificacaoDao;
import br.com.fiap.banco.exception.BadInfoException;
import br.com.fiap.banco.exception.HasChildException;
import br.com.fiap.banco.exception.IdNotFoundException;
import br.com.fiap.banco.model.Auditor;
import br.com.fiap.banco.factory.ConnectionFactory;

public class AuditorService extends GenericService<Auditor> {

    private ClassificacaoDao classificacaoDao;;

    public AuditorService() throws ClassNotFoundException, SQLException {
        super(new AuditorDao(ConnectionFactory.getConnection()));
        this.classificacaoDao = new ClassificacaoDao(ConnectionFactory.getConnection());
    }

    @Override
    public void remover(int id) throws ClassNotFoundException, SQLException, HasChildException, IdNotFoundException {
        if (classificacaoDao.pesquisarPorAuditor(id).size() > 0) {
            throw new HasChildException("Auditor não pode ser removido pois possui classificações");
        }
        super.remover(id);
    }

    @Override
    protected void validar(Auditor auditor) throws BadInfoException, SQLException {
        if (auditor.getCpf() == null) {
            throw new BadInfoException("CPF não pode ser vazio");
        }
        if (auditor.getNome() == null) {
            throw new BadInfoException("Nome não pode ser vazio");
        }
        if (auditor.getNome().length() > 50) {
            throw new BadInfoException("Nome não pode ter mais de 50 caracteres");
        }
        if (auditor.getCrm() != null && auditor.getCrm().length() > 20) {
            throw new BadInfoException("CRM não pode ter mais de 20 caracteres");
        }
        if (auditor.getCoren() != null && auditor.getCoren().length() > 20) {
            throw new BadInfoException("COREN não pode ter mais de 20 caracteres");
        }
        if (auditor.getEspecialidade() != null && auditor.getEspecialidade().length() > 50) {
            throw new BadInfoException("Especialidade não pode ter mais de 50 caracteres");
        }
        if (auditor.getCpf().length() != 11) {
            throw new BadInfoException("CPF deve ter 11 caracteres");
        }
        try {
            Long.parseLong(auditor.getCpf());
        } catch (NumberFormatException e) {
            throw new BadInfoException("CPF deve ser numérico");
        }
    }

}
