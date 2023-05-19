# redes-computadores
## Trabalho 1
### Streaming de  ́audio
- Cliente deve poder recuperar a lista de m ́usicas no servidor
- Cliente deve poder clicar para tocar uma m ́usica hospedada no servidor
- Se o cliente tentar tocar a m ́usica e ela n ̃ao estiver em cache local, buscar no servidor
- O servidor deve transmitir a m ́usica em blocos de 30 segundos de  ́audio
- O cliente deve poder pausar a m ́usica, o que deve interromper a bufferiza ̧c ̃ao
- Se o cliente retomar a execu ̧c ̃ao do ponto parado ou reiniciar a m ́usica, o buffer local deve ser
consumido
- Diferentes clientes devem ser capazes de se descobrir em uma rede local
- Clientes devem ser capazes de tocar a m ́usica em um cliente remoto
