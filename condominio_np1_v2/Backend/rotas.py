import os
import usuario
import morador
import area
import reserva

PASTA_FRONTEND = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Frontend")


def tratar_get(caminho):

    caminho_arquivo = os.path.join(PASTA_FRONTEND, caminho.lstrip("/"))

    if not os.path.isfile(caminho_arquivo):
        return 404, "text/plain; charset=utf-8", "Arquivo não encontrado".encode("utf-8")

    tipo_conteudo = descobrir_tipo(caminho_arquivo)

    with open(caminho_arquivo, "rb") as arquivo:
        conteudo = arquivo.read()

    return 200, tipo_conteudo, conteudo


def tratar_post(caminho, dados_json):
    

    #LOGIN 
    if caminho == "/login":
        email = dados_json.get("email")
        senha = dados_json.get("senha")
        resultado = usuario.fazer_login(email, senha)
        status_code = 200 if resultado["sucesso"] else 401
        return status_code, resultado

    # MORADORES 
    if caminho == "/moradores/cadastrar":
        resultado = morador.cadastrar_morador(dados_json)
        return (200 if resultado["sucesso"] else 400), resultado

    if caminho == "/moradores/consultar":
        resultado = morador.consultar_moradores()
        return 200, resultado

    if caminho == "/moradores/alterar":
        resultado = morador.alterar_morador(dados_json)
        return (200 if resultado["sucesso"] else 400), resultado

    # ---------- ÁREAS COMUNS ----------
    if caminho == "/areas/cadastrar":
        resultado = area.cadastrar_area(dados_json)
        return (200 if resultado["sucesso"] else 400), resultado

    if caminho == "/areas/consultar":
        resultado = area.consultar_areas()
        return 200, resultado

    if caminho == "/areas/alternar_status":
        resultado = area.alternar_status_area(dados_json)
        return (200 if resultado["sucesso"] else 400), resultado

    # ---------- RESERVAS ----------
    if caminho == "/reservas/criar":
        resultado = reserva.criar_reserva(dados_json)
        return (200 if resultado["sucesso"] else 400), resultado

    if caminho == "/reservas/consultar":
        resultado = reserva.consultar_reservas(dados_json)
        return 200, resultado

    if caminho == "/reservas/cancelar":
        resultado = reserva.cancelar_reserva(dados_json)
        return (200 if resultado["sucesso"] else 400), resultado

    return 404, {"sucesso": False, "mensagem": "Rota não encontrada."}


def descobrir_tipo(caminho_arquivo):
    """Descobre o Content-Type da resposta baseado na extensão do arquivo."""
    if caminho_arquivo.endswith(".html"):
        return "text/html; charset=utf-8"
    if caminho_arquivo.endswith(".css"):
        return "text/css; charset=utf-8"
    if caminho_arquivo.endswith(".js"):
        return "application/javascript; charset=utf-8"
    if caminho_arquivo.endswith(".png"):
        return "image/png"
    if caminho_arquivo.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    if caminho_arquivo.endswith(".svg"):
        return "image/svg+xml"
    return "application/octet-stream"
