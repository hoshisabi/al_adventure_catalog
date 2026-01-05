import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    # Ensure we are serving from the project root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Custom handler to render Jekyll layouts
    class JekyllHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            # Map / to /index.html
            path = self.path
            if path == '/' or path == '':
                path = '/index.html'
            
            # If requesting an HTML file, try to render it with layout
            if path.endswith('.html'):
                file_path = f".{path}"
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Very basic Frontmatter parsing (just remove it)
                        if content.startswith('---'):
                            parts = content.split('---', 2)
                            if len(parts) >= 3:
                                content = parts[2]
                        
                        # Read layout and header if needed
                        if os.path.exists('_layouts/default.html'):
                            with open('_layouts/default.html', 'r', encoding='utf-8') as f:
                                layout = f.read()
                            
                            if os.path.exists('_includes/header.html'):
                                with open('_includes/header.html', 'r', encoding='utf-8') as f:
                                    header = f.read()
                                layout = layout.replace('{% include header.html %}', header)
                            
                            # Replace liquid tags (basic)
                            layout = layout.replace('{{ content }}', content)
                            layout = layout.replace('{{ site.baseurl }}', '/')
                            layout = layout.replace('{{ site.title }}', 'AL DC Catalog')
                            layout = layout.replace('{{ site.tagline }}', 'Adventure List')
                            layout = layout.replace('{{ page.title }}', 'Home') # Simplified
                            
                            self.send_response(200)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(layout.encode('utf-8'))
                            return
                    except Exception as e:
                        print(f"Error rendering {path}: {e}")
                        # Fallback to default handler
            
            return super().do_GET()

    with socketserver.TCPServer(("", PORT), JekyllHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()
