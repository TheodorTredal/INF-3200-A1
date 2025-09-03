#!/bin/python3

# 1.  Få opp en enkel python server som gir sitt host-port nummer som respons

# 2. Lag et shell script som deployer flere av denne serveren på forskjellige noder på klusteret
#   - input: antall noder som skal kjøre
#   - output: en json streng som viser alle host-port komboene av serverene som kjører
#       - Lage en mekanisme som finner ut om en node er ledig





# from flask import Flask, request
# import sys

# app = Flask(__name__)

# @app.route("/helloworld", methods=["GET"])
# def helloworld():
#     print(f"request.host: {request.host}")
#     return request.host


# if __name__ == "__main__":
#     HOST = "0.0.0.0"
#     PORT = 50153
#     print(f"Starting server at {HOST}:{PORT}")


#     if len(sys.argv) > 1:
#         HOST = sys.argv[1]
#     if len(sys.argv) > 2:
#         PORT = int(sys.argv[2])

#     app.run(host=HOST, port=PORT)




import socketserver
import sys

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).decode()
        print(data)

        request_line = data.splitlines()[0]
        method, path, _ = request_line.split()

        # Find the host header
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
    HOST = "0.0.0.0"
    PORT = 50153

    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])


    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        print(f"starting socketserver at {HOST}:{PORT}")
        server.serve_forever()
