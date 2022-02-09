from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes


#TODO: Add links to other pages

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
        self.send_header("Cache-Control", "5")

    def serveFile(self, filePath, mimeType, statusCode=200):
        self.beginResponse(statusCode)
        f = open(filePath, "rb")
        data = f.read()
        f.close()
        self.send_header("Content-Length", str(len(data)))

        self.send_header("Content-Type", mimeType)
        self.end_headers()
        self.wfile.write(data)


    def sendRedirect(self, redirectLocation):
        self.beginResponse(301)
        self.send_header("Location", redirectLocation)
        self.end_headers()

    def makeDebug(self):
        self.beginResponse(200)
        content = f"""
        <h1>Debugging page</h1>
        <p>Server version: {self.server_version}</p>
        <p>Server timestamp: {self.date_time_string()}</p>
        <p>User-agent address: {self.client_address[0]}:{self.client_address[1]}</p>
        <p>Requested path: "{self.path}"</p>
        <p>HTTP request command: {self.command}</p>
        <p>Request version: {self.request_version}</p>
        <p>Headers
            <ul>
        """
        for h, v in self.headers.items():
            content += "<li>"
            content += h
            content += ": "
            content += v
            content += "</li>"
        
        content += "</ul></p>"

        data = bytes(content, "utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(data)

    def teapotResponse(self):
        self.serveFile("error418.html", "text/html", 418)
        

    # TODO: This could be done dynamically, but unclear if it's required
    def denyAccess(self):
        self.serveFile("error403.html", "text/html", 403)

    # TODO: could be dynamic
    def send404(self):
        self.serveFile("error404.html", "text/html", 404)
        

    def inspectPath(self, requestPath):
        if requestPath == "":
            self.sendRedirect("index.html")
        elif os.access(requestPath + ".html", os.R_OK):
            self.sendRedirect(requestPath + ".html")
        elif requestPath == "debugging":
            self.makeDebug()
        elif requestPath == "make-coffee":
            self.teapotResponse()
            
        else:
            self.send404()

    def do_GET(self):
        relativePath = self.path[1:]
        print(relativePath)
        if os.access(relativePath, os.R_OK):
            self.serveFile(relativePath, mimetypes.guess_type(relativePath))
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