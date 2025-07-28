#!/usr/bin/env python3
import http.server
import socketserver
import os

# 切换到当前目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"服务器启动在 http://localhost:{PORT}")
    print("请在浏览器中访问 http://localhost:8000/comparison.html")
    print("按 Ctrl+C 停止服务器")
    httpd.serve_forever()