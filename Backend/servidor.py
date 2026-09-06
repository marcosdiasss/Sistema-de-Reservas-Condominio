# =====================================================
# servidor.py
# Sobe um servidor HTTP simples (sem frameworks) usando o
# módulo nativo http.server, e delega as requisições para
# as funções de rotas.py
# =====================================================

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import rotas

HOST = "localhost"
PORTA = 8000


class ManipuladorRequisicoes(BaseHTTPRequestHandler):

    def do_GET(self):
        # A raiz "/" precisa de um REDIRECIONAMENTO de verdade para
        # "/HTML/index.html" (e não só servir o conteúdo por baixo dos
        # panos), senão os links relativos entre as páginas do Frontend
        # (ex: "opcoes.html") quebram, porque o navegador continuaria
        # achando que está na raiz do site.
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/HTML/index.html")
            self.end_headers()
            return

        status_code, tipo_conteudo, conteudo = rotas.tratar_get(self.path)
        self.send_response(status_code)
        self.send_header("Content-Type", tipo_conteudo)
        self.end_headers()
        self.wfile.write(conteudo)

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        corpo = self.rfile.read(tamanho)

        try:
            dados_json = json.loads(corpo) if corpo else {}
        except json.JSONDecodeError:
            dados_json = {}

        status_code, resposta = rotas.tratar_post(self.path, dados_json)

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(resposta).encode("utf-8"))

    def log_message(self, formato, *args):
        # Log simples em ASCII (evita caracteres estranhos no terminal do Windows)
        print("Requisicao:", self.address_string(), "-", formato % args)


def iniciar_servidor():
    servidor = HTTPServer((HOST, PORTA), ManipuladorRequisicoes)
    print(f"Servidor rodando em http://{HOST}:{PORTA}")
    servidor.serve_forever()


if __name__ == "__main__":
    iniciar_servidor()
