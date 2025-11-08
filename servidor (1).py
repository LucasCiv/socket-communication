import socket
import threading

def handle_client(client_socket, client_address):
    """
    Função que gerencia a comunicação individual com cada cliente conectado.
    
    Esta função é executada em uma thread separada para cada cliente, permitindo que
    o servidor atenda múltiplas conexões ao mesmo tempo. Ela fica em loop contínuo
    recebendo mensagens do cliente até que a conexão seja encerrada.
    
    Fluxo de operação:
    1. Aguarda mensagens do cliente usando recv() (chamada bloqueante)
    2. Processa a mensagem recebida
    3. Envia resposta para o cliente
    4. Repete até detectar desconexão ou comando 'sair'
    """
    print(f"[+] Nova conexão estabelecida com {client_address}")
    
    try:
        while True:
            # RECEBIMENTO DE MENSAGENS:
            # recv(1024) bloqueia a execução até receber dados do cliente
            # O número 1024 define o buffer máximo para recebimento
            # decode('utf-8') converte os bytes recebidos para string
            message = client_socket.recv(1024).decode('utf-8')
            
            # VERIFICAÇÃO DE CONEXÃO ATIVA:
            # Se a mensagem estiver vazia, indica que o cliente fechou a conexão
            # Isso ocorre quando o cliente chama socket.close() normalmente
            if not message:
                break
                
            # LOG DA MENSAGEM NO SERVIDOR:
            # Exibe a mensagem recebida junto com informações do cliente
            print(f"Cliente {client_address}: {message}")
            
            # TRATAMENTO DO COMANDO DE SAÍDA:
            # Se o cliente enviar 'sair', encerramos a conexão com ele
            # lower() garante que o comando funcione independente de maiúsculas/minúsculas
            if message.lower() == 'sair':
                client_socket.send("Conexão encerrada.".encode('utf-8'))
                break
                
            # PREPARAÇÃO E ENVIO DE RESPOSTA:
            # Cria uma resposta confirmando o recebimento da mensagem
            # encode('utf-8') converte a string para bytes para transmissão
            response = f"Servidor recebeu: {message}"
            client_socket.send(response.encode('utf-8'))
            
    except Exception as e:
        # TRATAMENTO DE ERROS DE COMUNICAÇÃO:
        # Captura exceções como quebra de conexão abrupta, erros de rede, etc.
        # Isso impede que erros em um cliente afetem os outros clientes conectados
        print(f"Erro: {e}")
    
    finally:
        # LIMPEZA DE RECURSOS:
        # Garante que o socket do cliente seja fechado mesmo em caso de erro
        # Libera os recursos do sistema operacional associados ao socket
        client_socket.close()
        print(f"[-] {client_address} desconectou")

def start_server(host='0.0.0.0', port=8888):
    """
    Função principal que inicializa e executa o servidor de chat.
    
    Esta função configura o socket do servidor, coloca-o em modo de escuta
    e fica em loop infinito aceitando novas conexões de clientes.
    
    Parâmetros:
    host='0.0.0.0' - Escuta em todas as interfaces de rede (permite conexões externas)
    port=8888 - Porta TCP onde o servidor ficará escutando
    
    Funcionamento interno:
    1. Cria socket TCP/IP
    2. Configura opções do socket
    3. Vincula socket ao endereço e porta
    4. Coloca socket em modo de escuta
    5. Aceita conexões em loop, criando thread para cada cliente
    """
    
    # CRIAÇÃO DO SOCKET DO SERVIDOR:
    # AF_INET especifica que usaremos IPv4
    # SOCK_STREAM especifica que usaremos TCP (orientado a conexão)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # CONFIGURAÇÃO DE REUTILIZAÇÃO DE ENDEREÇO:
    # SO_REUSEADDR permite reutilizar o endereço/porta imediatamente após
    # o servidor ser fechado, evitando o erro "Address already in use"
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # VINCULAÇÃO DO SOCKET AO ENDEREÇO:
        # bind() associa o socket ao endereço IP e porta especificados
        # '0.0.0.0' significa que o servidor escutará em todas as interfaces
        server_socket.bind((host, port))
        
        # HABILITA MODO DE ESCUTA:
        # listen(5) coloca o socket em estado de escuta, permitindo aceitar conexões
        # O número 5 define o tamanho da fila de conexões pendentes
        server_socket.listen(5)
        print(f"[*] Servidor ouvindo em {host}:{port}")
        print("[*] Aguardando conexões...")
        
        # LOOP PRINCIPAL DE ACEITAÇÃO DE CONEXÕES:
        # O servidor fica em loop infinito aceitando novas conexões
        while True:
            # ACEITAÇÃO DE CONEXÃO (BLOQUEANTE):
            # accept() bloqueia a execução até que um cliente conecte
            # Retorna um novo socket para comunicação com o cliente específico
            # e o endereço (IP, porta) do cliente
            client_socket, client_address = server_socket.accept()
            
            # CRIAÇÃO DE THREAD PARA O CLIENTE:
            # Cada cliente é atendido em uma thread separada para permitir
            # atendimento simultâneo de múltiplos clientes
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, client_address)
            )
            
            # CONFIGURAÇÃO DA THREAD COMO DAEMON:
            # Threads daemon são automaticamente encerradas quando o programa principal termina
            # Isso garante que todas as threads sejam fechadas ao encerrar o servidor
            client_thread.daemon = True
            
            # INICIALIZAÇÃO DA THREAD:
            # A thread começa a executar a função handle_client com os argumentos fornecidos
            client_thread.start()
            
    except KeyboardInterrupt:
        # TRATAMENTO DE INTERRUPÇÃO POR TECLADO:
        # Captura Ctrl+C, permitindo encerramento gracioso do servidor
        print("\n[*] Servidor encerrado")
    
    except Exception as e:
        # TRATAMENTO DE ERROS GERAIS:
        # Captura qualquer outro erro não previsto
        print(f"Erro: {e}")
    
    finally:
        # GARANTIA DE FECHAMENTO DO SOCKET:
        # Garante que o socket do servidor seja fechado mesmo em caso de erro
        # Libera a porta 8888 para uso por outros aplicativos
        server_socket.close()

if __name__ == "__main__":
    """
    Ponto de entrada do programa.
    
    Esta verificação garante que o servidor só será iniciado se o arquivo
    for executado diretamente, e não se for importado como módulo.
    
    start_server() inicia o loop principal do servidor, que só terminará
    quando o servidor for interrompido (normalmente por Ctrl+C).
    """
    start_server()
