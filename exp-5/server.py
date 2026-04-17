from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

PORT = 8000

class ServletHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != '/MethodServlet':
            return super().do_GET()

        params = parse_qs(parsed.query)
        name = params.get('name', [''])[0]
        self.send_result(name, method='GET')

    def do_POST(self):
        if self.path != '/MethodServlet':
            self.send_error(404, 'Not Found')
            return

        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length).decode('utf-8')
        params = parse_qs(post_data)

        name = params.get('name', [''])[0]
        self.send_result(name, method='POST')

    def send_result(self, name, method):
        if method == 'GET':
            title = 'GET Method Used'
            bg = '#e3f2fd'
            color = 'blue'
        else:
            title = 'POST Method Used'
            bg = '#ffebee'
            color = 'red'

        content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<title>Result</title>
<style>
body {{ font-family: Arial; text-align: center; background:{bg}; padding-top: 100px; }}
h1 {{ color: {color}; }}
</style>
</head>
<body>
<h1>{title}</h1>
<h2>Hello {name}</h2>
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
