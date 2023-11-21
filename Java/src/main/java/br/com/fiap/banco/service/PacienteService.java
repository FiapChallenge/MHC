package br.com.fiap.banco.service;

import java.sql.SQLException;

import br.com.fiap.banco.dao.ClassificacaoDao;
import br.com.fiap.banco.dao.PacienteDao;
import br.com.fiap.banco.exception.BadInfoException;
import br.com.fiap.banco.model.Paciente;
import br.com.fiap.banco.exception.HasChildException;
import br.com.fiap.banco.exception.IdNotFoundException;
import br.com.fiap.banco.factory.ConnectionFactory;

public class PacienteService extends GenericService<Paciente> {

    private ClassificacaoDao classificacaoDao;;

    public PacienteService() throws ClassNotFoundException, SQLException {
        super(new PacienteDao(ConnectionFactory.getConnection()));
        this.classificacaoDao = new ClassificacaoDao(ConnectionFactory.getConnection());
    }

    @Override
    public void remover(int id) throws ClassNotFoundException, SQLException, HasChildException, IdNotFoundException {
        if (classificacaoDao.pesquisarPorPaciente(id).size() > 0) {
            throw new HasChildException("Paciente não pode ser removido pois possui classificações");
        }
        super.remover(id);
    }

    @Override
    protected void validar(Paciente paciente) throws BadInfoException, SQLException {
        if (paciente.getDataHoraEntrada() == null) {
            throw new BadInfoException("Data e hora de entrada do paciente não pode ser vazio");
        }
        if (paciente.getNome() != null && paciente.getNome().length() > 50) {
            throw new BadInfoException("Nome do paciente não pode ter mais de 50 caracteres");
        }
        if (paciente.getCpf() != null && paciente.getCpf().length() != 11) {
            throw new BadInfoException("CPF do paciente deve ter 11 caracteres");
        }
        if (paciente.getRg() != null && paciente.getRg().length() > 9) {
            throw new BadInfoException("RG do paciente não pode ter mais de 9 caracteres");
        }
        if (paciente.getSexo() != null && paciente.getSexo().length() > 1) {
            throw new BadInfoException("Sexo do paciente não pode ter mais de 1 caracter");
        }
        if (paciente.getIdade() != null && paciente.getIdade().toString().length() > 3) {
            throw new BadInfoException("Idade do paciente não pode ter mais de 3 caracteres");
        }
        if (paciente.getAltura() != null && paciente.getAltura().toString().length() > 3) {
            throw new BadInfoException("Altura do paciente não pode ter mais de 3 caracteres");
        }
        if (paciente.getPeso() != null && paciente.getPeso().toString().length() > 3) {
            throw new BadInfoException("Peso do paciente não pode ter mais de 3 caracteres");
        }

    }

}
