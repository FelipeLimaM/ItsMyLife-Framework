# Its My Life  - Context Aware

O projeto foi desenvolvido a partir de um aglomerado de scripts em python. Esse scripts foram usados para a geração de dados de uma dissertação de mestrado realizado dentro do UNICAMP com parceria da Motorola.

O intuito desse servidor é facilitar a manipulação dos dados que podem ser vindo de diversos Smartphones atraves de coletas simultaneas.

## Pre-requisisto:

 - Criar um projeto dentro do Firebase. [link](https://github.com/FelipeLimaM/ItsMyLife-Framework/blob/master/Firebase_setup.pdf)

 - Gerar o arquivo de acesso (Projeto Firebase) para aplicação do Smartphone.

 - Configurar um Email para que o servidor possa disparar o emails com o resultado ou informando algum erro durante o processamento das informações.

## Iniciando o servidor:

Para executar o servidor, basta colocar as configurações explicadas nos link acima, após isso dentro do diretorio do projeto, rode o seguinte comando:

```
docker-compose up -d
```

Após concluir vc já poderá ser acessivel pela sua maquina ou rede local, se for um servidor, pode ser acessivel pelo IP externo.
