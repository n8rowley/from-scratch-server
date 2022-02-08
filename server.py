from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import re


class CS2610Assn1(BaseHTTPRequestHandler):
    """
    Your task is to define this class such that it fulfills the assingment
    requirements.

    Refer to the official Python documentation for the `http.server` class for
    details on what can go in here.

    Replace this pass statement with your own code:
    """
    

    def beginResponse(self, statusCode):
        self.send_response(statusCode)
        self.send_header("Connection", "close")
        self.send_header("Cache-Control", "500")

    def serveFile(self, filePath, statusCode=200):
        self.beginResponse(statusCode)
        f = open(filePath, "rb")
        data = f.read()
        f.close()
        self.send_header("Content-Length", str(len(data)))

        ext = filePath.split(".")[-1]
        self.send_header("Content-Type", "text/html") #TODO: Fix this
        self.end_headers()
        self.wfile.write(data)


    def sendRedirect(self, redirectLocation):
        self.beginResponse(301)
        self.send_header("Location", redirectLocation)
        self.end_headers()

    def makeDebug(self):
        pass

    def teapotResponse(self):
        pass

    def denyAccess(self):
        pass

    def send404(self):
        pass

    def inspectPath(self, requestPath):
        if requestPath == "":
            self.sendRedirect("index.html")
        elif os.access(requestPath + ".html", os.R_OK):
            self.sendRedirect(requestPath + ".html")
        elif requestPath.startswith("bio"):
            self.sendRedirect("about.html")

        else:
            self.send404()

    def do_GET(self):
        relativePath = self.path[1:]
        print(relativePath)
        if os.access(relativePath, os.R_OK):
            self.serveFile(relativePath)
        else:
            self.inspectPath(relativePath)

        # print("\nExiting...\n")
        # exit(0)



if __name__ == '__main__':
    server_address = ('localhost', 8000)
    print(f"Serving from http://{server_address[0]}:{server_address[1]}")
    print("Press Ctrl-C to quit\n")
    try:
        HTTPServer(server_address, CS2610Assn1).serve_forever()
    except KeyboardInterrupt:
        print(" Exiting")
        exit(0)