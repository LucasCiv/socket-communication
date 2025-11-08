import socket

def start_client(host=''IP_DO_SERVIDOR'', port=8888):
    """
    Função principal que inicia o cliente de chat.
    
    Estabelece conexão com o servidor e gerena o loop de comunicação
    para envio e recebimento de mensagens.
    """
    
    # Cria socket TCP/IP para comunicação com o servidor
    # AF_INET = IPv4, SOCK_STREAM = TCP (protocolo orientado a conexão)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Estabelece conexão com o servidor no endereço e porta especificados
        # connect() inicia o three-way handshake do protocolo TCP
        # Se o servidor não estiver rodando, lançará ConnectionRefusedError
        client_socket.connect((host, port))
        print(f"[+] Conectado ao servidor {host}:{port}")
        print("[*] Digite 'sair' para encerrar")
        
        # Loop principal de comunicação
        # Mantém o cliente ativo até que o usuário decida encerrar
        while True:
            # Solicita mensagem do usuário via input
            # input() é bloqueante - aguarda o usuário digitar e pressionar Enter
            message = input("Você: ")
            
            # Envia a mensagem para o servidor
            # encode('utf-8') converte a string para bytes para transmissão pela rede
            # send() transmite os dados através do socket TCP estabelecido
            client_socket.send(message.encode('utf-8'))
            
            # Verifica se o usuário digitou 'sair' para encerrar a conexão
            # lower() garante que funciona independente de maiúsculas/minúsculas
            if message.lower() == 'sair':
                break
                
            # Aguarda resposta do servidor
            # recv(1024) é bloqueante - fica aguardando dados do servidor
            # 1024 é o tamanho máximo do buffer de recebimento
            # decode('utf-8') converte os bytes recebidos de volta para string
            response = client_socket.recv(1024).decode('utf-8')
            
            # Exibe a resposta recebida do servidor para o usuário
            print(f"Servidor: {response}")
            
    except ConnectionRefusedError:
        # Este erro ocorre quando o servidor não está disponível na porta especificada
        # Pode ser porque o servidor não foi iniciado ou está em endereço diferente
        print("[-] Servidor não encontrado. Verifique se o servidor está rodando.")
        
    except Exception as e:
        # Captura outros erros genéricos que podem ocorrer durante a comunicação
        # Como quebras de conexão, timeouts, ou problemas de rede
        print(f"Erro: {e}")
        
    finally:
        # Garante que o socket seja fechado mesmo em caso de erro
        # Fechar o socket libera os recursos do sistema operacional
        # Envia o FIN do TCP para encerramento gracioso da conexão
        client_socket.close()
        print("[-] Conexão encerrada")

if __name__ == "__main__":
    # Ponto de entrada do programa - executa a função principal
    # quando o arquivo é executado diretamente (não importado como módulo)
    start_client()
