package br.com.fiap.banco.resource;

import java.sql.SQLException;

import br.com.fiap.banco.model.Paciente;
import br.com.fiap.banco.service.GenericService;
import br.com.fiap.banco.service.PacienteService;
import jakarta.ws.rs.Path;

@Path("/paciente")
public class PacienteResource extends GenericResource<Paciente> {

    private PacienteService service;

    public PacienteResource() throws ClassNotFoundException, SQLException {
        service = new PacienteService();
    }

    @Override
    protected GenericService<Paciente> getService() {
        return service;
    }
}
