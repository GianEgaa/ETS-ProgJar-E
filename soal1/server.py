import socket
import logging
import json
import ssl

alldata = dict()
alldata['1']=dict(nomor=1, nama="Eko", posisi="GK")
alldata['2']=dict(nomor=2, nama="Aris", posisi="DF")
alldata['3']=dict(nomor=3, nama="Ripto", posisi="DF")
alldata['4']=dict(nomor=4, nama="Munawir", posisi="DF")
alldata['5']=dict(nomor=5, nama="Linda", posisi="DF")
alldata['6']=dict(nomor=6, nama="Harun", posisi="MF")
alldata['7']=dict(nomor=7, nama="Sri Gembira", posisi="FW")
alldata['8']=dict(nomor=8, nama="Agung", posisi="MF")
alldata['9']=dict(nomor=9, nama="Sarwono", posisi="FW")
alldata['10']=dict(nomor=10, nama="BudiBowo", posisi="FW")
alldata['11']=dict(nomor=11, nama="Andreas", posisi="FW")
alldata['12']=dict(nomor=21, nama="Dade", posisi="MF")
alldata['13']=dict(nomor=13, nama="Yuni", posisi="RT")
alldata['14']=dict(nomor=14, nama="Kifdullah", posisi="RFW")
alldata['15']=dict(nomor=15, nama="Nand", posisi="LMF")
alldata['16']=dict(nomor=16, nama="Dite", posisi="MF")
alldata['17']=dict(nomor=17, nama="Sakti", posisi="MF")
alldata['18']=dict(nomor=18, nama="Faiz", posisi="MF")
alldata['19']=dict(nomor=19, nama="Rio", posisi="GK")
alldata['20']=dict(nomor=20, nama="Fanny", posisi="FM")

def versi():
    return "versi 0.0.1"


def proses_request(request_string):
    #format request
    # NAMACOMMAND spasi PARAMETER
    cstring = request_string.split(" ")
    hasil = None
    try:
        command = cstring[0].strip()
        if (command == 'get_pemain_data'):
            # getdata spasi parameter1
            # parameter1 harus berupa nomor pemain
            logging.warning("getdata")
            player_number = cstring[1].strip()
            try:
                logging.warning(f"data {player_number} ketemu")
                hasil = alldata[player_number]
            except:
                hasil = None
        elif (command == 'versi'):
            hasil = versi()
    except:
        hasil = None
    return hasil


def serialisasi(a):
    #print(a)
    #serialized = str(dicttoxml.dicttoxml(a))
    serialized =  json.dumps(a)
    logging.warning("serialized data")
    logging.warning(serialized)
    return serialized

def run_server(server_address):
    #--- INISIALISATION ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1000)


    while True:
        # Wait for a connection
        logging.warning("waiting for a connection")
        connection, client_address = sock.accept()
        logging.warning(f"Incoming connection from {client_address}")
        # Receive the data in small chunks and retransmit it

        try:
            selesai=False
            data_received="" #string
            while True:
                data = connection.recv(32)
                logging.warning(f"received {data}")
                if data:
                    data_received += data.decode()
                    if "\r\n\r\n" in data_received:
                        selesai=True

                    if (selesai==True):
                        hasil = proses_request(data_received)
                        logging.warning(f"hasil proses: {hasil}")
                        hasil = serialisasi(hasil)
                        hasil += "\r\n\r\n"
                        connection.sendall(hasil.encode())
                        selesai = False
                        data_received = ""  # string
                        break

                else:
                   logging.warning(f"no more data from {client_address}")
                   break
            # Clean up the connection
        except ssl.SSLError as error_ssl:
            logging.warning(f"SSL error: {str(error_ssl)}")

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 12000))
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    finally:
        logging.warning("selesai")
