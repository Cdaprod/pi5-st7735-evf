"""Standard-library HTTP/MJPEG server. Example: python evf.py --mock --web --no-display"""
from __future__ import annotations

import json
import socket
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from ..input.actions import UIAction

PAGE = b'''<!doctype html><html><head><meta name="viewport" content="width=device-width"><title>EVF Monitor</title>
<style>body{margin:0;background:#101216;color:#e8edf2;font:15px system-ui}header,main{max-width:1100px;margin:auto;padding:1rem}main{display:grid;grid-template-columns:3fr 1fr;gap:1rem}.card{background:#1a1e24;border:1px solid #343b45;border-radius:9px;padding:1rem}img{display:block;max-width:100%;background:#000}.video{width:100%;aspect-ratio:16/9;object-fit:contain}.mirror{width:128px;height:128px;image-rendering:pixelated}button{color:#fff;background:#303946;border:1px solid #647080;padding:.7rem;margin:.2rem;border-radius:5px}dl{display:grid;grid-template-columns:1fr 1fr}dd{margin:0;text-align:right}@media(max-width:700px){main{grid-template-columns:1fr}}</style></head>
<body><header><h1>EVF Monitor</h1></header><main><section class="card"><img class="video" src="/video.mjpg" alt="Live video"></section><aside class="card"><h2>ST7735</h2><img id="ui" class="mirror" src="/ui.png"><h2>Status</h2><dl id="status"></dl></aside><section class="card"><h2>Controls</h2><div id="controls"></div></section></main>
<script>const actions=['MENU','BACK','PREVIOUS','NEXT','SELECT','TOGGLE_FOCUS_ASSIST','TOGGLE_ZEBRA','TOGGLE_CROSSHAIR','TOGGLE_HISTOGRAM'];for(const a of actions){let b=document.createElement('button');b.textContent=a.replaceAll('_',' ');b.onclick=()=>fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:a})});controls.append(b)}async function update(){let s=await(await fetch('/api/status')).json();status.innerHTML=Object.entries(s).map(([k,v])=>`<dt>${k}</dt><dd>${v??'-'}</dd>`).join('');ui.src='/ui.png?t='+Date.now()}setInterval(update,1000);update()</script></body></html>'''


def make_handler(hub, dispatch):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_): pass
        def _send(self, code, body, content_type):
            self.send_response(code); self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
            self.end_headers(); self.wfile.write(body)
        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/": self._send(200, PAGE, "text/html; charset=utf-8")
            elif path == "/api/status":
                payload = hub.status(); payload["hostname"] = socket.gethostname()
                self._send(200, json.dumps(payload).encode(), "application/json")
            elif path == "/ui.png":
                body = hub.ui_png()
                self._send(200 if body else 503, body, "image/png")
            elif path in ("/video", "/video.mjpg"):
                self.send_response(200); self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame"); self.end_headers()
                generation = -1
                try:
                    while True:
                        generation = hub.wait_for_generation(generation)
                        jpg = hub.jpeg()
                        self.wfile.write(b"--frame\r\nContent-Type: image/jpeg\r\nContent-Length: " + str(len(jpg)).encode() + b"\r\n\r\n" + jpg + b"\r\n")
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError): pass
            else: self._send(404, b"not found", "text/plain")
        def do_POST(self):
            if urlparse(self.path).path != "/api/action": self._send(404, b"not found", "text/plain"); return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 4096: raise ValueError("request too large")
                action = UIAction(json.loads(self.rfile.read(length)).get("action"))
            except (ValueError, TypeError, json.JSONDecodeError):
                self._send(400, b'{"error":"invalid action"}', "application/json"); return
            dispatch(action); self._send(202, json.dumps({"accepted": action.value}).encode(), "application/json")
    return Handler


class _HTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class WebServer:
    def __init__(self, hub, dispatch, host="0.0.0.0", port=8080):
        self.httpd = _HTTPServer((host, port), make_handler(hub, dispatch))
        self.thread = threading.Thread(target=self.httpd.serve_forever, name="evf-web", daemon=True)
    @property
    def address(self): return self.httpd.server_address
    def start(self): self.thread.start()
    def close(self):
        self.httpd.shutdown(); self.httpd.server_close()
        if self.thread.is_alive(): self.thread.join(timeout=2)
