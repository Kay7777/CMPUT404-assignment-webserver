#  coding: utf-8
import socketserver
import os
# import "./www/index.html" as basePage

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.path = self.getPath(self.data)
        self.method = self.getMethod(self.data)

        htmlContent = None
        cssContent = None

        if self.path == "/" or self.path == "/index.html":
            for file in os.listdir(os.getcwd()+'/www'):
                if file == 'base.css':
                    cssContent = self.readFile(os.getcwd()+'/www/base.css')
                elif file == 'index.html':
                    htmlContent = self.readFile(os.getcwd()+'/www/index.html')

        elif self.path == "/deep" or self.path == "/deep/" or self.path == "/deep/index.html":
            if self.path == "/deep":
                self.request.sendall(
                    bytearray("HTTP/1.1 301 Moved Permanently\r\n" + "Location: /deep/\r\n", 'utf-8'))
            for file in os.listdir(os.getcwd()+'/www/deep'):
                if file == 'deep.css':
                    cssContent = self.readFile(
                        os.getcwd()+'/www/deep/deep.css')
                elif file == 'index.html':
                    htmlContent = self.readFile(
                        os.getcwd()+'/www/deep/index.html')
        elif self.path == "/base.css":
            cssContent = self.readFile(os.getcwd()+'/www/base.css')
        elif self.path == "/deep/deep.css":
            cssContent = self.readFile(os.getcwd()+'/www/deep/deep.css')

        if self.method != "GET":
            self.request.sendall(
                bytearray("HTTP/1.1 405 Method Not Allowed\r\n", 'utf-8'))
        elif htmlContent != None:
            self.request.sendall(bytearray(
                "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"+htmlContent+"\r\n", 'utf-8'))
        elif cssContent:
            self.request.sendall(bytearray(
                "HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\n\r\n"+cssContent+"\r\n", 'utf-8'))
        elif len(self.path.split("/")) == 3 and self.path.split("/")[1] != "deep" and (self.path.split("/")[2] == "index.html" or self.path.split("/") == ""):
            self.request.sendall(
                bytearray("200 OK Not FOUND! Hardcoding? " + self.path + "\r\nContent-Type: text/html charset=utf-8\r\n\r\n", 'utf-8'))
        else:
            self.request.sendall(
                bytearray("HTTP/1.1 404 Not Found\r\nConnection: close\r\n", 'utf-8'))

        return

    def getPath(self, data):
        data = str(data, 'utf-8').split(' ')
        return data[1]

    def getMethod(self, data):
        data = str(data, 'utf-8').split(' ')
        return data[0]

    def readFile(self, file):
        with open(file, 'r') as f:
            readPage = f.read()
            f.close()
            return readPage


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
