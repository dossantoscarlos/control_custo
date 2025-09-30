# Fix(otel): Substituir o `logging` exporter depreciado

## 1. Problema

*   O container `otel-collector` não estava iniciando e apresentava o status `Exited (1)`.

## 2. Diagnóstico

*   A análise dos logs do container revelou o erro: `the logging exporter has been deprecated, use the debug exporter instead`.
*   O arquivo de configuração `otel-collector-config.yaml` confirmou o uso do `logging` exporter, que foi descontinuado.

## 3. Solução

*   O arquivo `otel-collector-config.yaml` foi modificado para substituir o `logging` exporter pelo `debug` exporter.
*   A diretiva `loglevel: debug` foi substituída por `verbosity: detailed`, conforme a nova especificação do `debug` exporter.

## 4. Verificação

*   O container `otel-collector` foi iniciado com sucesso após a correção da configuração.
*   O status do container foi verificado e confirmado como `Up`.
