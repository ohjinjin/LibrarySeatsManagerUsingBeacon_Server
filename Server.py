import socket
import time
from slacker import Slacker
import os
import socket
import threading

class ClientThread(threading.Thread):
    def __init__(self,ip,port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        print ("[+] New thread started for "+ip+":"+str(port))

    def run(self):
        while True:
            # 클라이언트로 전송해줍니다
            clientSock.sendall("AT".encode())

            try:
                # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다. 
                data = clientSock.recv(1024)

                # 빈 문자열을 수신하면 루프를 중지합니다. 
                if not data:
                    slack.chat.post_message('#general ','network pipe was broken')
                    print("network pipe was broken")
                    break
            except socket.error as e:
                slack.chat.post_message('#general ','network pipe was broken')
                print("network pipe was broken")
                clientSock.close()
                

            # 수신받은 문자열을 출력합니다.
            print('Received from', ip, data.decode())

            time.sleep(1)


# 스레드를 관리
threads = []

# for Slack
token='xoxb-xxxx-xxxx'
slack= Slacker(token)

# 접속할 서버 주소입니다. 여기에서는 루프백(loopback) 인터페이스 주소 즉 localhost를 사용합니다. 
HOST = '192.168.0.20'

# 클라이언트 접속을 대기하는 포트 번호입니다.   
PORT = 8080

# 소켓 객체를 생성합니다. 
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 포트 사용중이라 연결할 수 없다는 
# WinError 10048 에러 해결를 위해 필요합니다. 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
# HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
# 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다. 
# PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.  
server_socket.bind((HOST, PORT))


# 무한루프를 돌면서 
while True:  
    # 서버가 클라이언트의 접속을 허용하도록 합니다. 
    server_socket.listen(5)

    # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다. 
    (clientSock, (ip, port)) = server_socket.accept()

    # 접속한 클라이언트의 주소입니다.
    print('Connected by', ip)
    newthread = ClientThread(ip, port)
    newthread.start()
    threads.append(newthread)

# 소켓을 닫습니다.
server_socket.close()
