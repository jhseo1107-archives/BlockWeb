import http.server
import os

ERROR_MSG = "404 Error"
PATHS = []
EVENTS = {}

class Run:
    def __init__(self, host, port, proj_name):
        "Write Server Address || Host is String"
        "This code should be written at last line"
        if proj_name == "":
            print ('\033[96m' + "Project Name: Default" + '\033[0m' )
        else:
            print ("Project Name: {}".format(proj_name))
        print ('Started to: {}:{}'.format(host,port))
        if os.path.isfile('error_page.html'):
            pass
        else:
            with open('error_page.html', 'w') as f:
                f.write("""
                <!DOCTYPE HTML>
                <h3>404 Not Found</h3>
                """)
        
        TCP = http.server.HTTPServer((host, port), PWS)
        TCP.serve_forever()

class BlockWebs(http.server.CGIHTTPRequestHandler):
    "This is the system of server. You can make route to make new folder or use makeNewRoute(routename)."
    def do_GET(self):
        self.checking_path()
        global EVENTS
        if self.path + "_GET" in str(list(EVENTS.keys())):
            EVENTS[self.path + "_GET"]()
        else:
            pass

    def do_POST(self):
        self.checking_path()
        global EVENTS
        if self.path + "_POST" in str(list(EVENTS.keys())):
            EVENTS[self.path + "_POST"]()
        else:
            pass

    def checking_path(self):
        if os.path.exists(self.path[1:]):
            if self.path.endswith(".jpg") or self.path.endswith(".JPG"):
                self.response(200, self.path, 'image/jpeg')
            elif self.path.endswith(".png") or self.path.endswith(".PNG"):
                self.response(200, self.path, 'image/png')
            elif self.path.endswith(".html")  or self.path.endswith(".HTML"):
                self.response(200, self.path, 'text/html')
            elif self.path.endswith(".js") or self.path.endswith(".JS"):
                self.response(200, self.path, 'application/javascript')
            elif self.path.endswith(".mjs") or self.path.endswith(".MJS"):
                self.response(200, self.path, 'application/javascript') # Javascript Module
            elif self.path.endswith(".gif") or self.path.endswith(".GIF"):
                self.response(200, self.path, 'image/gif')
            elif self.path.endswith(".css") or self.path.endswith(".CSS"):
                self.response(200, self.path, 'text/css')
            elif self.path.endswith(".svg")  or self.path.endswith(".SVG"):
                self.response(200, self.path, 'image/svg+xml')
            elif self.path.endswith(".mp4"):
                self.response(200, self.path, 'video/mp4')
            elif self.path.endswith(""):
                self.response(200, "{}/index.html".format(self.path[1:]), "text/html")
        elif self.path[1:] == "":
            self.response(200, "{}/index.html".format(self.path[1:]), "text/html")
        else:
            self.not_found()

    def response(self, status_code, body, header):
        if body[0] == "/":
            body = str(body)[1:30000]
        if "image/jpeg" or 'image/png' or 'image/gif' in header:
            self.send_response(status_code)
            self.send_header("Content-Type", "{}".format(header))
            self.end_headers()
            with open("{}".format(body), "rb") as imageFile:
                self.wfile.write(imageFile.read())
        else:
            self.send_response(status_code)
            self.send_header("Content-Type", "{}; charset=utf-8".format(header))
            self.end_headers()
            with open("{}".format(body), "rb") as files:
                file = files.read()
                self.wfile.write(str(file).encode("utf-8"))

    def not_found(self):
        self.send_response(404)
        self.send_header("content-type","text-html;charset=utf-8")
        self.end_headers()
        with open('error_page.html', 'r') as f:
            self.wfile.write(str(f.read()).encode('utf8'))

    def makeNewRoute(routename):
        if routename[0] == '/':
            routename = routename[1:]
        HTML_FILE = """<!DOCTYPE HTML/>
        <html>
        <head>

        </head>

        <body>
            <h3>Hello World!</h3>
            <h3>Welcome to PWS Service!</h3>
        </body>
        </html>"""
        if not os.path.exists(routename):
            os.makedirs(routename)
            with open('{}/index.html'.format(routename), 'w') as f:
                f.write(HTML_FILE)

class Response_Handler:
    def __init__(self, route, event):
        #self.callback = callback
        self.route = route
        self.event = event

    def __call__(self, func):
        global EVENTS
        if self.event == "POST":
            if self.route + "_POST" not in str(list(EVENTS.keys())):
                EVENTS[self.route + "_POST"] = func
            
        elif self.event == "GET":
            if self.route + "_GET" not in str(list(EVENTS.keys())):
                EVENTS[self.route + "_GET"] = func
        print ("Every Events: {}".format(str(list(EVENTS.keys()))))
        print(EVENTS)