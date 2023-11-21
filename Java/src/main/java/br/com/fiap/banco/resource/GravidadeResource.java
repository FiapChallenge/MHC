package br.com.fiap.banco.resource;

import java.sql.SQLException;

import br.com.fiap.banco.model.Gravidade;
import br.com.fiap.banco.service.GenericService;
import br.com.fiap.banco.service.GravidadeService;
import jakarta.ws.rs.Path;

@Path("/gravidade")
public class GravidadeResource extends GenericResource<Gravidade> {

    private GravidadeService service;

    public GravidadeResource() throws ClassNotFoundException, SQLException {
        service = new GravidadeService();
    }

    @Override
    protected GenericService<Gravidade> getService() {
        return service;
    }
}
