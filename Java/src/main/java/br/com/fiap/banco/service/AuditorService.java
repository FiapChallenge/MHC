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
    private AuditorDao dao;

    public AuditorService() throws ClassNotFoundException, SQLException {
        super(new AuditorDao(ConnectionFactory.getConnection()));
        this.classificacaoDao = new ClassificacaoDao(ConnectionFactory.getConnection());
        this.dao = new AuditorDao(ConnectionFactory.getConnection());
    }

    @Override
    public void remover(int id) throws ClassNotFoundException, SQLException, HasChildException, IdNotFoundException {
        if (classificacaoDao.pesquisarPorAuditor(id).size() > 0) {
            throw new HasChildException("Auditor não pode ser removido pois possui classificações");
        }
        super.remover(id);
    }

    @Override
    protected void validar(Auditor auditor) throws BadInfoException, SQLException, ClassNotFoundException {
        if (auditor.getNome() == null) {
            throw new BadInfoException("Nome não pode ser vazio");
        }
        if (auditor.getNome().length() > 50) {
            throw new BadInfoException("Nome não pode ter mais de 50 caracteres");
        }
        if (auditor.getEmail() == null) {
            throw new BadInfoException("Email não pode ser vazio");
        }
        if (auditor.getEmail().length() > 50) {
            throw new BadInfoException("Email não pode ter mais de 50 caracteres");
        }
        if (dao.pesquisarPorEmail(auditor.getEmail()) != null) {
            throw new BadInfoException("Email já cadastrado");
        }
        if (auditor.getSenha() == null) {
            throw new BadInfoException("Senha não pode ser vazia");
        }
        if (auditor.getSenha().length() > 50) {
            throw new BadInfoException("Senha não pode ter mais de 50 caracteres");
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
        if (auditor.getCpf() != null && auditor.getCpf().length() != 11) {
            throw new BadInfoException("CPF deve ter 11 caracteres");
        }
        try {
            if (auditor.getCpf() != null) {
                Long.parseLong(auditor.getCpf());
            }
        } catch (NumberFormatException e) {
            throw new BadInfoException("CPF deve ser numérico");
        }
    }

}
