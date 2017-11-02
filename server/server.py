#!/usr/bin/python
''' server.py '''

import socket
import threading
import argparse
import json
import netifaces
import requests

class dataParsing(object):
    ''' '''
    def __init__(self, receivedStr):
        self.receivedStr = receivedStr
        # self.dataInterpretation(self.receivedStr)
        #import api
        #print(api.apiCall('https://api.darksky.net/forecast/faee14155496c39ee342cfd902632560/37.8267,-122.4233'))

    def dataInterpretation(self, recievedStr):
        with open('keywords.json') as json_data:
            jsonData = json.load(json_data)
            recievedList = recievedStr.split(" ")
            found = []
            for key in jsonData:
                for keyword in jsonData[key]:
                    for word in recievedList:
                        if word == keyword:
                            found.append(keyword)
            return(found)


        # split receivedStr into words, loop over words and check if they are in the json
        # dont reutrn or print anything

class server(object):
    ''' server is a class that handled network connections, pass host ip and host port for init'''
    def __init__(self, hostIP, hostPort):
        self.hostIP = hostIP
        self.hostPort = hostPort
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostIP, self.hostPort))
        print('** server started on\n** internal - {}:{}\n** external - {}:{}\n'.format(self.getServerIP()['internal'], self.hostPort,self.getServerIP()['external'] ,self.hostPort))

    def serverListen(self):
        ''' serverListen listens to incoming connects from clients and opens a new thread for each connected client '''
        self.socket.listen(15)
        while True:
            try:
                client, clientAddress = self.socket.accept()
                client.settimeout(120)
                threading.Thread(target=self.receiveFromClient,args = (client, clientAddress)).start()
                print('** Client Connected {} - {}'.format(clientAddress, self.getIpData(clientAddress)['city']))
            except:
                raise Exception('Client connection error')

    def getIpData(self, clientAddress):
        '''gets ip information in json format from ip address'''
        request = requests.get('http://ip-api.com/json/{}'.format(clientAddress))
        requestJson = request.json()
        if requestJson['status'] == 'success':
            return requestJson
        else:
            return self.getIpData('') #gets the ip for the server as oppose to client - as they should be on the same network

    def receiveFromClient(self, client, clientAddress):
        ''' receiveFromClient handles incoming data from clients '''
        byteSize = 1024
        while True:
            try:
                receivedData = client.recv(byteSize)
                if receivedData and type(receivedData) == bytes:
                    receivedStr = receivedData.decode()
                    # send to language decoder
                    client.sendall(receivedData)
                    #datax = dataParsing(receivedStr)
                    #print(dataParsing.dataInterpretation(receivedStr))
                else:
                    print('** Client Disconnected {}'.format(clientAddress))
                    client.close()
                    return False
            except:
                client.close()
                return False

    def getServerIP(self):
        deviseName = netifaces.gateways()['default'][netifaces.AF_INET][1]
        return {'internal': netifaces.ifaddresses(deviseName)[netifaces.AF_INET][0]['addr'],'external': self.getIpData('')['query']}
        

def getArgs():
    ''' getArgs returns all program arguments '''
    parser = argparse.ArgumentParser(description='') # Add description
    parser.add_argument('-p', '--port', metavar='Port', default=1143, type=int, help='Server port')
    return parser.parse_args()

def drawHeader():
    ''' draws program ui header '''
    print('*** Server Header ***\nWelcome\n\n')

def main():
    ''' main '''
    drawHeader()
    args = getArgs()
    if args.port != 1143:
        print('** no server port specified using default')
    server('', args.port).serverListen() # i have passed empty string for the host ip as it will be filled in later

if __name__ == '__main__':
    main()
