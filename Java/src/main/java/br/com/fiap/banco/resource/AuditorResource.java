package br.com.fiap.banco.resource;

import java.sql.SQLException;

import br.com.fiap.banco.model.Auditor;
import br.com.fiap.banco.service.AuditorService;
import br.com.fiap.banco.service.GenericService;
import jakarta.ws.rs.Path;

@Path("/auditor")
public class AuditorResource extends GenericResource<Auditor> {

    private AuditorService service;

    public AuditorResource() throws ClassNotFoundException, SQLException {
        service = new AuditorService();
    }

    @Override
    protected GenericService<Auditor> getService() {
        return service;
    }
}
