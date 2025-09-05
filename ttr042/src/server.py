#!/bin/python3


import socketserver
import sys

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).decode()
        print(data)

        request_line = data.splitlines()[0]
        method, path, _ = request_line.split()

        # Find the host and port number
        host_header = None
        for line in data.splitlines():
            if line.lower().startswith("host"):
                host_header = line.split(":", 1)[1].strip()
                break

        if method == "GET" and path == "/helloworld":
            body = f"{host_header}"
            response = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                f"{body}"
            )
        else:
            body = "Not found"
            response = "HTTP/1.1 404 Not Found\r\n"
            f"Content-Type: {len(body)}\r\n"
            "\r\n"
            f"{body}"

        self.request.sendall(response.encode())


if __name__ == "__main__":
    # Default host and port, unless args are specified
    HOST = "0.0.0.0"
    PORT = 50153

    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])


    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        print(f"starting socketserver at {HOST}:{PORT}")
        server.serve_forever()
