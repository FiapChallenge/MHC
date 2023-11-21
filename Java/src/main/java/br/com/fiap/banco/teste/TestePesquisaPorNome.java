package br.com.fiap.banco.teste;

import java.util.List;

import br.com.fiap.banco.model.Auditor;
import br.com.fiap.banco.service.AuditorService;

public class TestePesquisaPorNome {

    // Testar a pesquisa por nome do auditor
    public static void main(String[] args) {

        try {
            AuditorService service = new AuditorService();
            List<Auditor> auditores = service.pesquisarPorNome("Ma");
            for (Auditor auditor : auditores) {
                System.out.println(auditor);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
