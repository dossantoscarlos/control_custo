# Plano de Ação para Corrigir Health Check de Containers

## 1. Diagnóstico Inicial

*   O usuário reportou que o container `keycloak` estava com status `unhealthy`.
*   Ao inspecionar o container, foi verificado que o comando de health check (`curl`) não estava disponível na imagem.

## 2. Tentativa de Correção 1 (Falha)

*   A primeira tentativa foi substituir `curl` por `wget` no `docker-compose.yml`.
*   Após reiniciar os serviços, foi constatado que `wget` também não estava disponível na imagem do `keycloak`.

## 3. Diagnóstico Adicional

*   Foi observado que o container `fastapi` também estava com status `unhealthy` pelo mesmo motivo (uso de `curl` no health check).

## 4. Solução Implementada

*   A solução foi alterar o comando do health check para ambos os containers (`keycloak` e `fastapi`) no arquivo `docker-compose.yml`.
*   O novo comando utiliza `bash` para testar a conexão TCP na porta correspondente, sem depender de `curl` ou `wget`.
    *   **Keycloak:** `test: ["CMD-SHELL", "bash -c 'exec 3<>/dev/tcp/localhost/9000' || exit 1"]`
    *   **Fastapi:** `test: ["CMD-SHELL", "bash -c 'exec 3<>/dev/tcp/localhost/8000' || exit 1"]`
*   Também foi exposta a porta `9000` no serviço do `keycloak` para permitir o acesso do health check.

## 5. Verificação

*   Os serviços foram reiniciados com `docker-compose down` e `docker-compose up -d`.
*   Após a reinicialização, o status de ambos os containers foi verificado e confirmado como `healthy`.
