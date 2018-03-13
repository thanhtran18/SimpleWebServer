#!usr/bin/python

import socket

HOST = 'guineapig.cs.umanitoba.ca'
PORT = 15086
address = (HOST, PORT)
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def bindServer(thisSocket):
    try:
        thisSocket.bind((HOST, PORT))
    except socket.error as se:
        print("Error in binding port: ", PORT, " --- message: ", se)

    print("Connected successfully with: ", PORT)

    listenForRequests(thisSocket)


def listenForRequests(thisSocket):
    thisSocket.listen(5)
    while True:
        print("Listening for requests...")

        requestSocket, address = thisSocket.accept()
        requestSocket.settimeout(30)
        print("Got request!")

        data = requestSocket.recv(2048)
        socketString = bytes.decode(data)

        requestMethod = socketString.split(' ')[0]
        print("Method: %s", requestMethod)
        print("Message body: %s", socketString)

        if requestMethod == 'GET' or requestMethod == 'POST':
            requestedContent = socketString.split(' ')[1].split('?')[0]

            if requestedContent == '/':
                requestedContent = '/index.html'

            #socketFile =
            try:
                socketFile = open(requestedContent, 'rb')
                if requestMethod == 'GET':
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
            if requestMethod == 'GET':
                responseMessage += response

            requestSocket.send(responseMessage)
            #socketFile.close()
            requestSocket.close()
            thisSocket.close()



        else:
            print("Does not support given method!")


def respondHeader(code):
    header = ""
    if code == 200:
        header = "HTTP/1.1 200 OK\n"
    elif code == 404:
        header = "HTTP/1.1 404 Not Found\n"

    header += "Content-Type: texh/html\n\n"
    return header


bindServer(mySocket)
