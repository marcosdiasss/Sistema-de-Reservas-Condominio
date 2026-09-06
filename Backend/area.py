# =====================================================
# area.py
# Regras de negócio relacionadas às áreas comuns (CRUD)
# =====================================================

import banco


def cadastrar_area(dados):
    """Valida e cadastra uma nova área comum."""
    nome = dados.get("nome")
    descricao = dados.get("descricao", "")
    capacidade = dados.get("capacidade")

    if not nome or not capacidade:
        return {"sucesso": False, "mensagem": "Preencha o nome e a capacidade da área."}

    try:
        capacidade = int(capacidade)
    except (TypeError, ValueError):
        return {"sucesso": False, "mensagem": "Capacidade deve ser um número."}

    if capacidade <= 0:
        return {"sucesso": False, "mensagem": "Capacidade deve ser maior que zero."}

    sucesso, mensagem_erro = banco.cadastrar_area(nome, descricao, capacidade)

    if not sucesso:
        return {"sucesso": False, "mensagem": mensagem_erro}

    return {"sucesso": True, "mensagem": "Área cadastrada com sucesso."}


def consultar_areas():
    """Retorna a lista de áreas comuns cadastradas."""
    areas = banco.consultar_areas()
    return {"sucesso": True, "areas": areas}


def alternar_status_area(dados):
    """Ativa ou desativa uma área comum (nunca apaga o registro)."""
    id_area = dados.get("id_area")

    if not id_area:
        return {"sucesso": False, "mensagem": "Área não informada."}

    sucesso, mensagem_erro = banco.alternar_status_area(id_area)

    if not sucesso:
        return {"sucesso": False, "mensagem": mensagem_erro}

    return {"sucesso": True, "mensagem": "Status da área atualizado com sucesso."}
