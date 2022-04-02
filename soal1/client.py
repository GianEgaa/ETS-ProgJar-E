import socket
import json
import logging
import threading
import datetime
import random
from tabulate import tabulate

server_address = ('172.16.16.104', 12000)

def make_socket(destination_address='localhost',port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def deserealisasi(s):
    logging.warning(f"deserialisasi {s.strip()}")
    return json.loads(s)
    

def send_command(command_str):
    alamat_server = server_address[0]
    port_server = server_address[1]
    sock = make_socket(alamat_server,port_server)

    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = deserialisasi(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False

def getdatapemain(nomor=0):
    cmd=f"getdatapemain {nomor}\r\n\r\n"
    hasil = send_command(cmd)
    if (hasil):
        pass
    else:
        print("kegagalan pada data transfer")
    return hasil

# lihat versi
def version():
    cmd=f"versi \r\n\r\n"
    hasil = send_command(cmd)
    return hasil

def getdatapemain_multithread(total_request, data_table):
    total_response = 0
    texec = dict()
    start_time = datetime.datetime.now()

    for i in range(total_request):
        texec[i] = threading.Thread(target=getdatapemain, args=(random.randint(1, 20),))
        texec[i].start()

    for i in range(total_request):
        if (texec[i] != -1):
            total_response = total_response + 1
        else: 
            continue
        texec[i].join()
        

    finish_time = datetime.datetime.now()
    final_time = finish_time - start_time
    # memasukan respon time kedalam tabel
    data_table.append([total_request, total_request, total_response, final_time])
    

if __name__ == '__main__':
    h = version()
    if (h):
        print(h)
    
    total_request = [1, 5, 10, 20]
    data_table = []
    
    for request in total_request:
        getdatapemain_multithread(request, data_table)
        
    table_header = ["Total Thread", " Total Request", "Total Response", "Latency"]
    print(tabulate(data_table, headers=table_header, tablefmt="fancy_grid"))
