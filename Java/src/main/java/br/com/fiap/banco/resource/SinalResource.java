package br.com.fiap.banco.resource;

import java.sql.SQLException;

import br.com.fiap.banco.model.Sinal;
import br.com.fiap.banco.service.GenericService;
import br.com.fiap.banco.service.SinalService;
import jakarta.ws.rs.Path;

@Path("/sinal")
public class SinalResource extends GenericResource<Sinal> {

    private SinalService service;

    public SinalResource() throws ClassNotFoundException, SQLException {
        service = new SinalService();
    }

    @Override
    protected GenericService<Sinal> getService() {
        return service;
    }
}
