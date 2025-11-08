> **Trabalho** **4** **de** **REDES** **DE** **COMPUTADORES**

Nome: Lucas Thiago Dias Civardi

Parte 1: Teoria

**O** **que** **são** **sockets** **e** **qual** **seu** **papel**
**na** **comunicação** **entre** **processos** **?**

Sockets representam pontos de conexão de rede que permitem a comunicação
bidirecional entre diferentes processos, seja na mesma máquina ou em
máquinas diferentes. Seu objetivo principal é abstrair a complexidade
das conexões de rede, atuando como um canal para troca de dados e sendo
a base para a comunicação em rede, tal qual um navegador web acessando
um servidor de site.

E seu papel na comunicação entre os processo é:

-Ponto de comunicação: Um socket funciona como uma "porta" para
intercâmbio de dados, fazendo a conexão de um programa a outro, parecido
à forma como lâmpadas se conectam a um circuito elétrico.

-Identificação única: Cada socket possui uma combinação única de um
endereço IP e um número de porta, que identifica um dispositivo e o
processo específico rodando nele.

-Modelo cliente-servidor: Sockets são essenciais para a arquitetura
cliente-servidor. Um servidor (por exemplo, um site) "ouve" por conexões
em um socket específico, e clientes (como seu navegador) se conecta ele
para transferência de dados.

-Abstração da rede: Eles fazem uma abstração do desenvolvimento, porque
os desenvolvedores não têm a necessidade lidar diretamente com os
detalhes do transporte de dados pela rede. O Sistema operacional faz o
gerenciamento da comunicação através do socket.

-Flexibilidade de comunicação: Sockets podem ser utilizados para
comunicações locais (mesma máquina) ou remota (através de uma rede). Em
sistemas como Unix, são tratados como arquivos, permitindo operações de
leitura e escrita.

**Comparação** **entre** **sockets** **TCP** **e** **UDP:**

||
||
||
||
||
||
||
||
||
||

**Demonstração** **ciclo** **de** **vida** **de** **um** **socket:**

<img src="./0q0uyxye.png"
style="width:5.21875in;height:7.16667in" />

**1.** **Preparação**

Cliente & Servidor: Cria o socket com Socket()

Servidor: faz a configuração do endereço com o bind() e faz a escuta com
listen()

**2.** **Conexão** **&** **Comunicação**

Cliente: Inicialização da conexão com Connect()

Servidor: Aceita a conexão com accept() → ( Conexão estabelecida)

Realização da troca de dados: send()/recv() em ambos os lados do
diagrama

**3.** **Encerramento** Cliente: Inicia close()

Servidor: Confirma com close()

Parte 2: Prática

**Justificativa** **da** **escolha** **da** **linguagem:**

Optei pela linguagem Python para o desenvolvimento deste trabalho, pois
estou em processo de aprofundamento nos estudos dessa linguagem e
acredito que este projeto pode me auxiliar na compreensão de novas
funcionalidades que ainda não conhecia. Especificamente, a biblioteca
sockets presente no Python era uma funcionalidade da qual eu não tinha
conhecimento prévio, e esta implementação prática proporcionou uma
oportunidade valiosa para explorar suas capacidades.

