from client import *
import json

def setup_client(addr):
    global client
    client = Client(addr)
    print('Client ok ' + str(client.verify_guest()))

if __name__ == '__main__':
    global client
    setup_client(Guest(url="monitorvm:8080", version="1.3"))
    print(client.machineInfo().json())