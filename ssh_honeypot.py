# Libraries
import logging
from logging.handlers import RotatingFileHandler
import paramiko
import socket
import threading

# Constants
logging_format = logging.Formatter('%(asctime)s %(message)s')
SSH_BANNER = "SSH-2.0-SHARK-SSHServer_1.0"

#host_key = "server.key"
host_key = paramiko.RSAKey(filename='server.key')

# Loggers & Logging Files 
funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler('audits.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)


creds_logger = logging.getLogger('CredsLogger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('cmd_audits.log', maxBytes=2000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)



#  Emulated shell

def emulated_shell(channel, client_ip):
    try:
        banner = "Welcome to LEGACY-ADMIN where 'All activity is logged and monitored.'\r\n\r\n"
        # If you already sent banner before calling this, you can remove the send below
        # channel.send(banner.encode())
        prompt = "corporate-jumpbox2$ "
        channel.send(prompt.encode())

        command = b""
        while True:
            # read one byte at a time (keeps behavior interactive)
            char = channel.recv(1)
            if not char:
                # remote closed or socket error
                channel.close()
                return

            # echo back what the user typed
            channel.send(char)

            # accumulate bytes until a newline / carriage return
            command += char
            if char in (b'\r', b'\n'):
                cmd_bytes = command.strip()  # bytes
                # convert to string for logging (safe)
                try:
                    cmd_text = cmd_bytes.decode('utf-8', errors='ignore')
                    creds_logger.info(f"{client_ip} - {cmd_text}")
                except:
                     cmd_text = str(cmd_bytes)
                
                # log the command (writes to cmd_audits.log via creds_logger)
                creds_logger.info(f"{client_ip} - {cmd_text}")
                cmd = cmd_bytes.lower()              # keep bytes for comparisons below

                # handle commands
                if cmd == b'exit':
                    channel.send(b"\r\nGoodbye\r\n")
                    channel.close()
                    return
                elif cmd == b'pwd':
                    channel.send(b"\r\n/usr/local\r\n")
                elif cmd == b'whoami':
                    channel.send(b"\ncorpuseral\r\n")
                elif cmd == b'ls':
                    channel.send(b"\njumpbox1.conf\r\n")
                elif cmd == b'cat jumpbox1.conf':
                    channel.send(b"\nGo to deeboodah.com\r\n")
                else:
                    # echo unknown command back
                    if cmd:
                        channel.send(b"\n" + cmd + b"\r\n")
                    else:
                        channel.send(b"\r\n")

                # send prompt and reset buffer
                channel.send(prompt.encode())
                command = b""
    except Exception as e:
        # Print exception for debugging, don't re-raise (keeps server alive)
        print("[emulated_shell] exception:", repr(e))
        try:
            channel.close()
        except Exception:
            pass
        return



# SSH Server + sockets

class Server(paramiko.ServerInterface):

    def __init__(self, client_ip, input_username=None, input_password=None):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.input_username = input_username
        self.input_password = input_password


    def check_channel_request(self, kind: str, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        
    def get_allowed_auths(self, username):
        return "password"

    def check_auth_password(self, username, password):
        funnel_logger.info(f'Client {self.client_ip} attempted connection ' + f'username:{username}, ' + f'password:{password}')
        creds_logger.info(f'{self.client_ip}, {username}, {password}')
        if self.input_username is not None and self.input_password is not None:
            if username == self.input_username and password == self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
            
        else:
            return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    
    def check_channel_exec_request(self, channel, command):
        command = str(command)
        return True


def client_handle(client, addr, username, password):
    try:
        client_ip = client.getpeername()[0]
    except Exception:
        client_ip = addr[0]
    print(f"{client_ip} has connected to the server.")
    funnel_logger.info(f"{client_ip} connected")

    transport = None
    try:
        print("[*] Creating Transport...")
        transport = paramiko.Transport(client)
        print("[*] Transport created. Setting local_version...")
        transport.local_version = SSH_BANNER
        print(f"[*] local_version set to {transport.local_version!r}")

        server = Server(client_ip=client_ip, input_username=username, input_password=password)
        print("[*] Server object created. Adding server key...")
        transport.add_server_key(host_key)
        print("[*] Server key added. Starting server...")
        transport.start_server(server=server)
        print("[*] start_server returned. Waiting for channel.accept()...")
        channel = transport.accept(100)
        print(f"[*] transport.accept() returned: {channel!r}")


        if channel is None:
            print("[!] No channel was opened; connection likely closed by client or server.")
            return
        
        print("[*] Channel opened. Sending banner...")
        standard_banner = "Welcome to LEGACY-ADMIN where 'All activity is logged and monitored.'\r\n\r\n"  
        channel.send(standard_banner)
        emulated_shell(channel, client_ip=client_ip)


    except Exception as error:
        print(error)
        print("!!!ERROR!!!")
    finally:
        if transport is not None:

            try:
                transport.close()
            except Exception as error:
                print(error)
                print("!!!ERROR!!!")
        client.close()

# Provision SSH-Based Honeypot


def honeypot(address, port, username, password):

    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks.bind((address, port))

    socks.listen(100)
    print(f"SSH server is listening on port {port}.")

    while True:
        try:
            client, addr = socks.accept()
            ssh_honeypot_thread = threading.Thread(target=client_handle, args=(client, addr, username, password))
            ssh_honeypot_thread.start()

        except Exception as error:
            print(error)

honeypot('127.0.0.1', 2223, username = None, password = None)