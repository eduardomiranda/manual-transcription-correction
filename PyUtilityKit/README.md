# PyUtilityKit
O PyUtilityKit é um módulo Python destinado a fornecer uma coleção de funcionalidades úteis para diversos projetos. Este módulo oferece métodos simplificados para tarefas comuns, como envio de arquivos para buckets S3, renomeação de arquivos, envio de e-mails e deleção de arquivos.



\
&nbsp;
## Instalação do pacote PyUtilityKit
Com o comando a seguir o pacote **PyUtilityKit** será instalado no ***Virtual Environment*** ativado anteriormente e vai estar disponível para os demais projetos dentro do mesmo  ***Virtual Environment***.

```sh
pip3 install -e .
```



&nbsp;
## Criando o Python Virtual Environment
Necessário apenas um única vez.

```sh
python3  -m  venv  myvenv
```

\
&nbsp;
## Ativando o Virtual Environment
**Necessário toda vez** que for executar o código.

```sh
source  myvenv/bin/activate
```


# Melhorias
- Remover várias funções desnecessárias
- Resolver a questão dos logs em outros aqruivos como filesistem_manager, etc...
- Pensar em como paralelizar melhor a execução