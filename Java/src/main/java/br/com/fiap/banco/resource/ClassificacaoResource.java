package br.com.fiap.banco.resource;

import java.sql.SQLException;

import br.com.fiap.banco.model.Classificacao;
import br.com.fiap.banco.service.ClassificacaoService;
import br.com.fiap.banco.service.GenericService;
import jakarta.ws.rs.Path;

@Path("/classificacao")
public class ClassificacaoResource extends GenericResource<Classificacao> {

    private ClassificacaoService service;

    public ClassificacaoResource() throws ClassNotFoundException, SQLException {
        service = new ClassificacaoService();
    }

    @Override
    protected GenericService<Classificacao> getService() {
        return service;
    }
}
