import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(50)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)


if __name__ == "__main__":
    HOST, PORT = "192.168.1.141", 2000

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()