Código [<u>cliente.py</u>](http://cliente.py):

Utilizando IDE: VScode no windows import socket

def start_client(host='192.168.100.163', port=8888): *"""*

> *Função* *principal* *que* *inicia* *o* *cliente* *de* *chat.*
>
> *Estabelece* *conexão* *com* *o* *servidor* *e* *gerena* *o* *loop*
> *de* *comunicação* *para* *envio* *e* *recebimento* *de* *mensagens.*
>
> *"""*
>
> \# Cria socket TCP/IP para comunicação com o servidor
>
> \# AF_INET = IPv4, SOCK_STREAM = TCP (protocolo orientado a conexão)
> client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>
> try:

\# Estabelece conexão com o servidor no endereço e porta especificados

> \# connect() inicia o three-way handshake do protocolo TCP \# Se o
> servidor não estiver rodando, lançará

ConnectionRefusedError client_socket.connect((host, port))

> print(f"\[+\] Conectado ao servidor {host}:{port}") print("\[\*\]
> Digite 'sair' para encerrar")
>
> \# Loop principal de comunicação
>
> \# Mantém o cliente ativo até que o usuário decida encerrar while
> True:
>
> \# Solicita mensagem do usuário via input

\# input() é bloqueante - aguarda o usuário digitar e pressionar Enter

> message = input("Você: ")
>
> \# Envia a mensagem para o servidor

\# encode('utf-8') converte a string para bytes para transmissão pela
rede

\# send() transmite os dados através do socket TCP estabelecido

> client_socket.send(message.encode('utf-8'))

\# Verifica se o usuário digitou 'sair' para encerrar a conexão

\# lower() garante que funciona independente de maiúsculas/minúsculas

> if message.lower() == 'sair': break
>
> \# Aguarda resposta do servidor

\# recv(1024) é bloqueante - fica aguardando dados do servidor

> \# 1024 é o tamanho máximo do buffer de recebimento

\# decode('utf-8') converte os bytes recebidos de volta para string

> response = client_socket.recv(1024).decode('utf-8')
>
> \# Exibe a resposta recebida do servidor para o usuário
> print(f"Servidor: {response}")
>
> except ConnectionRefusedError:

\# Este erro ocorre quando o servidor não está disponível na porta
especificada

\# Pode ser porque o servidor não foi iniciado ou está em endereço
diferente

print("\[-\] Servidor não encontrado. Verifique se o servidor está
rodando.")

> except Exception as e:

\# Captura outros erros genéricos que podem ocorrer durante a
comunicação

> \# Como quebras de conexão, timeouts, ou problemas de rede
> print(f"Erro: {e}")
>
> finally:
>
> \# Garante que o socket seja fechado mesmo em caso de erro \# Fechar o
> socket libera os recursos do sistema operacional \# Envia o FIN do TCP
> para encerramento gracioso da conexão
>
> client_socket.close()
>
> print("\[-\] Conexão encerrada")

if \_\_name\_\_ == "\_\_main\_\_":

> \# Ponto de entrada do programa - executa a função principal

\# quando o arquivo é executado diretamente (não importado como módulo)

> start_client()

**Principais** **funções:**

Conexão TCP - Estabelece canal confiável com servidor Interface
simples - Input/Output via terminal

Comando de saída - "sair" encerra conexão graciosamente Tratamento de
erros - Servidor inacessível, falhas de rede

Código [<u>servidor.py</u>](http://servidor.py) feito na MV:

Utilizando nano(editor de texto) no linux mint:

import socket import threading

def handle_client(client_socket, client_address): """

> Função que gerencia a comunicação individual com cada cliente
> conectado.
>
> Esta função é executada em uma thread separada para cada cliente,
> permitindo que o servidor atenda múltiplas conexões ao mesmo tempo.
> Ela fica em loop contínuo recebendo mensagens do cliente até que a
> conexão seja encerrada.
>
> Fluxo de operação:
>
> 1\. Aguarda mensagens do cliente usando recv() (chamada bloqueante) 2.
> Processa a mensagem recebida
>
> 3\. Envia resposta para o cliente
>
> 4\. Repete até detectar desconexão ou comando 'sair' """
>
> print(f"\[+\] Nova conexão estabelecida com {client_address}")
>
> try:
>
> while True:
>
> \# RECEBIMENTO DE MENSAGENS:
>
> \# recv(1024) bloqueia a execução até receber dados do cliente \# O
> número 1024 define o buffer máximo para recebimento
>
> \# decode('utf-8') converte os bytes recebidos para string message =
> client_socket.recv(1024).decode('utf-8')
>
> \# VERIFICAÇÃO DE CONEXÃO ATIVA:
>
> \# Se a mensagem estiver vazia, indica que o cliente fechou a conexão
> \# Isso ocorre quando o cliente chama socket.close() normalmente
>
> if not message: break
>
> \# LOG DA MENSAGEM NO SERVIDOR:
>
> \# Exibe a mensagem recebida junto com informações do cliente
>
> print(f"Cliente {client_address}: {message}")
>
> \# TRATAMENTO DO COMANDO DE SAÍDA:
>
> \# Se o cliente enviar 'sair', encerramos a conexão com ele
>
> \# lower() garante que o comando funcione independente de
> maiúsculas/minúsculas if message.lower() == 'sair':
>
> client_socket.send("Conexão encerrada.".encode('utf-8')) break
>
> \# PREPARAÇÃO E ENVIO DE RESPOSTA:
>
> \# Cria uma resposta confirmando o recebimento da mensagem \#
> encode('utf-8') converte a string para bytes para transmissão response
> = f"Servidor recebeu: {message}"
> client_socket.send(response.encode('utf-8'))
>
> except Exception as e:
>
> \# TRATAMENTO DE ERROS DE COMUNICAÇÃO:
>
> \# Captura exceções como quebra de conexão abrupta, erros de rede,
> etc.
>
> \# Isso impede que erros em um cliente afetem os outros clientes
> conectados print(f"Erro: {e}")
>
> finally:
>
> \# LIMPEZA DE RECURSOS:
>
> \# Garante que o socket do cliente seja fechado mesmo em caso de erro
> \# Libera os recursos do sistema operacional associados ao socket
> client_socket.close()
>
> print(f"\[-\] {client_address} desconectou")

def start_server(host='0.0.0.0', port=8888): """

> Função principal que inicializa e executa o servidor de chat.
>
> Esta função configura o socket do servidor, coloca-o em modo de escuta
> e fica em loop infinito aceitando novas conexões de clientes.
>
> Parâmetros:
>
> host='0.0.0.0' - Escuta em todas as interfaces de rede (permite
> conexões externas) port=8888 - Porta TCP onde o servidor ficará
> escutando
>
> Funcionamento interno: 1. Cria socket TCP/IP
>
> 2\. Configura opções do socket
>
> 3\. Vincula socket ao endereço e porta 4. Coloca socket em modo de
> escuta
>
> 5\. Aceita conexões em loop, criando thread para cada cliente """
>
> \# CRIAÇÃO DO SOCKET DO SERVIDOR: \# AF_INET especifica que usaremos
> IPv4
>
> \# SOCK_STREAM especifica que usaremos TCP (orientado a conexão)
> server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>
> \# CONFIGURAÇÃO DE REUTILIZAÇÃO DE ENDEREÇO:
>
> \# SO_REUSEADDR permite reutilizar o endereço/porta imediatamente após
> \# o servidor ser fechado, evitando o erro "Address already in use"
>
> server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
>
> try:
>
> \# VINCULAÇÃO DO SOCKET AO ENDEREÇO:
>
> \# bind() associa o socket ao endereço IP e porta especificados
>
> \# '0.0.0.0' significa que o servidor escutará em todas as interfaces
> server_socket.bind((host, port))
>
> \# HABILITA MODO DE ESCUTA:
>
> \# listen(5) coloca o socket em estado de escuta, permitindo aceitar
> conexões \# O número 5 define o tamanho da fila de conexões pendentes
> server_socket.listen(5)
>
> print(f"\[\*\] Servidor ouvindo em {host}:{port}") print("\[\*\]
> Aguardando conexões...")
>
> \# LOOP PRINCIPAL DE ACEITAÇÃO DE CONEXÕES: \# O servidor fica em loop
> infinito aceitando novas conexões while True:
>
> \# ACEITAÇÃO DE CONEXÃO (BLOQUEANTE):
>
> \# accept() bloqueia a execução até que um cliente conecte
>
> \# Retorna um novo socket para comunicação com o cliente específico \#
> e o endereço (IP, porta) do cliente
>
> client_socket, client_address = server_socket.accept()
>
> \# CRIAÇÃO DE THREAD PARA O CLIENTE:
>
> \# Cada cliente é atendido em uma thread separada para permitir \#
> atendimento simultâneo de múltiplos clientes
>
> client_thread = threading.Thread( target=handle_client,
> args=(client_socket, client_address) )
>
> \# CONFIGURAÇÃO DA THREAD COMO DAEMON:
>
> \# Threads daemon são automaticamente encerradas quando o programa
> principal termina \# Isso garante que todas as threads sejam fechadas
> ao encerrar o servidor client_thread.daemon = True
>
> \# INICIALIZAÇÃO DA THREAD:
>
> \# A thread começa a executar a função handle_client com os argumentos
> fornecidos client_thread.start()
>
> except KeyboardInterrupt:
>
> \# TRATAMENTO DE INTERRUPÇÃO POR TECLADO:
>
> \# Captura Ctrl+C, permitindo encerramento gracioso do servidor
> print("\n\[\*\] Servidor encerrado")
>
> except Exception as e:
>
> \# TRATAMENTO DE ERROS GERAIS: \# Captura qualquer outro erro não
> previsto print(f"Erro: {e}")
>
> finally:
>
> \# GARANTIA DE FECHAMENTO DO SOCKET:
>
> \# Garante que o socket do servidor seja fechado mesmo em caso de erro
> \# Libera a porta 8888 para uso por outros aplicativos
> server_socket.close()

if \_\_name\_\_ == "\_\_main\_\_": """

> Ponto de entrada do programa.
>
> Esta verificação garante que o servidor só será iniciado se o arquivo
> for executado diretamente, e não se for importado como módulo.
>
> start_server() inicia o loop principal do servidor, que só terminará

<img src="./bt14psh0.png"
style="width:6.27083in;height:3.96875in" />

> quando o servidor for interrompido (normalmente por Ctrl+C). """
>
> start_server()

**Como** **executar** **o** **código:**

Python 3.6 ou superior

Máquina virtual Linux (para servidor)

Máquina principal (para cliente)

Ambas na mesma rede

Ter o ip da sua rede para colocar no código

**Instruções** **de** **execução:**

Sequência obrigatória:

1-Executar o código [<u>servidor.py</u>](http://servidor.py) na maquina
virtual: 2-Executar o código [<u>cliente.py</u>](http://cliente.py) na
máquina normal:

**Capturas** **de** **telas** **da** **aplicação** **funcionando:**
**Servidor** **rodando** **na** **MV:**

**Cliente** **conectado:**

<img src="./bhxxnvks.png"
style="width:6.27083in;height:4.76042in" />

<img src="./ne0w3wui.png"
style="width:6.27083in;height:1.59375in" /><img src="./dv0qp1e4.png"
style="width:6.27083in;height:2.44792in" />**Troca** **de**
**mensagens:**

<img src="./tslqwb52.png"
style="width:4.23958in;height:2.71875in" />

*as* *3* *imagens* *se* *tratam* *da* *mesma* *funcionalidade* *mas*
*para* *melhor* *qualidade* *da* *imagem* *fiz* *também* *a* *captura*
*das* *telas* *separadamente.*

<img src="./qa1wp45k.png"
style="width:6.27083in;height:1.55208in" /><img src="./uc21nq5t.png"
style="width:6.27083in;height:2.42708in" />**Encerramento:**

<img src="./s51zql10.png"
style="width:5.375in;height:3.14583in" />

*as* *3* *imagens* *se* *tratam* *da* *mesma* *funcionalidade* *mas*
*para* *melhor* *qualidade* *da* *imagem* *fiz* *também* *a* *captura*
*das* *telas* *separadamente.*

<img src="./tjtb4vbi.png"
style="width:6.27083in;height:1.21875in" />**ERRO(Rodar** **o**
[**<u>cliente.py</u>**](http://cliente.py) **sem** **antes** **o**
**servidor.py:**

