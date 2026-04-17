from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs

PORT = 8000

class ServletHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/UserServlet':
            self.send_error(404, 'Not Found')
            return

        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length).decode('utf-8')
        params = parse_qs(post_data)

        name = params.get('username', [''])[0]
        age = params.get('age', [''])[0]

        content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<title>Result</title>
<style>
body {{ font-family: Arial; text-align: center; background: #f5f7fa; padding-top: 100px; }}
h1 {{ color: green; }}
</style>
</head>
<body>
<h1>Welcome {name}!</h1>
<h2>Your Age is: {age}</h2>
</body>
</html>"""

        encoded = content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', PORT), ServletHandler)
    print(f'Serving at http://127.0.0.1:{PORT}/')
    print('Open the browser and submit the form from index.html')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
        server.server_close()
