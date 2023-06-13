# Projeto 1 - Redes de Computadores

<h1> Estrutura do projeto: </h1> <br> 
O nosso projeto é dividido em duas pastas, uma do servidor, onde há uma pasta com as músicas armazenadas no servidor (resource) e o arquivo server.py, já na pasta client, temos uma pasta cache, que por padrão não existe e é criada apenas quando inicia-se uma reprodução, que contém as músicas que são armazenadas em memória no cliente durante o streaming de aúdio.<br>


<br> ![Alt text](image-2.png)
<br>

<h1> Padrão de mensagem e protocolo </h1>
De inicio, possuimos 5 serviços, são eles:


- Listar os dispositivos
- Listar as músicas
- Reproduzir música
- Tornar-se apto para reproduzir músicas de outro client
- Encerrar a conexão

As requisições que o client envia para o server seguem um padrão JSON, na seguinte configuração:
<code> {'service':'list_devices'} </code> <br>
<code> {'service':'list_songs'} </code> <br>
<code> {'service':'play_music','music':'music_name', 'device':'device_ip'} <br># O campo device por padrão é vazio. </code> <br>
O  serviço de estar disponível para reproduzir uma música não adota esse protocolo padrão, ele apenas fica em modo listen esperando uma comunicação do servidor. <br>
<code> {'service':'end_connection'} </code> <br>
O tamanho padrão de mensagens enviadas é de <b> 1024</b> bytes. <br>
As requisições são recebidas pelo servidor, decodificadas e interpretadas de acordo com o seu conteúdo, na função <b><code> handle_client() </code>  </b> e, para cada comando específico, é encaminhado para uma função que trata a requisição e envia a resposta ao client já com os dados solicitados anteriormente. <br>
Ao receber a resposta, o client as decodifica e já as executa dentro das funções próprias.
<h1> Limitações e pontos a serem tratados: </h1>

- Não conseguimos implementar corretamente o pause e o retorno da bufferização, acabamos nos confundindo muito e perdendo bastante tempo na questão das threads, temos a intenção de implementar esse requisito em breve.
- Também não conseguimos implementar a transmissão em pacotes de 30s de áudio.
- Nós não tratamos devidamente os erros, ou seja, com entradas erradas ou inesperadas do usuário, o client pode parar de funcionar.
- Tinhámos a intenção de criar um arquivo de logs, para armazenar todos os registros da comuniação entre o servidor e os clients, também será implementado no futuro ( é uma solução bem simples). <br>

[Link do repositório](https://github.com/felipeonf/redes-computadores/)
<h2> Alunos: </h2>
<h3>
<br>Carlos Eduardo de Carvalho Veras, 222012729<br>Felipe Oliveira do Nascimento Florentino, 202021767<br> THIAGO CALEGARIO FERREIRA GOMES, 211037238 </h3>