#!usr/bin/python

import socket
import time

def respondHeader(code):
    header = ''
    if code == 200:
        header += "HTTP/1.1 200 OK\n"
    elif code == 404:
        header += "HTTP/1.1 404 Not Found\n"

    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    header += 'Date: ' + current_date + '\n'
    header += 'Server: Simple-Python-HTTP-Server\n'
    header += 'Connection: close\n\n'

    return header


HOST = 'guineapig.cs.umanitoba.ca'
PORT = 15086
address = (HOST, PORT)
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    mySocket.bind((HOST, PORT))
except Exception as e:
    print("Error in binding port: ", PORT, " --- message: ", e)

print("Connected successfully with: ", PORT)


while True:
    mySocket.listen(10)
    requestSocket, address = mySocket.accept()
    #requestSocket.settimeout(30)

    print("Got request!")

    data = requestSocket.recv(4096)
    socketString = bytes.decode(data)

    requestMethod = socketString.split(' ')[0]
    print("Method: %s", requestMethod)
    print("Message body: %s", socketString)

    if requestMethod == 'GET' or requestMethod == 'POST':
        requestedContent = socketString.split(' ')[1].split('?')[0]

        if requestedContent == '/':
            requestedContent = '/index.html'

        requestedContent = requestedContent.strip('/')

        # socketFile =
        try:
            socketFile = open(requestedContent, 'rb')
            #if requestMethod == 'GET':
            response = socketFile.read()
            socketFile.close()

            headers = respondHeader(200)
        except Exception as e:
            print("file not found", e)
            headers = respondHeader(404)
            response = """
                <html>
                <body>
                    <p>Error 404: File not found</p>
                    <p>Python HTTP server</p>
                </body>
                </html>"""

        responseMessage = headers.encode()
        #if requestMethod == 'GET':
        responseMessage += response

        requestSocket.send(responseMessage)
        # socketFile.close()
        requestSocket.close()
        #mySocket.close()

    else:
        print("Does not support given method!")
