package br.com.fiap.banco.resource;

import java.sql.SQLException;
import java.util.List;

import br.com.fiap.banco.exception.BadInfoException;
import br.com.fiap.banco.exception.HasChildException;
import br.com.fiap.banco.exception.IdNotFoundException;
import br.com.fiap.banco.service.GenericService;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.Context;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.core.UriBuilder;
import jakarta.ws.rs.core.UriInfo;
import jakarta.ws.rs.core.Response.Status;

public abstract class GenericResource<T> {

    protected abstract GenericService<T> getService();

    @GET
    @Path("/query")
    @Produces(MediaType.APPLICATION_JSON)
    public List<T> pesquisar(@QueryParam("nome") String pesquisa) throws SQLException {
        return getService().pesquisarPorNome(pesquisa);
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public List<T> lista() throws ClassNotFoundException, SQLException {
        return getService().listar();
    }

    @GET
    @Path("/{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response busca(@PathParam("id") int codigo) throws ClassNotFoundException, SQLException {
        try {
            return Response.ok(getService().pesquisar(codigo)).build();
        } catch (IdNotFoundException e) {
            return Response.status(Status.NOT_FOUND).build();
        }
    }

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    public Response cadastrar(T entity, @Context UriInfo uri) throws ClassNotFoundException, SQLException {
        try {
            getService().cadastrar(entity);

            UriBuilder uriBuilder = uri.getAbsolutePathBuilder();
            return Response.created(uriBuilder.build()).build();
        } catch (BadInfoException e) {
            return Response.status(Status.BAD_REQUEST)
                    .entity(e.getMessage()).build();
        }
    }

    @PUT
    @Path("/{id}")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response atualizar(T entity, @PathParam("id") int codigo)
            throws ClassNotFoundException, SQLException {
        try {
            // setId of entity with codigo
            entity.getClass().getMethod("setId", int.class).invoke(entity, codigo);
            getService().atualizar(entity);
            return Response.ok().build();
        } catch (IdNotFoundException e) {
            return Response.status(Status.NOT_FOUND).build();
        } catch (BadInfoException e) {
            return Response.status(Status.BAD_REQUEST).entity(e.getMessage()).build();
        } catch (Exception e) {
            return Response.status(Status.INTERNAL_SERVER_ERROR).build();
        }
    }

    @DELETE
    @Path("/{id}")
    public Response remover(@PathParam("id") int id) throws ClassNotFoundException, SQLException {
        try {
            getService().remover(id);
            return Response.noContent().build();
        } catch (IdNotFoundException e) {
            return Response.status(Status.NOT_FOUND).build();
        } catch (HasChildException e) {
            return Response.status(Status.BAD_REQUEST).entity(e.getMessage()).build();
        }
    }
}
