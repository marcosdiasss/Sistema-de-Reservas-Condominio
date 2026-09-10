# =====================================================
# morador.py
# Regras de negócio relacionadas ao morador (CRUD)
# =====================================================

import banco
import re


def cadastrar_morador(dados):
   
    email = dados.get("email")
    senha = dados.get("senha")
    nome = dados.get("nome")
    cpf = dados.get("cpf")
    telefone = dados.get("telefone")
    bloco = dados.get("bloco")
    apartamento = dados.get("apartamento")

    if not all([email, senha, nome, cpf, telefone, bloco, apartamento]):
        return {"sucesso": False, "mensagem": "Preencha todos os campos."}

    if len(cpf) != 11 or not cpf.isdigit():
        return {"sucesso": False, "mensagem": "CPF deve conter exatamente 11 números."}

    if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome):
        return {"sucesso": False, "mensagem": "Nome deve conter apenas letras."}

    if not apartamento.isdigit() or len(apartamento) > 3:
        return {"sucesso": False, "mensagem": "Apartamento deve conter só números (até 3 dígitos)."}

    if "@" not in email or "." not in email.split("@")[-1]:
        return {"sucesso": False, "mensagem": "Informe um e-mail válido."}

    if len(senha) < 4:
        return {"sucesso": False, "mensagem": "A senha deve ter pelo menos 4 caracteres."}

    telefone_numeros = "".join(caractere for caractere in telefone if caractere.isdigit())
    if len(telefone_numeros) < 10 or len(telefone_numeros) > 11:
        return {"sucesso": False, "mensagem": "Telefone deve ter 10 ou 11 números (com DDD)."}

    sucesso, mensagem_erro = banco.cadastrar_morador(
        email, senha, nome, cpf, telefone, bloco, apartamento
    )

    if not sucesso:
        return {"sucesso": False, "mensagem": mensagem_erro}

    return {"sucesso": True, "mensagem": "Morador cadastrado com sucesso."}


def consultar_moradores():
    """Retorna a lista de moradores cadastrados."""
    moradores = banco.consultar_moradores()
    return {"sucesso": True, "moradores": moradores}


def alterar_morador(dados):
    """Valida e atualiza os dados de um morador já cadastrado."""
    id_morador = dados.get("id_morador")
    nome = dados.get("nome")
    cpf = dados.get("cpf")
    telefone = dados.get("telefone")
    bloco = dados.get("bloco")
    apartamento = dados.get("apartamento")

    if not all([id_morador, nome, cpf, telefone, bloco, apartamento]):
        return {"sucesso": False, "mensagem": "Preencha todos os campos."}

    if len(cpf) != 11 or not cpf.isdigit():
        return {"sucesso": False, "mensagem": "CPF deve conter exatamente 11 números."}

    if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome):
        return {"sucesso": False, "mensagem": "Nome deve conter apenas letras."}

    if not apartamento.isdigit() or len(apartamento) > 3:
        return {"sucesso": False, "mensagem": "Apartamento deve conter só números (até 3 dígitos)."}

    telefone_numeros = "".join(caractere for caractere in telefone if caractere.isdigit())
    if len(telefone_numeros) < 10 or len(telefone_numeros) > 11:
        return {"sucesso": False, "mensagem": "Telefone deve ter 10 ou 11 números (com DDD)."}

    sucesso, mensagem_erro = banco.alterar_morador(
        id_morador, nome, cpf, telefone, bloco, apartamento
    )

    if not sucesso:
        return {"sucesso": False, "mensagem": mensagem_erro}

    return {"sucesso": True, "mensagem": "Morador alterado com sucesso."}
