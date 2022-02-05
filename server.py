from http.server import HTTPServer, BaseHTTPRequestHandler
import os


class CS2610Assn1(BaseHTTPRequestHandler):
    """
    Your task is to define this class such that it fulfills the assingment
    requirements.

    Refer to the official Python documentation for the `http.server` class for
    details on what can go in here.

    Replace this pass statement with your own code:
    """
    
    def do_GET(self):
        print("forming response...")
        print(os.listdir())
        self.send_response(404)
        self.send_header("nates-header", "You got this info back")
        self.end_headers()
        

        print("\nExiting...\n")
        exit(0)



if __name__ == '__main__':
    server_address = ('localhost', 8000)
    print(f"Serving from http://{server_address[0]}:{server_address[1]}")
    print("Press Ctrl-C to quit\n")
    try:
        HTTPServer(server_address, CS2610Assn1).serve_forever()
    except KeyboardInterrupt:
        print(" Exiting")
        exit(0)