#!usr/bin/python

import socket
import time
from os import environ
import subprocess


def respondHeader(code):
    header = ''
    if code == 200:
        header += "HTTP/1.1 200 OK\n"
    elif code == 404:
        header += "HTTP/1.1 404 Not Found\n"

    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    header += 'Date: ' + current_date + '\n'
    header += 'Server: Simple-Python-HTTP-Server\n'
    # header += 'Connection: close\n\n'

    return header


HOST = 'chipmunk.cs.umanitoba.ca'
PORT = 15086
address = (HOST, PORT)
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    mySocket.bind((HOST, PORT))
    print("Connected successfully with: ", PORT)
except Exception as e:
    print("Error in binding port: ", PORT, " --- message: ", e)
    print("Please retry!")


while True:
    mySocket.listen(10)
    requestSocket, address = mySocket.accept()
    # requestSocket.settimeout(30)

    print("Got request!")

    data = requestSocket.recv(4096)
    socketString = bytes.decode(data)

    requestMethod = socketString.split(' ')[0]
    print("Method: %s", requestMethod)
    print("Message body: %s", socketString)
    uri = ''

    if requestMethod == 'GET':
        url = socketString.split(' ')[1]
        arrayContent = url.split('?')
        requestedContent = arrayContent[0]
        if len(arrayContent) > 1:
            uri = arrayContent[1]

        if requestedContent == '/':
            requestedContent = '/index.html'

        isCgi = False
        requestedContent = requestedContent.strip('/')
        if requestedContent.endswith('.cgi'):
            isCgi = True
            if len(uri) >= 1:
                print("*****************I")
                print(uri)
                environ['QUERY_STRING'] = uri
            procObject = subprocess.Popen(requestedContent, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            (stdOut, stdErr) = procObject.communicate(input=None)

        try:
            socketFile = open(requestedContent, 'rb')
            # if requestMethod == 'GET':
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

        contentType = ''
        code = ''
        if isCgi:
            responseMessage = ''
            cgiContent = stdOut.split('\n')
            contentType += cgiContent[0]
            if len(cgiContent) > 1:
                cookie = cgiContent[1]

            if len(cookie) > 0:
                environ['HTTP_COOKIE'] = cookie.split(':')[1].strip()
            contentType += '\nConnection: close\n\n'
            code = cgiContent[2:]

            headers += contentType
            # headers += code
            headers = headers.encode()
            # if requestMethod == 'GET':
            response = ''
            if len(code) > 0:
                for line in code:
                    response += line
            # responseMessage += response
            headers += response

        else:
            print("DSFSDGESRGDS F")
            headers += 'Connection: close\n\n'
            headers = headers.encode()
            headers += response
        print(headers)
        requestSocket.send(headers)
        requestSocket.close()

    elif requestMethod == 'POST':
        requestedContent = socketString.split(' ')[1]

        if requestedContent == '/':
            requestedContent = '/index.html'


        isCgi = False
        requestedContent = requestedContent.strip('/')
        if requestedContent.endswith('.cgi'):
            isCgi = True

            cgiContent = socketString.split('\n')
            environ['CONTENT_LENGTH'] = cgiContent[3].split(':')[1].strip()

            if len(cgiContent) > 1:
                uri = cgiContent[len(cgiContent) - 1].strip()
            print("&&&&&&&&&&&&&&&&&&&&&&")
            print("URI:" + uri)

            stdInput = subprocess.Popen(['echo', uri], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            pObject = subprocess.Popen(requestedContent, stdin=stdInput.stdout, stdout=subprocess.PIPE)
            # (stdOut, stdErr) = subprocess.Popen(requestedContent, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate(input=uri)
            (stdOut, stdErr) = pObject.communicate()

        try:
            socketFile = open(requestedContent, 'rb')
            # if requestMethod == 'GET':
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

        contentType = ''
        code = ''

        if isCgi:
            responseMessage = ''
            cgiContent = socketString.split('\n')
            outputArray = stdOut.split('\n')
            contentType += outputArray[0]

            # if len(cgiContent) > 1:
            #     uri = cgiContent[len(cgiContent) - 1].strip()

            if len(outputArray) > 1:
                cookie = outputArray[1]

            if len(cookie) > 0:
                environ['HTTP_COOKIE'] = cookie.split(':')[1].strip()
            contentType += '\nConnection: close\n\n'
            code = outputArray[2:]

            headers += contentType
            # headers += code
            headers = headers.encode()
            # if requestMethod == 'GET':
            response = ''
            if len(code) > 0:
                for line in code:
                    response += line
            # responseMessage += response
            headers += response

        else:
            print("DSFSDGESRGDS F")
            headers += 'Connection: close\n\n'
            headers = headers.encode()
            headers += response
        print(headers)
        requestSocket.send(headers)
        requestSocket.close()

    else:
        print("Does not support given method!")
